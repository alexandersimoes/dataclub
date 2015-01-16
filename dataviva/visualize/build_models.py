# -*- coding: utf-8 -*-
import copy, re, urllib
from abc import ABCMeta, abstractmethod
from flask.ext.babel import gettext
from dataviva import __data_years__ as possible_years
from dataviva.attrs import models as attrs
from dataviva.profile.stat import Stat
from dataviva.visualize.titles import build_title
from dataviva.translations.translate import translate
from dataviva.utils.title_format import title_format
from dataviva.utils.title_case import title_case
from dataviva.rais.models import Ybi
from dataviva.secex.models import Ymbp

url_formats = {
    "secex": "/<app>/secex/<year>/<bra>/<hs>/<wld>/",
    "rais": "/<app>/rais/<year>/<bra>/<cnae>/<cbo>/<demo>/",
    "ei": "/<app>/ei/<year>/<bra_s>/<cnae_s>/<bra_r>/<cnae_r>/<hs>/",
    "sc": "/<app>/sc/<year>/<bra>/<school>/<course_sc>/<demo>/",
    "hedu": "/<app>/hedu/<year>/<bra>/<university>/<course_hedu>/<demo>/"
}

def getAttr(key):
    if not key or "course" in key:
        return key
    else:
        return key.split("_")[0]

