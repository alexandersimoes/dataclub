# -*- coding: utf-8 -*-
import re
from flask.ext.babel import gettext
from dataviva.attrs.models import Wld
from dataviva.attrs.article import get_article

def title_format(title, attrs):

    joiner = gettext("and")

    if "<bra" in title and "bra" not in attrs:
        attrs["bra"] = Wld.query.get("sabra")

    for f, attr_list in attrs.items():

        if not isinstance(attr_list, list):
            attr_list = [attr_list]

        placeholder = "<{0}>".format(f)
        article = re.search("<{0}_article_(\w+)>".format(f), title)
        if article:
            placeholder = article.group(0)
            names = []
            for a in attr_list:
                word = get_article(a, article.group(1))
                name = get_name(a, f)
                if word:
                    names.append(u"{0} {1}".format(word, name))
                else:
                    names.append(name)
        else:
            names = [get_name(a, f) for a in attr_list]

        title = title.replace(placeholder, joiner.join(names))

    return title

def get_name(attr, attr_type):

    placeholders = {
        "hs": gettext("a product"),
        "wld": gettext("a country"),
        "cbo": gettext("an occupation"),
        "cnae": gettext("an industry"),
        "bra": gettext("a location")
    }

    strip_type = attr_type.split("_")[0]

    if not isinstance(attr, (str, unicode)):
        return attr.name()
    elif strip_type in placeholders:
        return placeholders[strip_type]
    else:
        return "<{0}>".format(attr_type)
