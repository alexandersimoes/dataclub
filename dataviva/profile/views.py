# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, render_template, g, url_for, redirect, request
from dataviva.profile.profiles import *
from dataviva.profile import get_list
from dataviva import view_cache
from dataviva.utils.decorators import cache_api

import json

mod = Blueprint('profile', __name__, url_prefix='/profile')

@mod.before_request
def before_request():
    g.page_type = mod.name

@mod.route("/")
def list():
    if request.is_xhr:
        return jsonify(profiles = [p.serialize() for p in get_list()])
    else:
        return redirect(url_for("general.home"))



@mod.route("/<loc>/")
@mod.route("/<loc>/<loc_id>/")
@mod.route("/<loc>/<loc_id>/<attr>/")
@mod.route("/<loc>/<loc_id>/<attr>/<attr_id>/")
@cache_api("profile_pages")
# @view_cache.cached(key_prefix='profile-cache/%s')
def bra_cbo(loc, loc_id = "all", attr = None, attr_id = None):

    if attr:
        profile = globals()["{0}Profile".format(attr.capitalize())]
    else:
        profile = globals()["{0}Profile".format(loc.capitalize())]

    if attr_id:
        if loc_id != "sabra":
            profile = profile(attr_id, loc_id)
        else:
            profile = profile(attr_id)
    else:
        if loc_id != "sabra":
            profile = profile(loc_id)
        else:
            profile = profile()

    builds = []
    sections = profile.sections()
    for section in sections:
        parseBuilds(section, builds)

    debug = request.args.get('debug', False)
    if debug:
        if debug == True:
            i = 0
        else:
            i = int(debug)
        raise Exception(builds[i].title(), builds[i].url(), builds[i].limit, builds[i].demo, builds[i].config)

    builds = [b.serialize() for b in builds]

    return render_template("profile/index.html", sections=sections, profile = profile, builds = json.dumps(builds))

def parseBuilds(section, builds):
    if "builds" in section:
        builds += section["builds"]
    if "sections" in section:
        for s in section["sections"]:
            parseBuilds(s, builds)
