# Utility functions for stats
import json

def compute_table_years(datasets):
    import dataviva.ei.models as ei
    import dataviva.secex.models as secex
    import dataviva.rais.models as rais
    import dataviva.hedu.models as hedu
    import dataviva.sc.models as sc
    tables = {"ei" : ei.Ymp, "rais": rais.Yb, "secex": secex.Ymb, "sc": sc.Yd, "hedu": hedu.Yd}
    results = {}
    for dataset in datasets:
        max_year = get_year(tables[dataset], mode='max')
        min_year = get_year(tables[dataset], mode='min')
        if dataset == "ei":
            max_year = str(max_year) + "-" + str(get_month(tables[dataset], max_year, 'max'))
            min_year = str(min_year) + "-" + str(get_month(tables[dataset], min_year, 'min'))
        results[dataset] = [min_year, max_year]
    return results

def compute_allowed(table_dict):
    master_list = set([])
    for table in table_dict:
        master_list = master_list.union(table.__table__.columns.keys())

    for table in table_dict:
        table_dict[table] = master_list.difference(table.__table__.columns.keys())
    return table_dict

def get_year(table, mode):
    if mode == 'min':
        year_col = table.year.asc()
    else:
        year_col = table.year.desc()
    return table.query.with_entities(table.year).order_by(year_col).first().year

def get_month(table, year, mode):
    if mode == 'min':
        month_col = table.month.asc()
    else:
        month_col = table.month.desc()
    return table.query.with_entities(table.month).filter_by(year=year).order_by(month_col).first().month

def get_or_set_years(redis, key):

    val = redis.get(key)
    if val:
        val = json.loads(val)
    else:
        val = compute_table_years(['ei', 'hedu', 'sc', 'secex', 'rais'])
    redis.set(key, json.dumps(val))
    return val

def gen_table_list(poss_tables):
    table_dict = {}
    for tname, tables in poss_tables.items():
        for table in tables:
            table_dict[table] = set()
    return table_dict
