from flask import Blueprint, request, g, jsonify
from dataviva import db
from dataviva.sc.models import Yb, Ybd, Yd, Ybs, Ybc, Yc, Ys, Ybcd
from dataviva.utils.gzip_data import gzipped
from sqlalchemy import func, distinct, desc
from dataviva.utils import make_query
from dataviva.utils.decorators import cache_api

mod = Blueprint('sc', __name__, url_prefix='/sc')

possible_tables = {
    "bra_id" : [Ybc, Ybd, Ybs, Ybcd],
    "d_id" : [Yd, Ybd, Ybcd],
    "school_id" : [Ybs],
    "course_sc_id" : [Yc, Ybc, Ybcd],
    "no_show" : [Yb, Yd, Yc, Ys, Ybd, Ybs, Ybc, Ybcd]
}

allowed_when_not = {
    Yb : set(["d_id", "school_id", "course_sc_id"]),
    Yd : set(["bra_id", "school_id", "course_sc_id"]),
    Yc: set(["d_id", "bra_id", "school_id"]),
    Ys: set(["d_id", "bra_id", "course_sc_id"]),
    Ybs : set(["d_id", "course_sc_id"]),
    Ybd: set(["school_id", "course_sc_id"]),
    Ybc: set(["school_id", "d_id"]),
    Ybcd: set(["school_id"]),
}

demo_map = {
    "gender" : ["A", "B"],
    "ethnicity" : ["C", "D", "E", "F", "G", "H"],
    "loc" : ["N", "O"],
    "school_type" : ["P", "Q", "R", "S", "T", "U"]
}


@mod.route('/<year>/<bra_id>/<school_id>/<course_sc_id>/<d_id>/')
@gzipped
@cache_api("sc")
def sc_api(**kwargs):
    idonly = request.args.get('id', False) is not False
    limit = int(request.args.get('limit', 0) or kwargs.pop('limit', 0))
    order = request.args.get('order', None) or kwargs.pop('order', None)
    sort = request.args.get('sort', None) or kwargs.pop('sort', 'desc')
    serialize = request.args.get('serialize', None) or kwargs.pop('serialize', True)
    exclude = request.args.get('exclude', None) or kwargs.pop('exclude', None)

    table = make_query.select_best_table_show(kwargs, possible_tables, allowed_when_not)
    d_id = kwargs.pop("d_id", None)
    if not table:
        raise Exception("Missing Table for this query")

    filters, groups, show_column = make_query.build_filters_and_groups(table, kwargs)
    demo_filter = demo_map.get(d_id)
    if demo_filter:
        filters.append(table.d_id.in_(demo_filter))
        groups += [table.d_id]

    if exclude:
        if "," in exclude:
            exclude = exclude.split(",")
            filters.append(~show_column.in_(exclude))
        else:
            filters.append(show_column!=exclude)

    if idonly:
        results = make_query.query_table(table, columns=[show_column], filters=filters, groups=[show_column])
    else:
        # desired = [g for g in groups]
        # desired += [table.enrolled, table.age, table.classes]
        # if table == Yb:
        #     desired += [table.num_schools]
        # if show_column:
        #     if not show_column in desired:
        #         desired.append(show_column)
        # if focus:
        #     focus_filter = table.d_id.in_(focus_map[focus])
        #     filters.append(focus_filter)
        # results = make_query.query_table(table, columns=desired, filters=filters, groups=groups, limit=limit, order=order, sort=sort, serialize=serialize)
        groups = []
        # raise Exception(filters[4])
        results = make_query.query_table(table, filters=filters, groups=groups, limit=limit, order=order, sort=sort, serialize=serialize)

    if serialize:
        return jsonify(results)
    return results
