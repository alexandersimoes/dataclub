import copy
from flask import request
from flask.views import View
from dataviva.visualize.build_list import buildList, url_formats
from dataviva.visualize.build_models import *

class Visualize(View):

    def dispatch(self, build, opts={}):
        raise Exception(build)

    def dispatch_request(self, app, data, year, **kwargs):

        app    = globals()["".join([a.title() for a in app.split("_")])]
        opts   = {}
        output = None

        for key, value in kwargs.iteritems():
            v = value.split(".")
            if v[0] != "all":
                v = v[0]
                if v != "show":
                    opts[key] = v
                if "show" in value:
                    output = key

        params = dict(request.args)
        for key, value in params.iteritems():
            params[key] = value[0]
        build = app(data, opts, output, year=year, **params)

        returnOpts = copy.copy(opts)
        focus = request.args.get("focus", None)
        if focus:
            returnOpts[output] = build.focus

        return self.dispatch(build, opts=returnOpts)

def dataRoutes(bp, view, endpoint):
    view_func = view.as_view(endpoint)
    for data, url in url_formats.iteritems():
        bp.add_url_rule(url, defaults={"data": data}, view_func=view_func)
