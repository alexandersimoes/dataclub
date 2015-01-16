# -*- coding: utf-8 -*-
import re
from abc import ABCMeta, abstractmethod
from flask.ext.babel import gettext
from dataviva import __data_years__ as possible_years
from dataviva.attrs import models as attrs
from dataviva.utils.title_format import title_format
from dataviva.profile.stat import Stat
from dataviva.visualize.build_models import *

class Profile(object):
    __metaclass__ = ABCMeta
    """A summary of the DataViva Profile class.

    This class should be used in instantiate an app (ie TreeMap, Stacked etc)
    that are all subclasses of a Build.

    """
    def __init__(self, attr_type, attr, filter_attr_type=None, filter_attr=None, **kwargs):
        """The __init__ method for a Build instance.

        Note:
            There are 3 "types" of profiles:
            0. Single attr profile (filter_attr_type & filter_attr not specified)
                ex. Minas Gerais or CEOs
            1. Single attr profile w/ filter (filter_attr not specified)
                ex. Education in Minas Gerais - filter_attr_type = edu
            2. Double attr profile
                ex. Garbagemen in Minas Gerais - filter_attr_type = cbo,
                filter_attr = garbagemen

        Args:
            attr_type (str): The attr type being shown ie bra, hs, cnae etc.
            attr (str): The ID of the specific attr.
            filter_attr_type (str): This would be either the attr_type of a
                second attr to be given for a type 3 profile OR a string rep
                a means of filtering the profile by a single section ie
                Education in Minas Gerais or Employment in Minas Gerais
            filter_attr (str): The ID of the specific attr for a type 3 profile.
            type (int): see note above
        """
        self.type = 0
        self.attr_type = getattr(attrs, attr_type.capitalize())
        self.attr = attr
        self.filters = 0
        if self.attr != "<bra>":
            self.filters += 1
            self.attr = self.attr_type.query.get_or_404(attr)
        self.filter_attr = filter_attr
        self.filter_attr_type = filter_attr_type
        if filter_attr_type and filter_attr:
            self.type = 2
            self.filter_attr_type = getattr(attrs, filter_attr_type.capitalize())
            if self.filter_attr != "<{0}>".format(filter_attr_type):
                self.filters += 1
                self.filter_attr = self.filter_attr_type.query.get(filter_attr)
        elif filter_attr_type:
            self.type = 1

    def title_stem(self):
        return ""

    def title(self):
        stem = self.title_stem()
        attrs = {}
        if type(self.attr) is str:
            attrs[self.attr[1:-1]] = self.attr
        else:
            attrs[self.attr.attr()] = self.attr
        if self.filter_attr:
            if type(self.filter_attr) is str:
                attrs[self.filter_attr[1:-1]] = self.filter_attr
            else:
                attrs[self.filter_attr.attr()] = self.filter_attr
        return title_format(stem, attrs)

    def subtitle(self):
        if type(self.attr) == str or self.attr.id == "sabra":
            pass
        else:
            sub = self.attr.name()
            # not state or region
            if len(self.attr.id) > self.attr.depths[1]:
                sub += ", {0}".format(self.attr.id[self.attr.depths[0]:self.attr.depths[1]].upper())
            if self.attr.capital():
                sub = u"{0} ({1})".format(sub,gettext("Capital"))
            return sub

    def headlines(self):
        """"Return a string representing the title to be shown."""
        pass

    def url(self):

        bra_id = self.attr
        if bra_id != "<bra>":
            bra_id = bra_id.id
        url = "/profile/{0}/{1}/".format(self.attr_type.__name__.lower(), bra_id)

        if self.type == 1:
            url += "{0}/".format(self.filter_attr_type)
        elif self.type == 2:
            filter_attr = self.filter_attr_type.__name__.lower()
            filter_id = self.filter_attr
            if filter_id != "<{0}>".format(filter_attr):
                filter_id = filter_id.id
            url += "{0}/{1}/".format(filter_attr,filter_id)
        return url

    def fallback(self, variable):
        f = None
        if self.type == 2 and not isinstance(self.filter_attr, (str, unicode)):
            if self.filter_attr.attr() == "university" and (isinstance(self.attr, (str, unicode)) or self.attr.id == "sabra"):
                attr = self.filter_attr.get_locations()[0]
                f = getattr(attr, variable)()
            else:
                f = getattr(self.filter_attr, variable)()
        if not f and not isinstance(self.attr, (str, unicode)):
            f = getattr(self.attr, variable)()
        return f

    def image(self):
        image = self.fallback("image")
        if not image:
            image = {"url": "/static/img/bgs/triangles_grey.png"}
        return image

    def icon(self):
        if self.type == 2 and not isinstance(self.filter_attr, str):
            return self.filter_attr.icon()
        elif not isinstance(self.attr, str):
            return self.attr.icon()
        return None

    def palette(self):
        palette = self.fallback("get_palette")
        if palette:
            return palette.split(", ")
        return []

    def summary(self):
        pass

    def serialize(self):

        denom = 2 if self.type == 2 else 1

        if self.type == 0:
            stem = u"<bra>"
        elif self.type == 1:
            stem = u"<bra> {0}".format(self.title())
        else:
            stem = u"<{0}> {1} <bra>".format(self.filter_attr_type.__name__.lower(),gettext("in"))

        filters = re.findall(r"<(.*?)>", stem)

        return {
            "completion": float(self.filters) / denom,
            "filter_types": filters,
            "icon": self.icon(),
            "image": self.image(),
            "palette": self.palette(),
            "title": self.title(),
            "stem": stem,
            "subtitle": self.subtitle(),
            "type": self.type,
            "url": self.url()
        }

    def __str__(self):
        return self.title()

    def __repr__(self):
        return "<Profile: {0}>".format(self.title())

from bra import BraProfile
from cbo import CboProfile
from cnae import CnaeProfile
from hs import HsProfile
from wld import WldProfile
from course_hedu import Course_heduProfile
from university import UniversityProfile
