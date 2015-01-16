# -*- coding: utf-8 -*-
from ei import title as ei_title
from hedu import title as hedu_title
from rais import title as rais_title
from sc import title as sc_title
from secex import title as secex_title

def build_title(build):

    args = {
        "demo": build.demo,
        "display_attr": build.display_attr,
        "display_key": build.display_key,
        "filters": build.filter_attrs,
        "limit": build.limit,
        "order": build.order,
        "size": None,
        "split": None
    }

    if "size" in build.config:
        args["size"] = build.config["size"]
    elif args["order"]:
        args["size"] = args["order"].split(".")[0]
    elif "y" in build.config:
        args["size"] = build.config["y"]

    if "split" in build.config:
        args["split"] = build.config["split"]

    return globals()["{}_title".format(build.data_type)](args)
