# -*- coding: utf-8 -*-
import json
from flask import Blueprint, jsonify, redirect, request, render_template, url_for
from dataviva.visualize.build_list import buildList
from dataviva.visualize.views import *

mod = Blueprint('build', __name__, url_prefix='/build')

@mod.route("/")
def list():
    if request.is_xhr:
        return jsonify(builds = [b.serialize() for b in buildList()])
    else:
        return redirect(url_for("search.search"))

class BuildView(Visualize):

    def dispatch(self, build, **kwargs):

        params = request.query_string
        if params:
            url = "{0}?{1}".format(request.path,params)
        else:
            url = request.path

        opts = kwargs.get("opts")
        builds = buildList(opts)
        recs = [b for b in builds if b.url() != url and b.completion() == 1]
        image = [a.image() for k, a in opts.iteritems() if not isinstance(a, (str, unicode))]
        image = image[0] if len(image) > 0 else False

        return render_template("visualize/build.html",
            build = build,
            buildJS = json.dumps(build.serialize()),
            recs = recs,
            image = image)

dataRoutes(mod, BuildView, "build")