class Build(object):
    __metaclass__ = ABCMeta
    """A summary of the DataViva Build class.

    This class should be used in instantiate an app (ie TreeMap, Stacked etc)
    that are all subclasses of a Build.

    Attributes:
        color (str): DataViva color assigned to the specific build.
        focus (bool): If the build requires a focus

    """
    color   = None
    focus   = False
    year    = None
    month   = None
    demo    = None
    limit   = None
    order   = None
    exclude = None
    def __init__(self, data_type, filter_attrs, display_attr, **kwargs):
        """The __init__ method for a Build instance.

        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            data_type (str): Data classification ie hs, secex etc.
            filter_attrs (dict of str): A dict keys by attr type ie {"bra":"mg"}.
            display_attr (str): The column name shown ie bra, hs, cnae_r, etc.
            kwargs (optional): The are the possible keyword args:
                year (int or str): if not provided will use most recent

        """
        self.data_type = data_type

        self.display_attr = getAttr(display_attr)
        self.display_key = display_attr

        self.icon = "/static/img/icons/app/app_{0}.png".format(str(self))

        # clamp years
        timeLimit = possible_years[self.data_type]
        if isinstance(timeLimit[0], (str, unicode)):
            yearLimit  = [int(p.split("-")[0]) for p in timeLimit]
            monthLimit = [int(p.split("-")[1]) for p in timeLimit]
        else:
            yearLimit  = timeLimit
            monthLimit = None

        if not self.year:
            self.year = kwargs.get("year", yearLimit[1])

        if self.year != "all":

            if isinstance(self.year, (str, unicode)):
                if "-" in self.year:
                    [self.year, self.month] = self.year.split("-")
                else:
                    self.year = int(self.year)

            self.year = min(yearLimit[1], self.year)
            self.year = max(yearLimit[0], self.year)

            if monthLimit:
                if self.month:
                    self.month = min(monthLimit[1], self.month)
                    self.month = max(monthLimit[0], self.month)
                else:
                    self.month = monthLimit[1]

        self.config = {}
        for k in ["size", "x", "y", "depth", "order", "split"]:
            if k in kwargs:
                self.config[k] = kwargs[k]

        for k in ["limit", "order", "exclude"]:
            if k in kwargs:
                setattr(self, k, kwargs[k])

        self.filters = 0

        def parseFilter(value, f):

            if f == "bra_r" and value != "<{0}>".format(f):
                if isinstance(value, attrs.Bra):
                    value = value.id
                if type(value) == str:
                    value = value[:3]

            f_type = getAttr(f)

            if f_type == "bra" and (value == "all" or (hasattr(value, "id") and value.id == "sabra")):
                f_type = "wld"

            if value.__class__.__name__.lower() == f_type:

                self.filters += 1
                return value

            elif value == "<{0}>".format(f) or not hasattr(attrs, f_type.capitalize()):
                return value
            else:

                attr_type = getattr(attrs, f_type.capitalize())

                try:
                    attr = attr_type.query.get_or_404(value)
                except:
                    raise RuntimeError(u"Unknown {0}: {1}".format(f_type.capitalize(), value))

                self.filters += 1
                return attr

        # get attrs from DB
        self.filter_attrs = filter_attrs
        for f, value in self.filter_attrs.iteritems():
            self.filter_attrs[f] = parseFilter(value, f)
            if f == "demo":
                self.demo = value

        focus = kwargs.get("focus", None)

        if self.focus or focus:

            self.focus = focus

            if self.focus:
                self.focus = parseFilter(self.focus, self.display_key)
                self.config["focus"] = self.focus.id if self.focus and type(self.focus) != str else self.focus
            else:
                raise RuntimeError("Build requires focus.")

    @abstractmethod
    def app_name(self):
        """"Return a string representing the type of app this is."""
        pass

    def description(self):
        pass

    def title(self):
        title = self.title_stem()
        if not title:
            return self.url()
        else:
            attrs = copy.copy(self.filter_attrs)
            if self.focus:
                attrs[self.display_key] = self.focus
            t = title_format(title, attrs)
            if self.year != "all":
                time = self.year
                latest = possible_years[self.data_type][1]
                if isinstance(latest, (str, unicode)) and "-" in latest:
                    maxYear, maxMonth = [int(m) for m in latest.split("-")]
                    if self.year == maxYear and maxMonth != 12:
                        jan = translate("month_1_short")
                        if maxMonth == 1:
                            time = "{0} {1}".format(jan, time)
                        else:
                            latestMonth = translate("month_{0}_short".format(maxMonth))
                            time = "{0}-{1} {2}".format(jan, latestMonth, time)
                t = u"{0} ({1})".format(t, time)
            return t

    def title_stem(self):
        return build_title(self)

    def completion(self):
        filters = len(self.filter_attrs)
        return float(self.filters) / filters if filters > 0 else 1

    def coords(self):
        pass

    def network(self):
        pass

    def time(self):
        return "{0}-{1}".format(self.year, self.month) if self.month else str(self.year)

    def url(self):

        output_attr = self.display_attr.capitalize()

        depth = None
        if hasattr(attrs, output_attr):
            attr = getattr(attrs, output_attr)
            if hasattr(attr, "depths"):
                d = -2 if output_attr == "Cnae" and self.data_type == "ei" else -1
                depth = attr.depths[d]

        data_url = url_formats[self.data_type]
        data_url = data_url.replace("<app>", str(self))

        data_url = data_url.replace("<year>", self.time())

        for key, attr in self.filter_attrs.iteritems():
            placeholder = "<{0}>".format(key)
            if placeholder in data_url and attr != placeholder:
                if key == self.display_key:
                    if "y" in self.config and self.config["y"] == "trade_val":
                        depth = len(attr.id)
                    suffix = "show.{0}".format(depth) if depth else "show"
                else:
                    suffix = ""

                if isinstance(attr, (str, unicode)):
                    value = attr
                else:
                    if "bra" in key and attr.id == "sabra":
                        value = "" if len(suffix) > 0 else "all"
                    else:
                        value = attr.id

                if len(value) and len(suffix):
                    # if len(value) == int(suffix.split(".")[1]):
                    #     suffix = ""
                    # else:
                    suffix = ".{0}".format(suffix)

                data_url = data_url.replace(placeholder, value + suffix)

        placeholder = "<{0}>".format(self.display_key)
        if "show" not in data_url and placeholder in data_url:
            show = "show.{0}".format(depth) if depth else "show"
            data_url = data_url.replace(placeholder, show)

        data_url = re.sub("<(\w+)>", "all", data_url)

        params = {}
        for k in ["limit", "order", "exclude"]:
            param = getattr(self, k)
            if param:
                params[k] = param
        for k, param in self.config.iteritems():
            params[k] = param

        params = urllib.urlencode(params)
        if len(params) > 0:
            params = "?{0}".format(params)

        return "/build{0}{1}".format(data_url, params)

    def serialize(self):

        stem = self.title_stem()
        if stem:
            filters = re.findall("<(\w+)>", stem)
            filters = [str(f) for f in filters]
            for i, f in enumerate(filters):
                if "_article" in f:
                    name = re.search("(\w+)_article_(\w+)", f)
                    filters[i] = name.group(1)
            stem = stem.encode("utf-8")
        else:
            filters = []

        attrs = {}
        for t, a in self.filter_attrs.iteritems():
            if not isinstance(a, (str, unicode)):
                if t not in attrs:
                    attrs[t] = []
                attrs[t].append(a.id)

        return {
            "app_name": self.app_name().encode("utf-8"),
            "app_type": str(self).encode("utf-8"),
            "color": self.color,
            "completion": self.completion(),
            "config": self.config,
            "coords": self.coords(),
            "data_type": self.data_type,
            "demo": self.demo,
            "display_attr": self.display_attr,
            "display_key": self.display_key,
            "filter_ids": attrs,
            "filter_types": filters,
            "network": self.network(),
            "stem": stem,
            "title": self.title().encode("utf-8"),
            "url": self.url()
        }

    def __repr__(self):
        return u"<{0}: {1} ({2})>".format(self.app_name(), self.title(), self.time())


