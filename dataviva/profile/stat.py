# -*- coding: utf-8 -*-
from decimal import Decimal
from abc import ABCMeta, abstractmethod
from flask.ext.babel import gettext
from sqlalchemy import func, desc
from dataviva import __data_years__ as possible_years
from dataviva.attrs import models as attrs
from dataviva.utils.num_format import num_format, affixes
from dataviva.utils.title_case import title_case
from dataviva.translations.translate import translate
from dataviva import __data_years__

from dataviva.secex.models import Ymw, Ymbp, Ympw, Ymbw, Ymbpw
from dataviva.rais.models import Yb as Rais_yb, Yo, Ybo, Yi, Ybi
from dataviva.hedu.models import Ybu, Yc, Ybc

from dataviva.secex.views import secex_api
from dataviva.rais.views import rais_api
from dataviva.hedu.views import hedu_api
from dataviva.sc.views import sc_api
from dataviva.ei.views import ei_api

class Stat(object):
    __metaclass__ = ABCMeta
    """A summary of the DataViva Stat class.

    This class should be used in instantiate a stat used throughout the
    profiles, in the stats section as well as in the summary texts.

    """
    # top.secex.import_val.hs_id
    # val.hedu.num_universities.
    def __init__(self, profile, dtype, val, type="val", output=None, attr=True, filter_attr=True, num_items=5, exclude=None, ei_flow=None):
        """The __init__ method for a Build instance.

        Args (required):
            profile (Profile): The profile to use for introspection purposes
            dtype (str): ones of -- attr, secex, rais, hedu, sc or ei
            val (str): The column of data requested i.e. import_val
            type (str): one of --
                top: get top <num_items> <output>s ordered by <val>
                val: just get the specific value we're looking for
            output (str): return type of items sought (can include "." for specific depth)
                otherwise uses deepest for that attribute type
        Args (optional):
            attr (Attr): An instance of an attr to use for data filtering purposes
            num_items (int): The number of items requested only used when type==top
        """
        self.profile = profile
        self.dtype = dtype
        self.val = val
        self.type = type
        self.ei_flow = ei_flow

        '''parse output if given, allow user to request specific depth via "." '''
        self.output = output
        self.prefix = None
        if self.output:

            if "_id" not in self.output:
                self.output = "{}_id".format(self.output)

            if "." in self.output:
                self.output_id, self.depth = self.output.split(".", 1)
                if "." in self.depth:
                    self.depth, self.prefix = self.depth.split(".", 1)
            else:
                self.output_id = self.output

            self.output = getattr(attrs, self.output.split("_id")[0].capitalize())

            if not hasattr(self, "depth"):
                self.depth = self.output.depths[-1]

        self.attr = self.profile.attr if attr is True else attr
        if profile.type == 2:
            self.filter_attr = self.profile.filter_attr if filter_attr == True else filter_attr
        else:
            self.filter_attr = None
        self.num_items = num_items
        self.exclude = exclude

    def format(self, labels=True):

        v = self.value()

        if isinstance(v, (Decimal, long, int, float)):
            v = num_format(v, self.val, labels=labels)

            # Tries to add the entity name for distance statistics.
            if labels and self.dtype == "attr" and "_dist" in self.val:
                name_key = u"{}_name".format(self.val.split("_")[0])
                if hasattr(self.attr, name_key):
                    name = getattr(getattr(self.attr, "stats"), name_key)
                    if name:
                        v = u"{} ({})".format(v, name)

        elif isinstance(v, (str, unicode)):
            v = title_case(v)

        elif isinstance(v, (list)):
            if isinstance(v[0], (tuple)):
                if labels:
                    v = [u"{} ({})".format(x[0].name(),num_format(x[1], self.val, labels=True)) for x in v]
                else:
                    v = [x[0].name() for x in v]
            else:
                v = [x.name() for x in v]

        return v

    def title(self):
        if "_dist" in self.val:
            if len(self.attr.id) == self.attr.depths[-1:][0]:
                return translate(self.val)
            else:
                return translate(u"{}_med".format(self.val))
        if self.val == "neighbors" and self.attr.id == "sabra":
            return None
        if self.val == "capital_dist" and getattr(self.attr, self.val) == 0:
            return None
        if self.type == "top":
            return translate("top.{}.{}.{}".format(self.dtype, self.val, self.output_id), self.num_items)

        num = self.value()
        if isinstance(num, (int, long, Decimal)):
            return translate(self.val, num)
        return translate(self.val)

    def list(self, val_num_format=None, with_len=False, with_value=True, with_filter=False, with_location=False):
        if with_filter:
            url_attr = self.filter_attr
        elif with_location:
            url_attr = self.attr
        else:
            url_attr = None
        val_list = self.value()
        if val_list is None:
            if with_len:
                return (None, None)
            return None
        if type(val_list) is not list:
            return NotImplemented
        if with_value:
            val_list = [u"<a href='{}'>{}</a> ({})".format(val[0].url(attr=url_attr), val[0].name(), num_format(val[1], val_num_format)) for val in val_list]
        else:
            val_list = [u"<a href='{}'>{}</a>".format(val[0].url(attr=url_attr), val[0].name()) for val in val_list]
        val_list_len = len(val_list)
        if val_list_len == 1:
            if with_len:
                return (val_list[0], val_list_len)
            return val_list[0]
        val_list = u"{} {} {}".format(", ".join(val_list[:-1]), gettext("and"), val_list[-1])
        if with_len:
            return (val_list, val_list_len)
        return val_list


    def rank(self, within_state=False, with_total=False):
        if self.dtype == "attr":
            attr_stats = getattr(self.attr, "stats", None)
            if attr_stats and hasattr(attr_stats, self.val):
                stat_class = attrs.Bra_stats if type(self.attr) == attrs.Bra else attrs.Wld_stats
                id_col = "bra_id" if type(self.attr) == attrs.Bra else "wld_id"
                depth = len(self.attr.id)
                q = stat_class.query.with_entities(id_col).filter(func.char_length(getattr(stat_class, id_col))==depth).filter(self.val!=None)
                if within_state:
                    state = self.attr.id[:3]
                    q = q.filter(getattr(stat_class, id_col).startswith(state))
                items = q.order_by(desc(getattr(stat_class, self.val))).all()
                items = [i for (i, ) in items]
                rank = items.index(self.attr.id) + 1
        else:
            filters = self.get_filters(use_filter_attr=False)
            if "limit" in filters: del filters["limit"]
            filters["order"] = self.val
            items = self.view(**filters)
            items = [i.get(self.output_id, None) for i in items]
            try:
                rank = items.index(self.filter_attr.id) + 1
            except:
                rank = None
        if with_total:
            return (rank, len(items))
        else:
            return rank

    def unit(self):
        unit = affixes(self.val, unit=True)
        key = unit if unit else self.val
        if "growth" in key:
            key = "growth"
        key = "{0}_unit".format(key)

        num = self.value()
        if isinstance(num, (int, long, Decimal)):
            return translate(key, num)
        return translate(key)

    def count(self):
        qfilters = self.get_filters(limit=False, order=False)
        return len(self.view(**qfilters))

    def get_filters(self, use_filter_attr=True, limit=True, order=True):
        self.view = globals()["{}_api".format(self.dtype)]
        # first add location (either BRA or WLD)
        if self.dtype == "ei":
            flow = self.ei_flow if self.ei_flow else "s"
            bra_key = "bra_id_{}".format(flow)
            cnae_key = "cnae_id_{}".format(flow)
        else:
            bra_key = "bra_id"
            cnae_key = "cnae_id"
        bra_key = "bra_id_s" if self.dtype == "ei" else "bra_id"
        filters = {bra_key: "all", "year": __data_years__[self.dtype][1], "serialize": False}
        if isinstance(self.attr, attrs.Bra):
            if self.output is attrs.Bra:
                filters[bra_key] = "{}.show.{}".format(self.attr.id, self.depth)
            else:
                filters[bra_key] = self.attr.id
        if self.output:

            if self.output_id not in filters or filters[self.output_id] == "all":
                filters[self.output_id] = "show.{}".format(self.depth)

            if self.output is attrs.University:
                filters[self.output_id] = "show"
            elif self.prefix:
                filters[self.output_id] = "{}.{}".format(self.prefix, filters[self.output_id])
            elif isinstance(self.filter_attr, self.output) and use_filter_attr:
                filters[self.output_id] = "{}.{}".format(self.filter_attr.id, filters[self.output_id])

        if self.filter_attr and (not self.output or not isinstance(self.filter_attr, self.output)):
            attr_type = self.filter_attr.attr()
            if attr_type == "cnae" and self.dtype == "ei":
                attr_id = cnae_key
            else:
                attr_id = "{}_id".format(attr_type)
            filters[attr_id] = self.filter_attr.id

        if limit:
            filters["limit"] = self.num_items
        if order:
            filters["order"] = self.val
        if self.exclude:
            filters["exclude"] = self.exclude

        # raise Exception(filters)
        return filters

    def value(self):
        if self.dtype == "attr":
            if self.val == "pop_100km":
                return sum(dist.bra.stats.pop for dist in self.attr.get_neighbors(100, True))
            if self.val == "prox":
                attr = self.filter_attr or self.attr
                if attr.id != "sabra":
                    return None
                return [getattr(v, self.output_id.split("_")[0]) for v in self.attr.get_similar()]
            if self.attr is not None:
                attr_stats = getattr(self.attr, "stats", None)
            else:
                attr_stats = getattr(self.filter_attr, "stats", None)
            if attr_stats and hasattr(attr_stats, self.val):
                stat = getattr(attr_stats, self.val)
                # If the attribute is a list of neighbors, convert the IDs
                # into Attr classes.
                if stat and self.val == "neighbors":
                    if self.attr.id == "sabra":
                        return None
                    else:
                        a = self.attr.__class__
                        ids = [b.strip() for b in stat.split(",")]
                        return [a.query.get_or_404(x) for x in [b.strip() for b in stat.split(",")]]
                # If the attribute is the capital, remove it (stats without
                # a title do not get displayed in the template).
                if self.val == "capital_dist" and stat == 0:
                    return None
                return stat
        else:
            qfilters = self.get_filters()
            resp = self.view(**qfilters)
            # raise Exception(resp)
            if resp:
                if self.type != "val":
                    resp = [(self.output.query.get(r.get(self.output_id)), r.get(self.val)) for r in resp]
                    return sorted(resp, key=lambda v: v[1], reverse=True)
                else:
                    return resp[0].get(self.val, None)
        return None

    def year(self):
        if self.dtype == "attr":
            if "pop" in self.val: return 2014
            if "gdp" in self.val: return 2012
            if "hdi" in self.val: return 2013
        else:
            try:
                return possible_years[self.dtype][1]
            except:
                return None

    def __repr__(self):
        return "<Stat {0}:{1}>".format(self.dtype, self.val)

""" test
s1 = Stat(BraProfile("4mg030000"), "attr", "pop")
s2 = Stat(BraProfile("4mg030000"), "hedu", "num_universities")
s3 = Stat(BraProfile("4mg030000"), "secex", "import_val", "top", "hs_id")
"""
