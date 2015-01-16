# -*- coding: utf-8 -*-
from dataviva import db
from sqlalchemy import func
from flask.ext.babel import gettext as _
from dataviva.attrs import models as attrs
from dataviva.profile.profiles import Profile
from dataviva.profile.stat import Stat
from dataviva.translations.translate import translate
from dataviva.utils.num_format import num_format
from dataviva.visualize.build_models import *
from dataviva.rais.models import Yi

class CnaeProfile(Profile):
    """A CNAE industry profile, which extends from the parent profile class.
        instantiate like: CnaeProfile(), CnaeProfile('a01113') or
        CnaeProfile('a01113', 'mg')
    """

    def __init__(self, cnae_id=None, bra_id=None):
        """Defaults to most ubiquitous industry = Manufacture of work clothes"""
        cnae_id = cnae_id or "c14134"
        attr_type = "bra" if bra_id else "wld"
        bra_id = bra_id if bra_id else "sabra"
        super(CnaeProfile, self).__init__(attr_type, bra_id, "cnae", cnae_id)

    def title_stem(self):
        if self.attr == "<bra>" or self.attr.id != "sabra":
            return gettext("<cnae> <bra_article_in>")
        else:
            return gettext("<cnae>")

    def sections(self):

        cbo_depth = attrs.Cbo.depths[-1]

        s = [
            {
                "title": gettext("Demographic Breakdown"),
                "anchor": "demo",
                "sections": [
                    {
                        "title": gettext("Common Occupations"),
                        "anchor": "num_emp",
                        "builds": [
                            Bar("rais", {"bra": self.attr, "cnae": self.filter_attr, "demo": "gender"}, "cbo", x="cbo_{0}".format(cbo_depth), y="wage_avg", limit=10, order="num_emp", exclude="xxxx"),
                            Bar("rais", {"bra": self.attr, "cnae": self.filter_attr, "demo": "ethnicity"}, "cbo", x="cbo_{0}".format(cbo_depth), y="wage_avg", limit=10, order="num_emp", exclude="xxxx"),
                        ]
                    },
                    {
                        "title": gettext("Highest Paid Occupations"),
                        "anchor": "wage_avg",
                        "builds": [
                            Bar("rais", {"bra": self.attr, "cnae": self.filter_attr, "demo": "gender"}, "cbo", x="cbo_{0}".format(cbo_depth), y="wage_avg", limit=10, order="wage_avg", exclude="xxxx"),
                            Bar("rais", {"bra": self.attr, "cnae": self.filter_attr, "demo": "ethnicity"}, "cbo", x="cbo_{0}".format(cbo_depth), y="wage_avg", limit=10, order="wage_avg", exclude="xxxx"),
                        ]
                    }
                ]
            }
        ]

        if len(self.attr.id) < 9:
            s.insert(0,{
                "title": gettext("Locations"),
                "anchor": "bra",
                "builds": [
                    Line("rais", {"bra": self.attr, "cnae": self.filter_attr}, "bra", y="num_emp"),
                    TreeMap("rais", {"bra": self.attr, "cnae": self.filter_attr}, "bra")
                ]
            })

        if len(self.filter_attr.id) == 6:
            s.append({
                "title": gettext("Related Industries"),
                "anchor": "related",
                "builds": [
                    Rings("rais", {"bra": self.attr}, "cnae", focus=self.filter_attr)
                ]
            })

        return s

    def headlines(self):
        return [
            Stat(self, "rais", "num_emp"),
            Stat(self, "rais", "wage_avg"),
            Stat(self, "rais", "num_emp_growth"),
            Stat(self, "rais", "num_emp", "top", "cbo_id", num_items=1)
            # Stat(self, "rais", "num_cbo_id"),
            # Stat(self, "rais", "num_est_size")
        ]

    def stats(self):
        return [
            {
                "title": gettext("Population"),
                "stats": [
                    Stat(self, "attr", "pop"),
                    Stat(self, "attr", "pop_active"),
                    Stat(self, "attr", "pop_eligible"),
                    Stat(self, "attr", "pop_employed")
                ],
                "col": 1,
            },
            {
                "title": gettext("Economy"),
                "stats": [
                    Stat(self, "attr", "gdp"),
                    Stat(self, "attr", "gdp_per_capita"),
                    Stat(self, "rais", "num_emp"),
                    Stat(self, "rais", "num_est"),
                    Stat(self, "rais", "wage_avg"),
                    Stat(self, "rais", "num_emp", type="top", output="cbo"),
                    Stat(self, "attr", "prox"),
                    Stat(self, "ei", "purchase_value", type="top", ei_flow="r", output="hs"),
                    Stat(self, "ei", "purchase_value", type="top", ei_flow="s", output="hs")
                ],
                "col": 2,
                "width": 3
            }
        ]

    def summary(self):
        p, text = [], []
        location = self.attr
        cnae = self.filter_attr
        REGION, STATE, MESO, MICRO, PLN_REG, MUNIC = 1, 3, 5, 7, 8, 9
        SECTION, DIVISION, CLASS = 1, 3, 6
        #___________________________________
        # Overview
        #-----------------------------------
        num_emp = Stat(self, "rais", "num_emp").value()
        year = Stat(self, "rais", "num_emp").year()
        if num_emp:
            if location.id == "sabra":
                total_num_emp = db.session.query(func.sum(Yi.num_emp)).filter_by(year=year, cnae_id_len=1).scalar()
            else:
                total_num_emp = Stat(self, "rais", "num_emp", filter_attr=None).value()
            rank, rank_total = Stat(self, "rais", "wage", "top", "cnae_id.{}".format(len(cnae.id))).rank(with_total=True)
            if rank <= (rank_total/2):
                lg_or_sm = _("largest")
            else:
                lg_or_sm = _("smallest")
                rank = rank_total - rank
            rank = "" if rank == 1 else num_format(rank, "ordinal")
            p.append(_(u"The %(industry)s industry is the %(rank)s %(lg_or_sm)s industry in %(location)s by number of employees.",
                industry=cnae.name(), rank=rank, lg_or_sm=lg_or_sm, location=location.name()))
            num_est = Stat(self, "rais", "num_est").format()
            wage_avg = Stat(self, "rais", "wage_avg").value()
            p.append(_(u"In %(location)s there are %(num_est)s %(industry)s establishments that " \
                u"employ a total of %(num_emp)s and pay an average wage of %(wage_avg)s.",
                industry=cnae.name(), location=location.name(), num_est=num_est, num_emp=num_format(num_emp, "num_emp"),
                wage_avg=num_format(wage_avg, "wage")))
            if location.id != "sabra":
                bra_wage_avg = Stat(self, "rais", "wage_avg", attr=None).value()
                if bra_wage_avg < wage_avg:
                    more_or_less = "more"
                    ratio = wage_avg / bra_wage_avg
                else:
                    more_or_less = "less"
                    ratio = bra_wage_avg / wage_avg
                demonym = location.stats.demonym
                if demonym:
                    employees = _(u"%(demonym)s employees", demonym=demonym)
                else:
                    employees = _(u"employees in %(location)s", location=location.name())
                p.append(_(u"Compared to the national average (%(bra_wage_avg)s), %(employees)s " \
                u"are paid roughly %(ratio).3g times %(more_or_less)s.",
                bra_wage_avg=num_format(bra_wage_avg, "wage"), location=location.name(), 
                employees=employees, ratio=ratio, more_or_less=more_or_less))
                if len(location.id) > 3:
                    state = attrs.Bra.query.get(location.id[:3])
                    state_wage_avg = Stat(self, "rais", "wage_avg", attr=state).value()
                    state_link = u"<a href='{}'>{}</a>".format(state.url(), state.name())
                    if state_wage_avg < wage_avg:
                        more_or_less = "more"
                        ratio = wage_avg / state_wage_avg
                    else:
                        more_or_less = "less"
                        ratio = state_wage_avg / wage_avg
                    p.append(_(u"Compared to the state average in %(state)s (%(bra_wage_avg)s), %(employees)s " \
                    u"are paid roughly %(ratio).3g times %(more_or_less)s.",
                    bra_wage_avg=num_format(state_wage_avg, "wage"), state=state_link, location=location.name(), 
                    employees=employees, ratio=ratio, more_or_less=more_or_less))
        # new paragraph
        text.append(" ".join(p).strip()); p = []
        #___________________________________
        # Occupations
        #-----------------------------------
        important_cbos = Stat(self, "rais", "importance", "top", "cbo_id", attr=None).list(with_value=False)
        p.append(_(u"Nationally, the most important occupations in the %(industry)s industry are %(important_cbos)s.",
            industry=cnae.name(), important_cbos=important_cbos))
        common_cbos = Stat(self, "rais", "num_emp", "top", "cbo_id").list(val_num_format="num_emp", with_location=True)
        p.append(_(u"In %(location)s the most common occupations employed in this industry are %(common_cbos)s.",
            location=location.name(), common_cbos=common_cbos))
        rich_cbos = Stat(self, "rais", "wage_avg", "top", "cbo_id").list(val_num_format="wage", with_location=True)
        p.append(_(u"Whereas the highest paid occupations in the %(industry)s industry in %(location)s are %(rich_cbos)s.",
            industry=cnae.name(), location=location.name(), rich_cbos=rich_cbos))
        # new paragraph
        text.append(" ".join(p).strip()); p = []
        #___________________________________
        # Demographics: gender
        #-----------------------------------
        m_wage = Stat(self, "rais", "wage_avg", "val", "d_id.A", attr=None).value()
        f_wage = Stat(self, "rais", "wage_avg", "val", "d_id.B", attr=None).value()
        higher_paid_gender = _("women") if f_wage > m_wage else _("men")
        if m_wage and f_wage:
            ratio = max(m_wage, f_wage) / min(m_wage, f_wage)
            lower_paid_gender = _("women") if higher_paid_gender == _("men") else _("men")
            p.append(_(u"The average monthly wage in Brazil for men in the %(industry)s industry is %(m_wage)s, " \
                u"whereas women are paid %(f_wage)s on average. This means that " \
                u"%(higher_paid_gender)s are paid %(ratio).3g times more than %(lower_paid_gender)s.",
                industry=cnae.name(), m_wage=num_format(m_wage, "wage"),
                f_wage=num_format(f_wage, "wage"), higher_paid_gender=higher_paid_gender, ratio=ratio, lower_paid_gender=lower_paid_gender))
        elif m_wage or f_wage:
            gender = _("men") if m_wage else _("women")
            opposite_gender = _("women") if m_wage else _("men")
            wage = m_wage or f_wage
            p.append(_(u"The average monthly wage in Brazil for %(gender)s in the %(industry)s industry is %(wage)s, " \
                u"there are no %(opposite_gender)s employed in the %(industry)s industry in Brazil.",
                gender=gender, industry=cnae.name(), wage=num_format(wage, "wage"), opposite_gender=opposite_gender))
        if location.id != "sabra":
            m_wage = Stat(self, "rais", "wage_avg", "val", "d_id.A").value()
            f_wage = Stat(self, "rais", "wage_avg", "val", "d_id.B").value()
            if m_wage and f_wage:
                higher_paid_gender = _("women") if f_wage > m_wage else _("men")
                lower_paid_gender = _("women") if higher_paid_gender == _("men") else _("men")
                ratio = max(m_wage, f_wage) / min(m_wage, f_wage)
                p.append(_(u"In %(location)s the average monthly wage for men in the %(industry)s industry is %(m_wage)s, " \
                    u"while for women it is %(f_wage)s on average. This means that " \
                    u"%(higher_paid_gender)s in %(location)s are paid %(ratio).3g times more than %(lower_paid_gender)s.",
                    location=location.name(), industry=cnae.name(), m_wage=num_format(m_wage, "wage"),
                    f_wage=num_format(f_wage, "wage"), higher_paid_gender=higher_paid_gender, ratio=ratio, lower_paid_gender=lower_paid_gender))
            elif m_wage or f_wage:
                gender = _("men") if m_wage else _("women")
                opposite_gender = _("women") if m_wage else _("men")
                wage = m_wage or f_wage
                p.append(_(u"In %(location)s the average monthly wage for %(gender)s in the %(industry)s industry is %(wage)s, " \
                    u"there are no %(opposite_gender)s employed in the %(industry)s industry in %(location)s.",
                    location=location.name(), gender=gender, industry=cnae.name(), wage=num_format(wage, "wage"), opposite_gender=opposite_gender))
        text.append(" ".join(p).strip()); p = []
        #___________________________________
        # Demographics: ethnicity
        #-----------------------------------
        wages_by_eth = Stat(self, "rais", "wage_avg", "top", "d_id.ethnicity", exclude="H").value()
        wages_by_eth = [wbe for wbe in wages_by_eth if wbe[1] > 0]
        if wages_by_eth:
            rich_eth, rich_eth_wage = wages_by_eth.pop(0)
            rich_ratio = max(rich_eth_wage, wage_avg) / min(rich_eth_wage, wage_avg)
            rich_lower_or_higher = _("lower") if wage_avg > rich_eth_wage else _("higher")
            p.append(_(u"In %(location)s %(rich_eth)s employees in the %(industry)s " \
                u"industry are paid the highest average wage of %(rich_eth_wage)s which is %(rich_ratio).3g times " \
                u"%(rich_lower_or_higher)s than the average wage of %(wage_avg)s.",
                location=location.name(), industry=cnae.name(), rich_eth=rich_eth.name(),
                rich_eth_wage=num_format(rich_eth_wage, "wage"), rich_ratio=rich_ratio,
                rich_lower_or_higher=rich_lower_or_higher, wage_avg=num_format(wage_avg, "wage")))
            if len(wages_by_eth) > 1:
                eths = []
                for i, eth in enumerate(wages_by_eth):
                    eth, eth_wage = eth
                    ratio = max(eth_wage, wage_avg) / min(eth_wage, wage_avg)
                    more_or_less = _("less") if wage_avg > eth_wage else _("more")
                    eths.append(_(u"%(eth)s employees are paid %(ratio).3g times %(more_or_less)s (%(eth_wage)s)",
                        eth=eth.name(), ratio=ratio, more_or_less=more_or_less,
                        eth_wage=num_format(eth_wage, "wage")))
                p.append(u"{} {} {}.".format(", ".join(eths[:-1]), gettext("and"), eths[-1]))
            text.append(" ".join(p).strip()); p = []
        return text
