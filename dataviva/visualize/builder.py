# -*- coding: utf-8 -*-
import json
from flask import Blueprint, render_template
from dataviva.visualize.views import *

mod = Blueprint('builder', __name__, url_prefix='/builder')

@mod.route("/")
def builder():
    return render_template("visualize/builder.html", buildJS = json.dumps(False))

class BuilderView(Visualize):

  def dispatch(self, build, **kwargs):
      return render_template("visualize/builder.html", build = build, buildJS = json.dumps(build.serialize()))

dataRoutes(mod, BuilderView, "builderBuild")
