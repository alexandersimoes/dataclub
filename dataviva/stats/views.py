# views.py
from dataviva import db, lm
from dataviva.utils.exist_or_404 import exist_or_404
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, jsonify, abort, current_app
from dataviva.stats.helper import compute_stats, stats_list, recent_profile_pages, top_occupations, percapita_exports
from dataviva.stats.helper import cbo_demographic_breakdown, hedu_demographic_breakdown, CAROSEL_NS
from dataviva.profile.profiles import *
from dataviva import view_cache
from dataviva.utils.cached_query import make_cache_key
from dataviva.account.views import get_userid
from flask.ext.babel import get_locale
from dataviva.utils.gzip_data import gzipped
from dataviva.profile.profiles import CboProfile
from dataviva.profile.profiles import BraProfile
from dataviva.profile.profiles import Course_heduProfile

from dataviva.stats.cache import profile_cache_serialized

import json

mod = Blueprint('stats', __name__, url_prefix='/stats')



def make_cache_key(*args, **kwargs):
    path = request.path
    args = str(hash(frozenset(request.args.items())))
    lang = str(get_locale())
    return CAROSEL_NS + (path + args + lang).encode('utf-8')


@mod.route('/rais/cbo/d/')
@gzipped
def rais_stats(**kwargs):
    limit = int(request.args.get('limit', 10) or kwargs.pop('limit', 10))
    offset = int(request.args.get('offset', 0) or kwargs.pop('offset', 0))
    d_id = request.args.get('d_id', 'A') or kwargs.pop('d_id', 'A')
    year = 2013
    
    cbo_id_len = 4
    
    data = cbo_demographic_breakdown(year, d_id, cbo_id_len, limit=limit, offset=offset)
    items = [profile_cache_serialized(CboProfile, attr) for attr in data]
    
    return json.dumps(items)

@mod.route('/hedu/course_hedu/d/')
@gzipped
def hedu_stats(**kwargs):
    limit = int(request.args.get('limit', 10) or kwargs.pop('limit', 10))
    offset = int(request.args.get('offset', 0) or kwargs.pop('offset', 0))
    d_id = request.args.get('d_id', 'A') or kwargs.pop('d_id', 'A')
    year = 2012
    
    course_hedu_id_len = 6
    
    data = hedu_demographic_breakdown(year, d_id, course_hedu_id_len, limit=limit, offset=offset)
    items = [Course_heduProfile(attr).serialize() for attr in data]
    
    return json.dumps(items)

@mod.route('/secex/percapita/')
@gzipped
def secex_stats(**kwargs):
    limit = int(request.args.get('limit', 10) or kwargs.pop('limit', 10))
    offset = int(request.args.get('offset', 0) or kwargs.pop('offset', 0))

    year = 2013
    month = 0
    bra_id_len = 9

    cities = percapita_exports(year=year, month=month, bra_id_len=bra_id_len, limit=limit, offset=offset)
    items = [profile_cache_serialized(BraProfile, bra) for bra in cities]
    return json.dumps(items)


@mod.route('/compute/')
def compute():
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    depth = request.args.get('depth', None)
    sort = request.args.get('sort', 'desc')

    metric = request.args.get('metric', None) # what we're looking at
    show = request.args.get('show', '')
    shows = show.split(",")
    data = compute_stats(metric, shows, limit=limit, offset=offset, depth=depth, sort=sort)
    return jsonify(data)

@mod.route('/carosel/')
@view_cache.cached(timeout=604800, key_prefix=make_cache_key)
def carosel():
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    depth = request.args.get('depth', None)
    sort = request.args.get('sort', 'desc')
    profile = request.args.get('profile', None)

    metric = request.args.get('metric', None) # what we're looking at
    show = request.args.get('show', '')
    shows = show.split(",")

    data = stats_list(metric, shows, limit=limit, offset=offset, sort=sort, depth=depth, listify=True)
    profile_model = globals()[profile]
    items = [profile_model(*attr).serialize() for attr in data]
    
    return json.dumps(items)

@mod.route('/recent/pages/')
def recent_pages():
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    sort = request.args.get('sort', 'desc')

    uid = get_userid()

    data = recent_profile_pages(uid, limit=limit, sort=sort, offset=offset) 
    
    results = [item for item in data]
    return json.dumps(results)

@mod.route("/raisd/occupations/<year>/<bra_id>")
def top_occ(year, bra_id):
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    sort = request.args.get('sort', 'desc')

    results = top_occupations(year, bra_id)
    return json.dumps(results)