class TreeMap(Build):
    """A tree map, which extends from the parent build class."""

    color = "#ffc41c"

    def app_name(self):
        """"Return a string representing the type of app this is."""
        return gettext('Tree Map')

    def __str__(self):
        return 'tree_map'

class Stacked(Build):
    """A stacked area chart, which extends from the parent build class."""

    color = "#742777"
    year = "all"

    def app_name(self):
        """"Return a string representing the type of app this is."""
        return gettext('Stacked')

    def __str__(self):
        return 'stacked'

class GeoMap(Build):
    """A geographic map, which extends from the parent build class."""

    color = "#3daf49"

    def app_name(self):
        """"Return a string representing the type of app this is."""
        return gettext('Geo Map')

    def coords(self):

        cat = self.display_attr
        display_id = False
        if cat in self.filter_attrs and type(self.filter_attrs[cat]) != str:
            display_id = self.filter_attrs[cat].id[:3]
            depth = getattr(attrs, cat.capitalize()).depths[-1]
        elif cat not in self.filter_attrs and cat == "bra":
            cat = "wld"
            display_id = "sabra"
            depth = 3

        if display_id:
            return "/static/json/coords/{0}/{0}_{1}_{2}.json".format(cat, display_id, depth)
        else:
            return False

    def __str__(self):
        return 'geo_map'

class Network(Build):
    """A network, which extends from the parent build class."""

    color = "#af1f24"

    def app_name(self):
        """"Return a string representing the type of app this is."""
        return gettext('Network')

    def title_stem(self):
        if self.display_attr == "hs":
            return gettext("Product Space <bra_article_for>")
        elif self.display_attr == "cnae":
            return gettext("Industry Space <bra_article_for>")
        pass

    def network(self):
        return "/static/json/networks/network_{0}.json".format(self.display_attr)

    def description(self):

        braPresent = "bra" in self.filter_attrs
        if braPresent:
            name = self.filter_attrs["bra"].name()
        else:
            name = gettext("Brazil")

        if self.display_attr == "hs":
            text = []
            text.append(gettext(u"The product space is a network connecting products with a high likelihood of being co-exported and can be used to predict the evolution of a location’s export structure."))

            if braPresent:
                rca = len(Ymbp.query.filter_by(year=self.year, month=0, bra_id=self.filter_attrs["bra"].id, hs_id_len=6).filter(Ymbp.rca>=1).all())
                text.append(gettext(u"The %(rca)d products exported by %(location)s (with comparative advantage) are shown using colored nodes, while the products that are not being exported by %(location)s appear in light grey. The probability that %(location)s will become an exporter of a product increases with the number of connections that this product has to products that %(location)s is currently exporting.", rca=rca, location=name))

            return text

        if self.display_attr == "cnae":
            text = []
            text.append(gettext(u"The industry space is a network connecting industries that hire the same occupations and can be used to predict the evolution of a location’s industrial structure."))

            if braPresent:
                rca = len(Ybi.query.filter_by(year=self.year, bra_id=self.filter_attrs["bra"].id, cnae_id_len=6).filter(Ybi.rca>=1).all())
                text.append(gettext(u"The %(rca)d industries present in %(location)s (with comparative advantage) are shown using colored nodes, while the industries that are absent from %(location)s appear in light grey. The probability that %(location)s will develop an industry increases with the number of connections that this industry has to industries that are already present in %(location)s.", rca=rca, location=name))

            return text
        pass

    def __str__(self):
        return 'network'

