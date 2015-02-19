import pickle

from dataviva.utils import make_query
from dataviva.stats.util import compute_allowed

from dataviva.utils.cached_query import cached_query
from dataviva.stats.cache import object_cache

from dataviva import db

import dataviva.ei.models as ei
import dataviva.secex.models as secex
import dataviva.rais.models as rais
import dataviva.rais.d_models as raisd

import dataviva.rais.d_models as raisd
import dataviva.hedu.models as hedu
import dataviva.attrs.models as attrs
import dataviva.account.models as account
from dataviva.profile.get_list import parseProfileString
from dataviva import __data_years__
from sqlalchemy import func
from sqlalchemy import desc, asc

from dataviva.stats.cache import profile_cache_serialized
from dataviva.stats.util import gen_table_list


possible_tables = {
    "hs_id" : [secex.Ymp, ei.Ymp, secex.Ymbp],
    "cnae_id_r" : [ei.Ymr],
    "bra_id_r" : [ei.Ymr],
    "cnae_id_s" : [ei.Yms],
    "bra_id_s" : [ei.Yms],
    "bra_id" : [secex.Ymb, rais.Yb, hedu.Yb_hedu, hedu.Ybu, secex.Ymbp, attrs.Bra_stats],
    "wld_id" : [secex.Ymw],
    "cnae_id" : [rais.Yi],
    "cbo_id" : [rais.Yo],
    "university_id" : [hedu.Yu],
    "course_hedu_id" : [hedu.Yc],
}

allowed_when_not = compute_allowed(gen_table_list(possible_tables))

max_depth = {
    "bra_id": 9,
    "course_hedu_id": 6,
    "cnae_id": 6,
    "cbo_id": 4,
    "hs_id": 6,
    "wld_id": 5,
}

no_length_column = { attrs.Bra_stats: 9 }
CAROSEL_NS = "carosel:"

filters_map = {
    secex.Ymbp : [secex.Ymbp.year == __data_years__['secex'][-1], secex.Ymbp.month == 0],
    secex.Ymw : [secex.Ymw.year == __data_years__['secex'][-1], secex.Ymw.month == 0],
    secex.Ymb : [secex.Ymb.year == __data_years__['secex'][-1], secex.Ymb.month == 0],
    secex.Ymp : [secex.Ymp.year == __data_years__['secex'][-1], secex.Ymp.month == 0],
    rais.Yb : [rais.Yb.year == __data_years__['rais'][-1]],
    rais.Yi : [rais.Yi.year == __data_years__['rais'][-1]],
    rais.Yo : [rais.Yo.year == __data_years__['rais'][-1]],
    hedu.Ybu : [hedu.Ybu.year == __data_years__['hedu'][-1], hedu.Ybu.bra_id != '0xx000007'],
    hedu.Yu : [hedu.Yu.year == __data_years__['hedu'][-1]],
    hedu.Yb_hedu : [hedu.Yb_hedu.year == __data_years__['hedu'][-1], hedu.Yb_hedu.bra_id != '0xx000007'],
    hedu.Yc : [hedu.Yc.year == __data_years__['hedu'][-1]],
}

def make_key(*args, **kwargs):
    return str(kwargs)

def stats_list(metric, shows, limit=None, offset=None, sort="desc", depth=None, listify=False):
    if type(shows) is str:
        shows = [shows]
    raw = compute_stats(metric, shows, limit=limit, offset=offset, sort=sort, depth=depth)
    # assumes there is only 1 metric possible and it is last column
    if len(shows) > 1 or listify:
        return [x[:-1] for x in raw["data"]]
    return [x[0] for x in raw["data"]]


def compute_stats(metric, shows, limit=None, offset=None, sort="desc", depth=None, filters=[]):
    cache_key = CAROSEL_NS + "".join(([metric] + shows) + ([str(limit), str(offset),sort,str(depth)]))
    prev = cached_query(cache_key)
    if prev:
        return pickle.loads(prev)
    # -- TODO cache the queries, cleanup
    kwargs = {metric:"dummy"}
    kwargs[shows[0]] = 'show'
    for show in shows[1:]:
        kwargs[show] = "dummy"

    table = make_query.select_best_table_show(kwargs, possible_tables, allowed_when_not)

    if not table:
        raise Exception("No Valid Table Available!")

    filters = []

    show_columns = [getattr(table, show) for show in shows]
    metric_col = getattr(table, metric)
    i = 0
    for show_column in show_columns:
        show=shows[i]
        if table in no_length_column:
            depth_val = depth or max_depth[show]
            filters.append(func.char_length(show_column) == depth_val )
        elif show in max_depth:
            depth_val = depth or max_depth[show]
            filters.append(getattr(table, show + make_query.LEN) == depth_val )
        i+=1

    if table in filters_map:
        filters += filters_map[table]

    columns = show_columns + [metric_col]
    results = make_query.query_table(table, columns, filters, order=metric, limit=limit, sort=sort, offset=offset)

    cached_query(cache_key, pickle.dumps(results))
    return results

def recent_profile_pages(uid, limit=10, sort="asc", offset=None):
    table = account.PageView
    raw = make_query.query_table(table, [table.page, table.timestamp], [table.user_id == uid, table.page.startswith("/profile")], order=table.timestamp, limit=limit, sort=sort, offset=offset)
    results = []
    for item in raw["data"]:
        profile, arguments = parseProfileString(item[0])
        results.append( profile_cache_serialized( profile, arguments ) )
    return results

