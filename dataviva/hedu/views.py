from flask import Blueprint, request, g, jsonify
from dataviva import db
import dataviva.hedu.models as hedu
from dataviva.utils.gzip_data import gzipped
from sqlalchemy import func, distinct, desc
from dataviva.utils import make_query
from dataviva.utils.decorators import cache_api

mod = Blueprint('hedu', __name__, url_prefix='/hedu')


possible_tables = {
    "bra_id" : [hedu.Yb_hedu, hedu.Ybu, hedu.Ybc, hedu.Ybd, hedu.Ybuc, hedu.Ybcd, hedu.Ybud, hedu.Ybucd],
    "university_id" : [hedu.Yu, hedu.Ybu, hedu.Yuc, hedu.Yud, hedu.Ybuc, hedu.Yucd, hedu.Ybud, hedu.Ybucd],
    "course_hedu_id" : [hedu.Yc, hedu.Ybc, hedu.Yuc, hedu.Ycd, hedu.Yucd, hedu.Ybuc, hedu.Ybcd, hedu.Ybucd],
    "d_id" : [hedu.Yd, hedu.Ybd, hedu.Yud, hedu.Ycd, hedu.Yucd, hedu.Ybcd, hedu.Ybud, hedu.Ybucd],
    "no_show" : [hedu.Yb_hedu, hedu.Yc, hedu.Yd, hedu.Yu, hedu.Yuc, hedu.Yud, hedu.Ybu, hedu.Ybc, hedu.Ycd, hedu.Yucd, hedu.Ybud, hedu.Ybuc, hedu.Ybcd, hedu.Ybucd]
}

allowed_when_not = {
    hedu.Yb_hedu : set(["d_id", "course_hedu_id", "university_id"]),
    hedu.Yd : set(["bra_id", "course_hedu_id", "university_id"]),
    hedu.Yc : set(["bra_id", "d_id", "university_id"]),
    hedu.Yu : set(["bra_id", "d_id", "course_hedu_id"]),
    hedu.Ybc : set(["d_id", "university_id"]),
    hedu.Ybd : set(["course_hedu_id", "university_id"]),
    hedu.Ybu : set(["course_hedu_id", "d_id"]),
    hedu.Yuc : set(["bra_id", "d_id"]),
    hedu.Yud : set(["bra_id", "course_hedu_id"]),
    hedu.Ycd : set(["bra_id", "university_id"]),
    hedu.Ybud : set(["course_hedu_id"]),
    hedu.Ybcd : set(["university_id"]),
    hedu.Yucd : set(["bra_id"]),
    hedu.Ybuc : set(["d_id"]),
    hedu.Ybucd : set([])
}

demo_map = {
    "gender" : ["A", "B"],
    "ethnicity" : ["C", "D", "E", "F", "G", "H"],
    "school_type" : ["P", "Q", "R", "S", "T", "U"]
}

@mod.route('/<year>/<bra_id>/<university_id>/<course_hedu_id>/<d_id>/')
@gzipped
# @cache_api("hedu")
def hedu_api(**kwargs):
    idonly = request.args.get('id', False) is not False
    limit = int(request.args.get('limit', 0) or kwargs.pop('limit', 0))
    order = request.args.get('order', None) or kwargs.pop('order', None)
    order_col = order
    sort = request.args.get('sort', None) or kwargs.pop('sort', 'desc')
    serialize = request.args.get('serialize', None) or kwargs.pop('serialize', True)
    exclude = request.args.get('exclude', None) or kwargs.pop('exclude', None)

    if "university_id" in kwargs:
        # -- there is no nesting for university ids
        kwargs["university_id"] = kwargs["university_id"].replace("show.5", "show")

    table = make_query.select_best_table_show(kwargs, possible_tables, allowed_when_not)
    if not table:
        raise Exception("Missing Table for this query")

    d_id = kwargs.pop("d_id", None)
    if d_id and "show." in d_id:
        d_id = d_id.replace("show.", "")

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

    if order and d_id and d_id != "all" and kwargs.get("course_hedu_id", "all") != "all":
        gender = None
        if "." in order:
            order, gender = order.split(".")

        temp_groups = list(groups)
        temp_groups.remove(table.d_id)
        if gender:
            cols = [table.course_hedu_id, func.exp(func.sum(func.IF(table.d_id==gender, func.ln(getattr(table, order)), -func.ln(getattr(table, order))))).label(order)]
        else:
            cols = [table.course_hedu_id, func.sum(getattr(table, order)).label(order)]
        res = make_query.query_table(table=table, columns=cols, filters=filters, groups=temp_groups, limit=limit, order=order, sort=sort)

        filtered_ids = [row[0] for row in res["data"]]

        order_col = None
        limit = limit * len(demo_filter)

        filters.append(table.course_hedu_id.in_(filtered_ids))

    if idonly:
        results = make_query.query_table(table, columns=[show_column], filters=filters, groups=[show_column], serialize=serialize)
    else:
        desired = [g for g in groups]
        # desired += fixed_fields
        if show_column:
            if not show_column in desired:
                desired.append(show_column)
        groups = [] # no group by for this table...
        # if focus:
        #     focus_filter = table.d_id.in_(focus_map[focus])
        #     filters.append(focus_filter)
        results = make_query.query_table(table, filters=filters, groups=groups, limit=limit, order=order_col, sort=sort, serialize=serialize)
        # results = make_query.query_table(table, columns=desired, filters=filters, groups=groups, limit=limit, order=order, sort=sort, serialize=serialize)

    if order and "growth" not in order:
        if serialize:
            col_index = results["headers"].index(order)
            results["data"] = [d for d in results["data"] if d[col_index] > 0]
        else:
            results = [d for d in results if d[order] > 0]

    if serialize:
        return jsonify(results)
    return results
