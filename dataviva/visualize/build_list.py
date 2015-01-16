import copy, itertools, re
from dataviva.visualize.build_models import *

def buildList(buildOpts = {}):

    attrs  = {}
    opts   = {}
    builds = []

    for data_type, url in url_formats.iteritems():
        placeholders = re.findall("<(\w+)>", url)
        placeholders.remove("app")
        placeholders.remove("year")
        for a in placeholders:
            if a not in opts:
                opts[a] = "<{0}>".format(a) if a not in buildOpts else buildOpts[a]
        attrs[data_type] = placeholders

    def getOpts(keys):
        obj = {}
        for key in keys:
            obj[key] = opts[key]
        return obj

    def everyCombo(build, dataset, outputs = None):

        keys = attrs[dataset]
        bras = [k for k in keys if "bra" in k]

        if not outputs:
            outputs = keys
        elif type(outputs) == str:
            outputs = [outputs]

        for output in outputs:
            slim = copy.copy(keys)

            if output in slim:
                slim.remove(output)

            for b in bras:
                if b in slim:
                    slim.remove(b)

            builds.append(build(dataset, getOpts(bras), output))

            for i in range(0, len(slim)):
                for combo in itertools.combinations(slim, i + 1):
                    filters = bras + list(combo)
                    builds.append(build(dataset, getOpts(filters), output))

    # SECEX Builds
    everyCombo(TreeMap, "secex")
    everyCombo(Stacked, "secex")
    everyCombo(GeoMap, "secex", "bra")

    builds.append(Scatter("secex", getOpts(["bra"]), "hs"))

    builds.append(Compare("secex", getOpts(["bra"]), "hs"))
    builds.append(Compare("secex", getOpts(["bra","wld"]), "hs"))
    builds.append(Compare("secex", getOpts(["bra"]), "wld"))
    builds.append(Compare("secex", getOpts(["bra","hs"]), "wld"))

    builds.append(Network("secex", getOpts(["bra"]), "hs"))

    builds.append(Rings("secex", getOpts(["bra"]), "hs", focus = opts["hs"]))

    # RAIS Builds
    everyCombo(TreeMap, "rais")
    everyCombo(Stacked, "rais")
    everyCombo(GeoMap, "secex", "bra")

    builds.append(Scatter("rais", getOpts(["bra"]), "cnae"))

    builds.append(Compare("rais", getOpts(["bra"]), "cnae"))
    builds.append(Compare("rais", getOpts(["bra","cbo"]), "cnae"))
    builds.append(Compare("rais", getOpts(["bra"]), "cbo"))
    builds.append(Compare("rais", getOpts(["bra","cnae"]), "cbo"))

    builds.append(Network("rais", getOpts(["bra"]), "cnae"))

    builds.append(Rings("rais", getOpts(["bra"]), "cbo", focus = opts["cbo"]))
    builds.append(Rings("rais", getOpts(["bra"]), "cnae", focus = opts["cnae"]))

    builds.append(Occugrid("rais", getOpts(["bra","cnae"]), "cbo"))

    # EI Builds
    everyCombo(TreeMap, "ei")

    return builds



  # builds = {}
  #
  # builds["rais"] = [
  #   {
  #     "description": {
  #       "attrs": ["4110","5211","7170"],
  #       "prefix": "The top 3 occupations employed by <bra> are ",
  #       "type": "cbo"
  #     },
  #     "filters": ["bra"],
  #     "title": gettext("Employment Ranking"),
  #     "apps": ["bar"],
  #     "url": "/show.2/all/all/"
  #   },
  # ]
  #
  # builds["attrs"] = [
  #   {
  #     "title": gettext("Population Ranking"),
  #     "apps": ["bar"],
  #     "url": "/?value=pop"
  #   },
  #   {
  #     "title": gettext("GDP Ranking"),
  #     "apps": ["bar"],
  #     "url": "/?value=gdp"
  #   }
  # ]
  #
  # builds["secex"] = [
  #   {
  #     "description": {
  #       "attrs": ["052601","020901","157202"],
  #       "prefix": "The top 3 products exported by <bra> are ",
  #       "type": "hs"
  #     },
  #     "filters": ["bra"],
  #     "title": gettext("Trade Ranking"),
  #     "apps": ["bar"],
  #     "url": "/show.2/all/all/"
  #   }
  # ]
  #
  # builds["ei"] = [
  #   {
  #     "filters": ["bra"],
  #     "title": gettext("Tax Ranking"),
  #     "apps": ["bar"],
  #     "url": "/show.2/all/all/all/all/"
  #   },
  #   {
  #     "apps": ["tree_map","stacked"],
  #     "title": gettext("Products sold by the <cnae> Industry in <bra> to the <cnae> Industry in <bra>"),
  #     "url": "/<bra>/<cnae>/<bra2>/<cnae2>/show.6/"
  #   }
  # ]
  #
  # builds["edu"] = [
  #   {
  #     "filters": ["bra"],
  #     "title": gettext("Enrollment Ranking"),
  #     "apps": ["bar"],
  #     "url": "/show.2/all/all/"
  #   }
  # ]
  #
  # finalList = {}
  # urls = []
  # for dataset, b in builds.iteritems():
  #   for build in b:
  #     for app in build["apps"]:
  #       newBuild = copy.copy(build)
  #       newBuild["type"] = app
  #       newBuild["url"] = "/{0}/{1}/<year>{2}".format(app,dataset,build["url"])
  #       newBuild["dataset"] = dataset
  #       finalList[newBuild["url"]] = newBuild
  #
  # if requestedBuild:
  #   return finalList[requestedBuild] if requestedBuild in finalList else False
  # else:
  #   return finalList
