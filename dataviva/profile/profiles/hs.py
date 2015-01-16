# -*- coding: utf-8 -*-
from dataviva import db
from sqlalchemy import func
from flask.ext.babel import gettext as _
from dataviva.attrs import models as attrs
from dataviva.profile.profiles import Profile
from dataviva.profile.profiles.bra import BraProfile
from dataviva.profile.stat import Stat
from dataviva.translations.translate import translate
from dataviva.utils.num_format import num_format
from dataviva.visualize.build_models import *
from dataviva.secex.models import Ymp, Ymbp

class HsProfile(Profile):
    """A HS product profile, which extends from the parent profile class.
        instantiate like: HsProfile(), HsProfile('010101') or
        HsProfile('010101', 'mg')
    """

    def __init__(self, hs_id=None, bra_id=None):
        """Defaults to most ubiquitous product = Iron Fasteners"""
        hs_id = hs_id or "157318"
        attr_type = "bra" if bra_id else "wld"
        bra_id = bra_id if bra_id else "sabra"
        super(HsProfile, self).__init__(attr_type, bra_id, "hs", hs_id)
        total_exp_val = Stat(self, "secex", "export_val", filter_attr=None).value()
        # raise Exception(total_exp_val)

    def title_stem(self):
        if self.attr == "<bra>" or self.attr.id != "sabra":
            return gettext("<hs> <bra_article_in>")
        else:
            return gettext("<hs>")

    def sections(self):
        s = [
            {
                "title": gettext("Trade Balance"),
                "anchor": "balance",
                "builds": [
                    Line("secex", {"bra": self.attr, "hs": self.filter_attr}, "hs", y="trade_val"),
                    Line("secex", {"bra": self.attr, "hs": self.filter_attr}, "hs", y="trade_net")
                ]
            },
            {
                "title": gettext("International Trade"),
                "anchor": "secex",
                "sections": [
                    {
                        "title": gettext("Trade Partners"),
                        "anchor": "secex_wld",
                        "builds": [
                            TreeMap("secex", {"bra": self.attr, "hs": self.filter_attr}, "wld", size="export_val"),
                            TreeMap("secex", {"bra": self.attr, "hs": self.filter_attr}, "wld", size="import_val")
                        ]
                    }
                ]
            },
            {
                "title": gettext("Domestic Trade"),
                "anchor": "ei",
                "builds": [
                    TreeMap("ei", {"bra_s": self.attr, "hs":self.filter_attr}, "bra_s"),
                    TreeMap("ei", {"bra_s": self.attr, "hs":self.filter_attr}, "cnae_s"),
                    TreeMap("ei", {"bra_s": self.attr, "hs":self.filter_attr}, "cnae_r")
                ]
            }
        ]

        if len(self.attr.id) < 9:
            s[1]["sections"].append({
                "title": gettext("Brazilian Consumption"),
                "anchor": "secex_bra",
                "builds": [
                    TreeMap("secex", {"bra": self.attr, "hs": self.filter_attr}, "bra", size="export_val"),
                    TreeMap("secex", {"bra": self.attr, "hs": self.filter_attr}, "bra", size="import_val")
                ]
            })

        if len(self.filter_attr.id) == 6:
            s.append({
                "title": gettext("Related Products"),
                "anchor": "rings",
                "builds": [
                    Rings("secex", {"bra": self.attr}, "hs", focus=self.filter_attr)
                ]
            })

        return s

    def headlines(self):
        return [
            Stat(self, "secex", "export_val"),
            Stat(self, "secex", "import_val"),
            Stat(self, "secex", "import_val", type="top", output="wld_id", num_items=1),
            Stat(self, "secex", "export_val", type="top", output="wld_id", num_items=1)
        ]

    def stats(self):

        if type(self.attr) == attrs.Bra:
            gen_stats = ["capital_dist", "demonym", "neighbors", "gdp", "gdp_per_capita", "airport_dist", "seaport_dist"]
        elif type(self.attr) == attrs.Wld:
            gen_stats = ["demonym", "neighbors", "gdp", "gdp_per_capita", "area", "capital", "gini", "subregion", "inet_users"]

        s = [
            {
                "title": gettext("Population"),
                "stats": [
                    Stat(self, "attr", "pop"),
                    Stat(self, "attr", "pop_density")
                ],
                "col": 1
            },
            {
                "title": gettext("Geography"),
                "stats": [Stat(self, "attr", s) for s in gen_stats],
                "col": 1
            },
            {
                "title": gettext("Economy"),
                "stats": [
                    Stat(self, "secex", "rca"),
                    # Stat(self, "secex", "rcd"),
                    Stat(self, "secex", "export_val"),
                    Stat(self, "secex", "import_val"),
                    Stat(self, "secex", "import_val", type="top", output="wld_id"),
                    Stat(self, "secex", "export_val", type="top", output="wld_id"),
                    Stat(self, "ei", "purchase_value"),
                    Stat(self, "ei", "purchase_value", type="top", output="cnae_id_s"),
                    Stat(self, "ei", "purchase_value", type="top", output="cnae_id_r")
                ],
                "col": 2,
                "width": 3
            }
        ]
        
        if type(self.attr) == attrs.Bra:
            s[2]["stats"].insert(1, Stat(self, "secex", "rcd"))
        
        return s

    def summary(self):
        p, text = [], []
        location = self.attr
        hs = self.filter_attr
        hs_section = None
        REGION, STATE, MESO, MICRO, PLN_REG, MUNIC = 1, 3, 5, 7, 8, 9
        SECTION, PRODUCT = 2, 6
        #___________________________________
        # Overview
        #-----------------------------------
        exp_val = Stat(self, "secex", "export_val").value()
        imp_val = Stat(self, "secex", "import_val").value()
        year = Stat(self, "secex", "import_val").year()
        if exp_val and imp_val:
            trade_ratio = max(exp_val, imp_val) / min(exp_val, imp_val)
            t_balance = gettext("exports") if exp_val > imp_val else gettext("imports")
            p.append(_(u"In %(year)s %(location)s exported %(exp_val)s and imported %(imp_val)s worth of %(prod)s, " \
                u"making their trade balance %(trade_ratio)d to 1 in favor of %(t_balance)s.",
                year=year, location=location.name(), exp_val=num_format(exp_val, "export_val"), imp_val=num_format(imp_val, "export_val"), prod=hs.name(),
                trade_ratio=trade_ratio, t_balance=t_balance))
        elif exp_val:
            p.append(_(u"In %(year)s %(location)s exported %(exp_val)s but did not import any %(prod)s.",
                year=year, location=location.name(), exp_val=num_format(exp_val, "export_val"), prod=hs.name()))
        elif imp_val:
            p.append(_(u"In %(year)s %(location)s imported %(imp_val)s but did not export any %(prod)s.",
                year=year, location=location.name(), imp_val=num_format(imp_val, "import_val"), prod=hs.name()))
        else:
            p.append(_(u"In %(year)s %(location)s did not export or import %(prod)s.", year=year, location=location.name(), prod=hs.name()))

        exp_pct = 0
        if exp_val:
            total_exp_val = db.session.query(func.sum(Ymp.export_val)).filter_by(year=year, month=0, hs_id_len=2).scalar()
            exp_pct=(exp_val / total_exp_val) * 100
            exp_pct="{:.2g}%".format(exp_pct) if exp_pct > 0.01 else _("less than 0.01%%")
        total_imp_val = Stat(self, "secex", "import_val", filter_attr=None).value()
        imp_pct = 0
        if imp_val:
            total_imp_val = db.session.query(func.sum(Ymp.import_val)).filter_by(year=year, month=0, hs_id_len=2).scalar()
            imp_pct=(imp_val / total_imp_val) * 100
            imp_pct="{:.2g}%".format(imp_pct) if imp_pct > 0.01 else _("less than 0.01%%")
        if exp_val and imp_val:
            p.append(_(u"%(prod)s represents %(exp_pct)s of the exports of %(location)s and %(imp_pct)s of its imports.",
                prod=hs.name(), exp_pct=exp_pct, location=location.name(), imp_pct=imp_pct))
        # new paragraph
        text.append(" ".join(p).strip()); p = []
        #___________________________________
        # RCA
        #-----------------------------------
        rca = Stat(self, "secex", "rca").value()
        num_bra_w_rca = len(Ymbp.query.filter_by(year=year, month=0, hs_id=hs.id, bra_id_len=9).filter(Ymbp.rca>=1).all())
        if num_bra_w_rca:
            if location.id == "sabra":
                num_munics_w_rca = len(Ymbp.query.filter_by(year=year, month=0, hs_id=hs.id, bra_id_len=9).filter(Ymbp.rca>=1).all())
                num_states_w_rca = len(Ymbp.query.filter_by(year=year, month=0, hs_id=hs.id, bra_id_len=3).filter(Ymbp.rca>=1).all())
                munic = translate("bra_9", n=num_munics_w_rca)
                state = translate("bra_3", n=num_states_w_rca)
                p.append(_(u"%(prod)s are exported with RCA (revealed comparative advantage) by %(num_states_w_rca)d %(state)s, " \
                    "and %(num_munics_w_rca)d %(munic)s in Brazil.",
                    prod=hs.name(), num_states_w_rca=num_states_w_rca, num_munics_w_rca=num_munics_w_rca, munic=munic,
                    location=location.name(), state=state))
            else:
                if len(location.id) == MUNIC:
                    bra_filter_id = location.id[:3]
                    bra_filter = attrs.Bra.query.get(bra_filter_id)
                else:
                    bra_filter_id = location.id
                    bra_filter = attrs.Bra.query.get(bra_filter_id)
                num_bra_w_rca_in_loc = len(Ymbp.query.filter_by(year=year, month=0, hs_id=hs.id, bra_id_len=9).filter(Ymbp.bra_id.startswith(bra_filter_id), Ymbp.rca>=1).all())
                p.append(_(u"%(prod)s are exported with RCA (revealed comparative advantage) by %(num_bra_w_rca)d municipalities in Brazil, " \
                    "and by %(num_bra_w_rca_in_loc)d municipalities in %(bra_filter)s.",
                    prod=hs.name(), num_bra_w_rca=num_bra_w_rca, num_bra_w_rca_in_loc=num_bra_w_rca_in_loc,
                    bra_filter=bra_filter.name()))
            text.append(" ".join(p).strip()); p = []
        #___________________________________
        # Top Municipalities
        #-----------------------------------
        export_bras, export_bras_num = Stat(self, "secex", "export_val", "top", "bra_id", attr=None).list(val_num_format="export_val", with_len=True, with_filter=True)
        import_bras, import_bras_num = Stat(self, "secex", "import_val", "top", "bra_id", attr=None).list(val_num_format="export_val", with_len=True, with_filter=True)
        if export_bras_num == 1:
            p.append(_(u"The only Brazilian municipality that exports %(prod)s is %(export_bras)s. ",
                prod=hs.name(), export_bras=export_bras))
        else:
            p.append(_(u"The top Brazilian municipalities that export %(prod)s are %(export_bras)s. ",
                prod=hs.name(), export_bras=export_bras))
        if import_bras_num == 1:
            p.append(_(u"The only Brazilian municipality that imports %(prod)s is %(import_bras)s.",
                prod=hs.name(), import_bras=import_bras))
        else:
            p.append(_(u"The top Brazilian municipalities that import %(prod)s are %(import_bras)s.",
                prod=hs.name(), import_bras=import_bras))
        text.append(" ".join(p).strip()); p = []
        #___________________________________
        # Top Destinations
        #-----------------------------------
        dests, dests_num = Stat(self, "secex", "export_val", "top", "wld_id").list(val_num_format="export_val", with_len=True, with_location=True)
        if dests:
            if dests_num == 1:
                p.append(_(u"The only international destination that imports %(prod)s exported by %(location)s is %(dests)s.",
                    prod=hs.name(), location=location.name(), dests=dests))
            else:
                p.append(_(u"The top international destinations that import %(prod)s exported by %(location)s are %(dests)s.",
                    prod=hs.name(), location=location.name(), dests=dests))
            text.append(" ".join(p).strip()); p = []
        #___________________________________
        # Complexity
        #-----------------------------------
        pci = Stat(self, "secex", "pci", attr=None).value()
        if pci:
            pci_rank, pci_total = Stat(self, "secex", "pci", "top", "hs_id", attr=None).rank(with_total=True)
            if pci_rank < (pci_total/2):
                pci_sentence = _(u"%(prod)s are a product with an above average complexity, ", prod=hs.name())
                if pci_rank < (pci_total/4):
                    pci_sentence = _(u"%(prod)s are a high complexity product, ", prod=hs.name())
            else:
                pci_sentence = _(u"%(prod)s are a product with a below average complexity, ", prod=hs.name())
                if pci_rank > (pci_total * 0.75):
                    pci_sentence = _(u"%(prod)s are a low complexity product, ", prod=hs.name())
            pci_sentence += _(u"ranking at number %(pci_rank)d (out of %(pci_total)d products in terms of " \
                u"product complexity with a product complexity index of %(pci).3f).",
                prod=hs.name(), pci_rank=pci_rank, pci_total=pci_total, pci=pci)
            p.append(pci_sentence)
            text.append(" ".join(p).strip()); p = []
        #___________________________________
        # Intro
        #-----------------------------------
        # if len(hs.id) == SECTION:
        #     hs_section = hs
        #     p.append(_(u"%(prod)s are a top level product section in the Harmonized System (HS) classification.",
        #         prod=hs.name()))
        # else:
        #     hs_section = attrs.Hs.query.get(hs.id[:2])
        #     p.append(_(u"%(prod)s are a product in the Harmonized System (HS) classification " \
        #         u"found in the %(section)s section with a %(id_len)s digit ID of %(id)s.",
        #         prod=hs.name(), section=hs_section.name(), id_len=len(hs.display_id()), id=hs.display_id()))
        #     #___________________________________
        #     # Get other producst in section
        #     #-----------------------------------
        #     show_attr_type = "hs_id.{0}.{1}".format(len(hs.id), hs.id[:2])
        #     prods_in_section = Stat(self, "secex", "export_val", "top", show_attr_type, num_items=2, exclude=hs.id).value()
        #     prods_in_section = [u"<a href='{0}'>{1}</a>".format(prod[0].url(), prod[0].name()) for prod in prods_in_section]
        #     prods_in_section = " and ".join(prods_in_section)
        #     num_in_section = attrs.Hs.query.filter(attrs.Hs.id.startswith(hs.id[:2]), func.char_length(attrs.Hs.id)==len(hs.id)).all()
        #     num_in_section = len(num_in_section) - 3
        #     p.append(_(u"This section also includes %(prods_in_section)s among %(num_in_section)d others.",
        #         prods_in_section=prods_in_section, num_in_section=num_in_section))
        #     #___________________________________
        #     # Most similar
        #     #-----------------------------------
        #     similar = hs.get_similar()
        #     similar = [u"<a href='{}'>{}</a>".format(s.hs.url(), s.hs.name()) for s in similar]
        #     similar = u"{0} {1} {2}".format(", ".join(similar[:-1]), gettext("and"), similar[-1])
        #     p.append(_(u"With regard to other locations that export this product, it is most closely related to %(similar)s.",
        #         similar=similar))
        # # new paragraph
        # text.append(" ".join(p).strip()); p = []
        #___________________________________
        # Exports
        #-----------------------------------
        # exp = Stat(self, "secex", "export_val").format() or "$0 USD"
        # imp = Stat(self, "secex", "import_val").format() or "$0 USD"
        # year = Stat(self, "secex", "export_val").year()
        # exp_val = Stat(self, "secex", "export_val").value()
        # imp_val = Stat(self, "secex", "import_val").value()
        # raise Exception(exp_val, Stat(self, "secex", "export_val", filter_attr=None).value())
        # if exp_val and imp_val:
        #     ratio = max(exp_val, imp_val) / min(exp_val, imp_val)
        #     t_balance = gettext("exports") if exp_val > imp_val else gettext("imports")
        #     text.append(gettext(u"In %(year)s %(location)s exported %(exp)s and imported %(imp)s, " \
        #         "making the balance of trade %(ratio).2g to 1 in favor of %(t_balance)s.",
        #         year=year, location=location.name(), exp=exp, imp=imp, ratio=ratio, t_balance=t_balance))
        # elif exp_val:
        #     text.append(gettext(u"In %(year)s %(location)s exported %(exp)s and did not import any products.",
        #         year=year, bra=location.name(), exp=exp))
        # elif imp_val:
        #     text.append(gettext(u"In %(year)s %(location)s imported %(imp)s and did not export any products.",
        #         year=year, bra=location.name(), imp=imp))
        # else:
        #     return [gettext(u"In %(year)s %(bra)s had no exports or imports.", year=year, bra=bra.name())]
        #___________________________________
        # Exports as %
        #-----------------------------------
        # total_exp_val = Stat(BraProfile(location.id), "secex", "export_val").value()

        # raise Exception(text)
        return text
