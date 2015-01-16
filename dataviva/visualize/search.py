# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, jsonify, request
from dataviva.visualize.build_list import buildList
from dataviva.profile.get_list import profileList

mod = Blueprint('search', __name__, url_prefix='/search')

@mod.route('/')
def search():
    g.page_type = "visualize"
    return render_template("visualize/search.html")

@mod.route('/results/')
def results():
    kwargs = {x[0]:x[1] for x in request.args.items()}
    filters = len(kwargs)
    builds = [b.serialize() for b in buildList(kwargs)]
    profiles = [p.serialize() for p in profileList(kwargs)]
    if filters > 0:
        builds = sorted(builds, key = lambda b: (b["completion"], len(b["filter_types"])), reverse=True)
        profiles = sorted(profiles, key = lambda p: (p["completion"], p["type"]), reverse=True)
    return jsonify(builds = builds, profiles = profiles)