class Rings(Build):
    """A ring network, which extends from the parent build class."""

    color = "#d67ab0"
    focus = True

    def app_name(self):
        """"Return a string representing the type of app this is."""
        return gettext('Rings')

    def title_stem(self):
        if self.display_attr == "hs":
            return gettext("Products co-exported <hs_article_with> <bra_article_in>")
        elif self.display_attr == "cnae":
            return gettext("Industries that are similar <cnae_article_to> <bra_article_in>")
        elif self.display_attr == "cbo":
            return gettext("Common career transitions <cbo_article_for> <bra_article_in>")
        pass

    def network(self):
        return "/static/json/networks/network_{0}.json".format(self.display_attr)

    def __str__(self):
        return 'rings'

class Scatter(Build):
    """A scatter plot, which extends from the parent build class."""

    color = "#0b1097"

    def app_name(self):
        """"Return a string representing the type of app this is."""
        return gettext('Scatter')

    def __str__(self):
        return 'scatter'

class Compare(Build):
    """A Comparison scatter plot, which extends from the parent build class."""

    color = "#1abbee"

    def app_name(self):
        """"Return a string representing the type of app this is."""
        return gettext('Compare')

    def title_stem(self):
        if self.display_attr == "hs":
            if "wld" in self.filter_attrs:
                return gettext("Exports of <bra> and <bra> to <wld>")
            else:
                return gettext("Export Comparison for <bra> and <bra>")
        if self.display_attr == "wld":
            if "hs" in self.filter_attrs:
                return gettext("Export Destinations of <hs> from <bra> and <bra>")
            else:
                return gettext("Export Destinations Comparison for <bra> and <bra>")
        if self.display_attr == "cnae":
            if "cbo" in self.filter_attrs:
                return gettext("Industries that employ <cbo> in <bra> and <bra>")
            else:
                return gettext("Industrial Comparison for <bra> and <bra>")
        if self.display_attr == "cbo":
            if "cnae" in self.filter_attrs:
                return gettext("Employment of <cnae> in <bra> and <bra>")
            else:
                return gettext("Employment Comparison for <bra> and <bra>")
        pass

    def __str__(self):
        return 'compare'

class Occugrid(Build):
    """A Comparison scatter plot, which extends from the parent build class."""

    color = "#e87600"

    def app_name(self):
        """"Return a string representing the type of app this is."""
        return gettext('Occugrid')

    def title_stem(self):
        return gettext("Estimated employment for <cnae> in <bra>")

    def __str__(self):
        return 'occugrid'

class Bar(Build):
    """A Comparison scatter plot, which extends from the parent build class."""

    color = "#93789e"

    def app_name(self):
        """"Return a string representing the type of app this is."""
        return gettext('Bar Chart')

    def __str__(self):
        return 'bar'

class Pie(Build):
    """A Comparison scatter plot, which extends from the parent build class."""

    color = "#800000"

    def app_name(self):
        """"Return a string representing the type of app this is."""
        return gettext('Pie Chart')

    def __str__(self):
        return 'pie'

class Line(Build):
    """A Comparison scatter plot, which extends from the parent build class."""

    color = "#a4bd99"
    year = "all"

    def app_name(self):
        """"Return a string representing the type of app this is."""
        return gettext('Line Chart')

    def __str__(self):
        return 'line'

class Box(Build):
    """A Comparison scatter plot, which extends from the parent build class."""

    color = "#b7834b"
    year = "all"

    def app_name(self):
        """"Return a string representing the type of app this is."""
        return gettext('Box and Whisker Plot')

    def __str__(self):
        return 'box'
