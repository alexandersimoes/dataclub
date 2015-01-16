# -*- coding: utf-8 -*-
import json
from flask import Blueprint, redirect, render_template, g, url_for
from dataviva.visualize.views import *

mod = Blueprint('embed', __name__, url_prefix='/embed')

@mod.before_request
def before_request():
    g.page_type = mod.name

@mod.route("/")
def index():
  return redirect(url_for("embed", app="tree_map", data="secex", year="2013", bra="mg", hs="show.6", wld="all"))

class EmbedView(Visualize):

  def dispatch(self, build, **kwargs):
      return render_template("visualize/embed.html", build = build, buildJS = json.dumps(build.serialize()))

dataRoutes(mod, EmbedView, "embed")
