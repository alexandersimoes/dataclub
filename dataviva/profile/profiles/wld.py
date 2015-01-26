# -*- coding: utf-8 -*-
from dataviva import db
from sqlalchemy import func
from flask.ext.babel import gettext as _
from dataviva.attrs import models as attrs
from dataviva.profile.profiles import Profile
from dataviva.profile.stat import Stat
from dataviva.visualize.build_models import *
from dataviva.secex.models import Ymw
from dataviva.utils.num_format import num_format

class WldProfile(Profile):
    """A country profile, which extends from the parent profile class.
        instantiate like: WldProfile(), WldProfile('aschn') or
        WldProfile('aschn', 'mg')
    """

    def __init__(self, wld_id=None, bra_id=None):
        """Defaults to most ubiquitous country = USA"""
        wld_id = wld_id or "nausa"
        attr_type = "bra" if bra_id else "wld"
        bra_id = bra_id if bra_id else "sabra"
        super(WldProfile, self).__init__(attr_type, bra_id, "wld", wld_id)

    def title_stem(self):
        return gettext("Trade <bra_article_from> <wld_article_to>")

    def sections(self):
        return [
            {
                "title": gettext("Trade Balance"),
                "anchor": "balance",
                "builds": [
                    Line("secex", {"bra": self.attr, "wld": self.filter_attr}, "wld", y="trade_val"),
                    Line("secex", {"bra": self.attr, "wld": self.filter_attr}, "wld", y="trade_net")
                ]
            },
            {
                "title": gettext("Trade Flow"),
                "anchor": "flow",
                "sections": [
                    {
                        "title": gettext("Products"),
                        "anchor": "hs",
                        "builds": [
                            TreeMap("secex", {"bra": self.attr, "wld": self.filter_attr}, "hs", size="export_val"),
                            TreeMap("secex", {"bra": self.attr, "wld": self.filter_attr}, "hs", size="import_val")
                        ]
                    },
                    {
                        "title": gettext("Locations"),
                        "anchor": "bra",
                        "builds": [
                            TreeMap("secex", {"bra": self.attr, "wld": self.filter_attr}, "bra", size="export_val"),
                            TreeMap("secex", {"bra": self.attr, "wld": self.filter_attr}, "bra", size="import_val")
                        ]
                    }
                ]
            }
        ]

    def headlines(self):
        return [
            Stat(self, "attr", "pop", attr=self.filter_attr, filter_attr=None),
            Stat(self, "secex", "export_val"),
            Stat(self, "secex", "import_val"),
            Stat(self, "attr", "gdp", attr=self.filter_attr, filter_attr=None)
        ]

    def stats(self):

        wld_name = self.filter_attr.name()

        return [
            {
                "title": gettext("Geography of <wld>").replace("<wld>", wld_name),
                "stats": [
                    Stat(self, "attr", "capital", attr=self.filter_attr, filter_attr=None),
                    Stat(self, "attr", "pop", attr=self.filter_attr, filter_attr=None),
                    Stat(self, "attr", "pop_density", attr=self.filter_attr, filter_attr=None),
                    Stat(self, "attr", "inet_users", attr=self.filter_attr, filter_attr=None),
                    Stat(self, "attr", "demonym", attr=self.filter_attr, filter_attr=None),
                    Stat(self, "attr", "neighbors", attr=self.filter_attr, filter_attr=None)
                ],
                "col": 1
            },
            {
                "title": gettext("Economy of <wld>").replace("<wld>", wld_name),
                "stats": [
                    Stat(self, "attr", "gdp", attr=self.filter_attr, filter_attr=None),
                    Stat(self, "attr", "gdp_per_capita", attr=self.filter_attr, filter_attr=None),
                    Stat(self, "attr", "gini", attr=self.filter_attr, filter_attr=None)
                ],
                "col": 2
            },
            {
                "title": self.attr.name(),
                "stats": [
                    Stat(self, "attr", "pop"),
                    Stat(self, "attr", "pop_density"),
                    Stat(self, "attr", "capital_dist"),
                    Stat(self, "attr", "airport_dist"),
                    Stat(self, "attr", "seaport_dist"),
                ],
                "col": 2
            },
            {
                "title": gettext("Trade with <bra>").replace("<bra>", self.attr.name()),
                "stats": [
                    Stat(self, "secex", "export_val"),
                    Stat(self, "secex", "import_val"),
                    Stat(self, "secex", "export_val", type="top", output="hs_id"),
                    Stat(self, "secex", "import_val", type="top", output="hs_id")
                ],
                "col": 3,
                "width": 2
            }
        ]

    def summary(self):
        p, text = [], []
        location = self.attr
        wld = self.filter_attr
        wld_stats = getattr(wld, "stats")
        if wld_stats:
            CONTINENT, COUNTRY = 2, 5
            pop = Stat(self, "attr", "pop", attr=None).format() or "n/a"
            pop_year = Stat(self, "attr", "pop", attr=None).year()
            gdp = Stat(self, "attr", "gdp", attr=None).format() or "n/a"
            gdp_per_capita = Stat(self, "attr", "gdp_per_capita", attr=None).format() or "n/a"
            if len(wld.id) == COUNTRY:
                continent = attrs.Wld.query.get(wld.id[:2])
                p.append(_(u"%(country)s is a country in %(subregion)s. " \
                    u"As of %(pop_year)s its population was %(pop)s, its GDP %(gdp)s, and its GDP per capita %(gdp_per_capita)s.",
                    country=wld.name(), subregion=wld_stats.subregion, continent=continent.name(),
                    pop_year=pop_year, pop=pop, gdp=gdp, gdp_per_capita=gdp_per_capita))
            text.append(" ".join(p).strip()); p = []
        #___________________________________
        # Brazil -> Destination exports
        #-----------------------------------
        exp_val = Stat(self, "secex", "export_val").value()
        if exp_val:
            year = Stat(self, "secex", "export_val").year()
            total_exp_val = db.session.query(func.sum(Ymw.export_val)).filter_by(year=year, month=0, wld_id_len=2).scalar()
            exp_pct = (exp_val / total_exp_val) * 100
            exp_pct = "{:.2g}%".format(exp_pct) if exp_pct > 0.01 else _("less than 0.01%%")
            rank, rank_total = Stat(self, "secex", "export_val", "top", "wld_id", attr=None).rank(with_total=True)
            if rank <= (rank_total/2):
                largest_or_smallest = _("largest")
            else:
                largest_or_smallest = _("smallest")
                rank = rank_total - rank
            top_prods, top_prods_len = Stat(self, "secex", "export_val", "top", "hs_id").list(val_num_format="export_val", with_len=True, with_location=True)
            p.append(_(u"%(location)s exported %(exp_val)s to %(country)s in 2014, making %(country)s the " \
                u"%(rank)s %(largest_or_smallest)s destination of the exports of %(location)s. %(country)s imports %(exp_pct)s of all of the exports of %(location)s. ",
                year=year, location=location.name(), exp_val=num_format(exp_val, "export_val"), country=wld.name(),
                rank=num_format(rank, "ordinal"), largest_or_smallest=largest_or_smallest, exp_pct=exp_pct))
            if(top_prods_len == 1):
                p.append(_(u"The sole product that %(location)s exports to %(country)s is %(top_prods)s. ",
                    location=location.name(), country=wld.name(), top_prods=top_prods))
            else:
                p.append(_(u"The top products that %(location)s exports to %(country)s include %(top_prods)s. ",
                    location=location.name(), country=wld.name(), top_prods=top_prods))

            if location.id == "sabra":
                bra_filter = location
                top_munics, top_munics_len = Stat(self, "secex", "export_val", "top", "bra_id").list(val_num_format="export_val", with_len=True, with_filter=True)
            else:
                bra_filter = location
                if len(bra_filter.id) == 9:
                    bra_filter = attrs.Bra.query.get(bra_filter.id[:3])
                top_munics, top_munics_len = Stat(self, "secex", "export_val", "top", "bra_id", attr=bra_filter).list(val_num_format="export_val", with_len=True, with_filter=True)
            if(top_munics_len == 1):
                p.append(_(u"The only municipality in %(location)s that exports to %(country)s is %(top_munics)s.",
                    location=bra_filter.name(), country=wld.name(), top_munics=top_munics))
            else:
                p.append(_(u"The municipalities in %(location)s with the highest export value to %(country)s are %(top_munics)s.",
                    location=bra_filter.name(), country=wld.name(), top_munics=top_munics))
            text.append(" ".join(p).strip()); p = []
        #___________________________________
        # Brazil <- Destination imports
        #-----------------------------------
        imp_val = Stat(self, "secex", "import_val").value()
        if imp_val:
            year = Stat(self, "secex", "import_val").year()
            total_imp_val = db.session.query(func.sum(Ymw.import_val)).filter_by(year=year, month=0, wld_id_len=2).scalar()
            imp_pct = (imp_val / total_imp_val) * 100
            imp_pct = "{:.2g}%".format(imp_pct) if imp_pct > 0.01 else _("less than 0.01%%")
            rank, rank_total = Stat(self, "secex", "import_val", "top", "wld_id", attr=None).rank(with_total=True)
            if rank <= (rank_total/2):
                largest_or_smallest = _("largest")
            else:
                largest_or_smallest = _("smallest")
                rank = rank_total - rank
            top_prods, top_prods_len = Stat(self, "secex", "import_val", "top", "hs_id").list(val_num_format="export_val", with_len=True, with_location=True)
            p.append(_(u"%(country)s exports %(imp_val)s to %(location)s, making %(country)s the " \
                u"%(rank)s %(largest_or_smallest)s origin of the imports of %(location)s. "\
                u"%(country)s represents %(imp_pct)s of all of the imports of %(location)s. ",
                location=location.name(), imp_val=num_format(imp_val, "import_val"), country=wld.name(),
                rank=num_format(rank, "ordinal"), largest_or_smallest=largest_or_smallest, imp_pct=imp_pct))
            if(top_prods_len == 1):
                p.append(_(u"The sole product that %(country)s exports to %(location)s is %(top_prods)s. ",
                    location=location.name(), country=wld.name(), top_prods=top_prods))
            else:
                p.append(_(u"The top products that %(country)s exports to %(location)s are %(top_prods)s.",
                    location=location.name(), country=wld.name(), top_prods=top_prods))
            
            if location.id == "sabra":
                top_munics, top_munics_len = Stat(self, "secex", "import_val", "top", "bra_id").list(val_num_format="export_val", with_len=True, with_filter=True)
            else:
                bra_filter = location
                if len(bra_filter.id) == 9:
                    bra_filter = attrs.Bra.query.get(bra_filter.id[:3])
                top_munics, top_munics_len = Stat(self, "secex", "import_val", "top", "bra_id", attr=bra_filter).list(val_num_format="export_val", with_len=True, with_filter=True)
            if(top_munics_len == 1):
                p.append(_(u"The only municipality in %(location)s that imports from %(country)s is %(top_munics)s.",
                    location=bra_filter.name(), country=wld.name(), top_munics=top_munics))
            else:
                p.append(_(u"The municipalities in %(location)s with the highest import value from %(country)s are %(top_munics)s.",
                    location=bra_filter.name(), country=wld.name(), top_munics=top_munics))
            text.append(" ".join(p).strip()); p = []
        return text
