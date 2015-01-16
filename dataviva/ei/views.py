import re, operator
from flask import Blueprint, request, render_template, flash, g, session, \
            redirect, url_for, jsonify, abort, make_response, Response
from dataviva import db
from dataviva.ei.models import Yms, Ymr, Ymp, Ymsr, Ymsp, Ymrp, Ymsrp
from dataviva.utils import make_query
from dataviva.utils.gzip_data import gzipped
from dataviva.utils.decorators import cache_api
from sqlalchemy import func, distinct
from sqlalchemy import or_, and_

mod = Blueprint('ei', __name__, url_prefix='/ei')

allowed_when_not = {
    Ymp : set(["bra_id_s", "bra_id_r", "cnae_id_r", "cnae_id_s"]),
    Ymr : set(["bra_id_s", "hs_id", "cnae_id_s"]),
    Yms : set(["bra_id_r", "hs_id", "cnae_id_r"]),
    Ymsr : set(["hs_id"]),
    Ymrp : set(["bra_id_s", "cnae_id_s"]),
    Ymsp : set(["bra_id_r", "cnae_id_r"]),
    Ymsrp : set()
}

possible_tables = {
    "hs_id" : [Ymp, Ymrp, Ymsp, Ymsrp],
    "cnae_id_r" : [Ymr, Ymrp, Ymsr, Ymsrp],
    "bra_id_r" : [Ymr, Ymrp, Ymsr, Ymsrp],
    "cnae_id_s" : [Yms, Ymsp, Ymsr, Ymsrp],
    "bra_id_s" : [Yms, Ymsp, Ymsr, Ymsrp],
    "no_show": [Ymp, Ymr, Yms, Ymsp, Ymrp, Ymsr, Ymsrp]
}

MAX_DEPTH = {"bra_id_s": 9, "bra_id_r":9, "cnae_id_s": 3, "cnae_id_r" : 3, "hs_id": 6 }
INDICES = ["bra_id_s", "bra_id_r", "cnae_id_s", "cnae_id_r", "hs_id"]


def ei_parse_value(table, groups, column, colname, value, max_depths):
    if colname in ["month", "year"]:
        if make_query.OR in value:
            return column.in_(value.split(make_query.OR))

        return column == value
    else:

        values = value.split(make_query.OR)
        params = []

        for value in values:
            if "bra_id" in colname and len(value) > 3 and not value.startswith("4mg"):
                value = value[:3]
            elif "cnae_id" in colname and len(value) > 3:
                value = value[:3]
            if len(value) > max_depths[colname]:
                value = value[:max_depths[colname]]
            if "bra_id" in colname and len(value) in [5, 7, 8]:
                groups.remove(column)
                groups.append(func.substr(column, 1, len(value)).label(column.key))
                params.append( column.startswith(value) )
            elif colname in max_depths and len(value) != max_depths[colname]:
                if column in groups:
                    groups.remove(column)
                unit_length = len(value)
                if make_query.OR in value:
                    unit_length = len(value.split(make_query.OR)[0])
                colname_tmp = colname + str(unit_length)
                column_tmp = getattr(table, colname_tmp).label(colname)
                groups.append(column_tmp)
                params.append( column_tmp == value )
            elif colname in max_depths and len(value) == max_depths[colname]:
                params.append(column == value)
            else:
                raise Exception("Unexpected Parameter: Error Code 617.")

        return or_(*params)


def is_deepest(colname, val_length):
    return MAX_DEPTH[colname] == int(val_length)

def ei_filters_and_groups(table, kwargs):
    filters = []
    groups = []
    show_column = None

    for colname in kwargs:
        value = kwargs[colname]
        if value != make_query.ALL and colname in INDICES:
            column = getattr(table, colname)
            groups.append(column)
            if not value.startswith(make_query.SHOW) and not make_query.SHOW2 in value:
                filters.append(ei_parse_value(table, groups, column, colname, value, MAX_DEPTH))
            else:
                show_column = column
                if '.' in value:
                    value = value.split('.')
                    length = value[-1]
                    if "cnae_id" in colname and length > 3:
                        length = 3
                    groups.remove(column)
                    if not is_deepest(colname, length):
                        groups.append(func.substr(column, 1, length).label(column.key))
                    else:
                        groups.append(column)
                    if len(value) == 3:
                        filters.append(column.startswith(value[0]))
        elif colname == "year":
            column = getattr(table, colname)
            groups.append(column)

    return filters, groups, show_column

@mod.route('/<year>/<bra_id_s>/<cnae_id_s>/<bra_id_r>/<cnae_id_r>/<hs_id>/')
@mod.route('/<year>-<month>/<bra_id_s>/<cnae_id_s>/<bra_id_r>/<cnae_id_r>/<hs_id>/')
@gzipped
@cache_api("ei")
def ei_api(**kwargs):
    idonly = request.args.get('id', False) is not False
    limit = int(request.args.get('limit', 0)) or kwargs.pop('limit', None)
    order = request.args.get('order', None)
    sort = request.args.get('sort', 'desc')
    desired = request.args.get('desired', '')
    exclude = request.args.get('exclude', None) or kwargs.pop('exclude', None)
    serialize = request.args.get('serialize', None) or kwargs.pop('serialize', True)

    if not "month" in kwargs: kwargs["month"] = "0"

    table = make_query.select_best_table_show(kwargs, possible_tables, allowed_when_not)
    filters, groups, show_column = ei_filters_and_groups(table, kwargs)

    if exclude:
        if "," in exclude:
            exclude = exclude.split(",")
            filters.append(~show_column.in_(exclude))
        else:
            filters.append(show_column!=exclude)

    if idonly:
        results = make_query.query_table(table, [show_column, func.sum(table.purchase_value).label(table.purchase_value.key)], filters, groups=[show_column], serialize=serialize)
    else:
        desired_columns = groups + [
            func.sum(table.tax).label('tax'),
            func.sum(table.icms_tax).label('icms_tax'),
            func.sum(table.purchase_value).label('purchase_value')
        ]
        if desired:
            dcols = desired.split(",")
            for col in dcols:
                desired_columns.append( func.sum(getattr(table, col)).label(col) )
        results = make_query.query_table(table, columns=desired_columns, filters=filters, groups=groups, limit=limit, order=order, sort=sort, serialize=serialize)

    if serialize:
        return jsonify(results)
    return results
