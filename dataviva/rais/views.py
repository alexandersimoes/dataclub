from flask import Blueprint, request, jsonify
from dataviva.rais.models import Yb, Yi, Yo, Ybi, Ybo, Yio, Ybio, Ybi_Lg
from dataviva.rais.d_models import Ybiod, Yiod, Ybid, Ybod, Yid, Yod, Ybd
from dataviva import db
from dataviva import __data_years__ as possible_years
from dataviva.utils import make_query
from dataviva.utils.gzip_data import gzipped
from dataviva.utils.decorators import cache_api
from sqlalchemy import func, and_, or_

from dataviva.stats.util import compute_allowed


mod = Blueprint('rais', __name__, url_prefix='/rais')

allowed_when_not = compute_allowed({
    Yi : set(),
    Yb : set(),
    Yo : set(),
    Ybi : set(),
    Ybo : set(),
    Yio : set(),
    Ybio: set(),
    Ybid: set(),
    Ybod: set(),
    Yiod: set(),
    Ybiod: set(),
    Ybd: set(),
    Yid: set(),
    Yod: set(),
})

possible_tables = {
    "bra_id" : [Yb, Ybi, Ybo, Ybio, Ybiod],
    "cnae_id" : [Yi, Ybi, Yio, Ybio, Yiod, Ybiod],
    "cbo_id" : [Yo, Ybo, Ybod, Yio, Ybio, Yiod, Ybiod],
    "d_id" : [Yod, Yid, Ybd, Ybod, Ybid, Yiod, Ybiod],
    "no_show" : [Yb, Yi, Yo, Ybi, Ybo, Yio, Yod, Yid, Ybd, Ybod, Ybid, Ybio, Yiod, Ybiod]
}

demo_map = {
    "gender" : ["A", "B"],
    "ethnicity" : ["C", "D", "E", "F", "G", "H"],
    "age" : ["1", "2", "3", "4", "5", "6"],
    "literacy" : ["I", "J", "K", "L", "M"]
}

@mod.route('/<year>/<bra_id>/<cnae_id>/<cbo_id>/')
@mod.route('/<year>/<bra_id>/<cnae_id>/<cbo_id>/<d_id>/')
@gzipped
@cache_api("rais")
def rais_api(**kwargs):
    idonly = request.args.get('id', False) is not False
    limit = int(request.args.get('limit', 0) or kwargs.pop('limit', 0))
    order = request.args.get('order', None) or kwargs.pop('order', None)
    sort = request.args.get('sort', None) or kwargs.pop('sort', 'desc')
    zeros = request.args.get('zeros', False) or kwargs.pop('zeros', False)
    serialize = request.args.get('serialize', None) or kwargs.pop('serialize', True)
    exclude = request.args.get('exclude', None) or kwargs.pop('exclude', None)

    table = make_query.select_best_table_show(kwargs, possible_tables, allowed_when_not)

    if zeros and table == Ybi:
        table = Ybi_Lg 

    d_id = kwargs.pop("d_id", None)
    if d_id and "show." in d_id:
        d_id = d_id.replace("show.", "")

    num_years = len(range(*possible_years["rais"])) if kwargs.get("year", None) == "all" else 1;
    limit = limit * num_years

    filters, groups, show_column = make_query.build_filters_and_groups(table, kwargs)
    if d_id and d_id != "all":
        demo_filter = demo_map.get(d_id, [d_id])
        filters.append(table.d_id.in_(demo_filter))
        groups += [table.d_id]
        show_column = table.d_id

    if exclude:
        if "," in exclude:
            exclude = exclude.split(",")
            filters.append(~show_column.in_(exclude))
        else:
            filters.append(show_column!=exclude)

    if order and d_id and d_id != "all" and kwargs.get("cbo_id", "all") != "all":
        gender = None
        having = None
        if "." in order:
            order, gender = order.split(".")

        temp_groups = list(groups)
        temp_groups.remove(table.d_id)
        if gender:
            wanted_gender = func.sum(func.IF(table.d_id==gender, getattr(table, "num_emp"), 0)).label('wanted_gender')
            unwanted_gender = func.sum(func.IF(table.d_id!=gender, getattr(table, "num_emp"), 0)).label('unwanted_gender')
            cols = [table.cbo_id,
                    func.exp(func.sum(func.IF(table.d_id==gender, func.ln(getattr(table, order)), -func.ln(getattr(table, order))))).label(order),
                    wanted_gender,unwanted_gender]
            having = [and_(wanted_gender>10, unwanted_gender>10)]
            uniqs_col = table.cbo_id
            # filters.append(table.num_emp >= 10)
        else:
            uniqs_col = table.cnae_id if "show" in kwargs.get("cnae_id", "all") else table.cbo_id
            cols = [uniqs_col, func.sum(getattr(table, order)).label(order)]
        res = make_query.query_table(table=table, columns=cols, filters=filters+[table.num_emp>=10], groups=temp_groups, limit=limit, order=order, sort=sort, having=having)

        filtered_items = [row[0] for row in res["data"]]

        order = None
        limit = limit * len(demo_filter)

        filters.append(uniqs_col.in_(filtered_items))

    if idonly:
        filters.append(table.num_emp > 0)
        results = make_query.query_table(table, columns=[show_column, func.sum(table.num_emp).label(table.num_emp.key)], filters=filters, groups=[show_column], serialize=serialize)
    else:
        if zeros:
            filters.append(and_(table.wage != None, table.wage > 0))
        results = make_query.query_table(table=table, filters=filters, groups=groups, limit=limit, order=order, sort=sort, serialize=serialize)
    # raise Exception(table, groups)
    if serialize:
        return jsonify(results)
    return results
