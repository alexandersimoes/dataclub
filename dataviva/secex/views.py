import re, operator
from flask import Blueprint, request, jsonify
from dataviva.secex.models import Ymb, Ymw, Ymp, Ymbw, Ymbp, Ympw, Ymbpw
from dataviva.utils import make_query
from dataviva.utils.gzip_data import gzipped
from dataviva.utils.decorators import cache_api
from sqlalchemy import func, or_

mod = Blueprint('secex', __name__, url_prefix='/secex')

possible_tables = {
    "bra_id" : [Ymb, Ymbw, Ymbp, Ymbpw],
    "hs_id" : [Ymp, Ympw, Ymbp, Ymbpw],
    "wld_id" : [Ymw, Ympw, Ymbw, Ymbpw],
    "no_show" : [Ymb, Ymp, Ymw, Ymbp, Ympw, Ymbw, Ymbpw],
    "year" : [Ymb, Ymp, Ymw, Ymbp, Ympw, Ymbw, Ymbpw],
}

allowed_when_not = {
    Ymb : set(["hs_id", "wld_id"]),
    Ymw : set(["bra_id", "hs_id"]),
    Ymp : set(["bra_id", "wld_id"]),
    Ymbw : set(["hs_id"]),
    Ymbp : set(["wld_id"]),
    Ympw : set(["bra_id"]),
    Ymbpw: set()
}

@mod.route('/<year>-<month>/<bra_id>/<hs_id>/<wld_id>/')
@mod.route('/<year>/<bra_id>/<hs_id>/<wld_id>/')
@gzipped
@cache_api("secex")
def secex_api(**kwargs):
    idonly = request.args.get('id', False) is not False
    limit = int(kwargs.pop('limit', 0)) or int(request.args.get('limit', 0) )
    order = request.args.get('order', None) or kwargs.pop('order', None)
    sort = request.args.get('sort', None) or kwargs.pop('sort', 'desc')
    zeros = request.args.get('zeros', False) or kwargs.pop('zeros', False)
    serialize = request.args.get('serialize', None) or kwargs.pop('serialize', True)
    exclude = request.args.get('exclude', None) or kwargs.pop('exclude', None)

    if not "month" in kwargs: kwargs["month"] = "all"
        
    table = make_query.select_best_table_show(kwargs, possible_tables, allowed_when_not)
    filters, groups, show_column = make_query.build_filters_and_groups(table, kwargs)


    if exclude:
        if "," in exclude:
            exclude = exclude.split(",")
            filters.append(~show_column.in_(exclude))
        else:
            filters.append(show_column!=exclude)

    if idonly:
        filters.append(table.export_val > 0)
        results = make_query.query_table(table, columns=[show_column, func.sum(table.export_val).label(table.export_val.key)], filters=filters, groups=[show_column], serialize=serialize)
    else:
        if not zeros:
            if not order or ("export_val" not in order and "import_val" not in order):
                filters.append(or_(table.export_val != None, table.import_val != None))
        results = make_query.query_table(table, filters=filters, groups=groups, limit=limit, order=order, sort=sort, serialize=serialize)

    if serialize:
        return jsonify(results)
    return results