def top_occupations(year, bra_id):
    cache_key = CAROSEL_NS + "top_occupations" + str(year) + bra_id
    prev = object_cache(cache_key)
    if prev:
        return pickle.loads(prev)

    table = rais.Ybo
    filters = [table.bra_id == bra_id, table.year == year]
    raw = make_query.query_table(table, [table.cbo_id], filters, order=table.wage_avg, limit=10, sort="desc")
    cbos = [x[0] for x in raw["data"]]
    table = raisd.Ybod
    filters = [table.bra_id == bra_id, table.year == year, table.cbo_id.in_(cbos), table.d_id.in_(["A", "B"])]
    columns = [table.cbo_id, table.d_id, table.num_emp, table.wage_avg, table.wage_growth]
    results = make_query.query_table(table, columns, filters, order=table.wage_avg)
    
    object_cache(cache_key, pickle.dumps(results))
    return results


def percapita_exports(year=2013, month=0, bra_id_len=9, limit=10, offset=0): 
    join_criteria = attrs.Bra_stats.bra_id == secex.Ymb.bra_id
    filters = [secex.Ymb.month==month, secex.Ymb.year==year, secex.Ymb.bra_id_len == bra_id_len]
    columns = [secex.Ymb.bra_id, secex.Ymb.export_val, attrs.Bra_stats.pop, (secex.Ymb.export_val / attrs.Bra_stats.pop).label("ratio")]
    params = "year=%s-month=%s-bra_id_len=%s-limit=%s-offset=%s" % (year, month, bra_id_len, limit, offset)
    data = generic_join_breakdown("secex_percapita", params, secex.Ymb, attrs.Bra_stats, join_criteria, columns, 
                                  filters=filters, order_col='ratio', limit=limit, offset=offset, col_select='bra_id')
    return data

def cbo_demographic_breakdown(year=2013, d_id='A', cbo_id_len=4, limit=10, offset=0):
    Yo = rais.Yo
    Yod = raisd.Yod

    join_criteria = Yo.cbo_id == Yod.cbo_id
    filters = [Yo.year==year, Yod.d_id == d_id, Yo.cbo_id_len == cbo_id_len, Yod.year == Yo.year, Yo.num_emp > 10]
    columns = [Yo.cbo_id, Yo.num_emp, Yod.num_emp, (Yod.num_emp / Yo.num_emp).label("ratio")]

    params = "year=%s-d_id=%s-cbo_id_len=%s-limit=%s-offset=%s" % (year, d_id, cbo_id_len, limit, offset)

    results = generic_join_breakdown("cbo_demographic_breakdown", params, Yo, Yod, join_criteria, columns, 
                                  filters=filters, order_col='ratio', limit=limit, offset=offset, col_select='cbo_id')
    return results

def hedu_demographic_breakdown(year=2012, d_id='A', course_hedu_id_len=6, limit=10, offset=0):
    Yc = hedu.Yc
    Ycd = hedu.Ycd
    
    join_criteria = Yc.course_hedu_id == Ycd.course_hedu_id
    filters = [Yc.year==year, Ycd.d_id == d_id, Yc.course_hedu_id_len == course_hedu_id_len, Ycd.year == Yc.year, Yc.enrolled > 25]
    columns = [Yc.course_hedu_id, Yc.enrolled, Ycd.enrolled, (Ycd.enrolled / Yc.enrolled).label("ratio")]

    params = "year=%s-d_id=%s-course_hedu_id_len=%s-limit=%s-offset=%s" % (year, d_id, course_hedu_id_len, limit, offset)
    results = generic_join_breakdown("hedu_demographic_breakdown", params, Yc, Ycd, join_criteria, columns, 
                                  filters=filters, order_col='ratio', limit=limit, offset=offset, col_select='course_hedu_id')
    return results

def generic_join_breakdown(namespace, params, left_table, right_table, join_criteria, columns, order_col="ratio", filters=[], 
                           limit=10, sort_order="desc", offset=0, col_select=None):

    cache_key = CAROSEL_NS + namespace + "_" + str(params)
    
    prev = object_cache(cache_key)
    if prev:
        return pickle.loads(prev) 

    order = desc(order_col) if sort_order != "asc" else asc(order_col)
    results = left_table.query.join(right_table, join_criteria) \
                            .with_entities(*columns) \
                            .filter(*filters) \
                            .order_by(order) \
                            .limit(limit) \
                            .offset(offset) \
                            .all()

    if not col_select:
        raise Exception("Please specify the column to select for results")

    results = [row.__dict__[col_select] for row in results]

    object_cache(cache_key, pickle.dumps(results))
    return results

# Based on example from http://stackoverflow.com/questions/2440826/collaborative-filtering-in-mysql
def suggested_profiles(uid, limit=10, offset=0):
    query_str = '''SELECT similar.page, sum(ub_rank.rank) total_rank
            FROM (
            SELECT similar.user_id,count(*) rank
            FROM account_pageview target
            join account_pageview similar on target.page=similar.page and target.user_id != similar.user_id
            where target.user_id = '{0}'
            group by similar.user_id

        ) ub_rank
        JOIN account_pageview similar on ub_rank.user_id = similar.user_id
        left join account_pageview target on target.user_id = '{0}' and target.page = similar.page
        where target.page is NULL
        GROUP BY similar.page
        HAVING total_rank > 1
        AND similar.page LIKE '/profile/%%'
        ORDER BY total_rank DESC
        LIMIT {1}
        OFFSET {2}
    '''.format(uid, limit, offset)
    results = db.engine.execute(query_str)
    # page_set = set([page.replace('/wld/sabra/cbo', '/cbo') for page,rank in results])
    results = [parseProfileString(page) for page,rank in results]
    results = [profile(*arguments) for (profile, arguments) in results]
    return results