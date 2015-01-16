# -*- coding: utf-8 -*-
from dataviva import db
from sqlalchemy import func
from flask.ext.babel import gettext as _
from dataviva.attrs import models as attrs
from dataviva.profile.profiles import Profile
from dataviva.profile.stat import Stat
from dataviva.utils.num_format import num_format
from dataviva.visualize.build_models import *
from dataviva.rais.models import Yo

class CboProfile(Profile):
    """A CBO occupation profile, which extends from the parent profile class.
        instantiate like: CboProfile(), CboProfile('1227') or
        CboProfile('1227', 'mg')
    """

    def __init__(self, cbo_id=None, bra_id=None):
        """Defaults to most ubiquitous occupation = Administrative Assistants"""
        cbo_id = cbo_id or "4110"
        attr_type = "bra" if bra_id else "wld"
        bra_id = bra_id if bra_id else "sabra"
        super(CboProfile, self).__init__(attr_type, bra_id, "cbo", cbo_id)

    def title_stem(self):
        if self.attr == "<bra>" or self.attr.id != "sabra":
            return gettext("<cbo> <bra_article_in>")
        else:
            return gettext("<cbo>")

    def sections(self):

        cnae_depth = attrs.Cnae.depths[-1]

        s = [
            {
                "title": gettext("Economic Activity"),
                "anchor": "econ",
                "sections": [
                    {
                        "title": gettext("Industries"),
                        "anchor": "cnae",
                        "builds": [
                            Line("rais", {"bra": self.attr, "cbo": self.filter_attr}, "cnae", y="wage_avg"),
                            TreeMap("rais", {"bra": self.attr, "cbo": self.filter_attr}, "cnae")
                        ]
                    }
                ]
            },
            {
                "title": gettext("Demographics"),
                "anchor": "demo",
                "sections": [
                    {
                        "title": gettext("Gender Wage Gaps"),
                        "anchor": "gender",
                        "builds": [
                            Bar("rais", {"bra": self.attr, "cbo": self.filter_attr, "demo": "gender"}, "cnae", x="cnae_{0}".format(cnae_depth), y="wage_avg", limit=10, order="num_emp"),
                            Bar("rais", {"bra": self.attr, "cbo": self.filter_attr, "demo": "gender"}, "cnae", x="cnae_{0}".format(cnae_depth), y="wage_avg", limit=10, order="wage_avg")
                        ]
                    },
                    {
                        "title": gettext("Ethnicity Wage Gaps"),
                        "anchor": "ethnicity",
                        "builds": [
                            Bar("rais", {"bra": self.attr, "cbo": self.filter_attr, "demo": "ethnicity"}, "cnae", x="cnae_{0}".format(cnae_depth), y="wage_avg", limit=10, order="num_emp"),
                            Bar("rais", {"bra": self.attr, "cbo": self.filter_attr, "demo": "ethnicity"}, "cnae", x="cnae_{0}".format(cnae_depth), y="wage_avg", limit=10, order="wage_avg")
                        ]
                    }
                ]
            }
        ]

        if len(self.attr.id) < 9:
            s[0]["sections"].append({
                "title": gettext("Locations"),
                "anchor": "bra",
                "builds": [
                    Line("rais", {"bra": self.attr, "cbo": self.filter_attr}, "bra", y="wage_avg"),
                    Stacked("rais", {"bra": self.attr, "cbo": self.filter_attr}, "bra", y="num_emp")
                ]
            })

        if len(self.filter_attr.id) == 4:
            s.append({
                "title": gettext("Related Occupations"),
                "anchor": "related",
                "builds": [
                    Rings("rais", {"bra": self.attr}, "cbo", focus=self.filter_attr)
                ]
            })

        return s

    def headlines(self):
        return [
            Stat(self, "rais", "num_emp"),
            Stat(self, "rais", "wage_avg"),
            # Stat(self, "rais", "maleRatio"),
            Stat(self, "rais", "num_emp", type="top", output="cnae", num_items=1)
        ]

    def stats(self):
        return [
            {
                "title": gettext("Population"),
                "stats": [
                    Stat(self, "attr", "pop"),
                    Stat(self, "attr", "pop_eligible"),
                    Stat(self, "attr", "pop_active"),
                    Stat(self, "attr", "pop_employed")
                ],
                "col": 1
            },
            {
                "title": gettext("Economy"),
                "stats": [
                    Stat(self, "rais", "wage_avg"),
                    Stat(self, "rais", "num_emp"),
                    Stat(self, "attr", "prox"),
                    Stat(self, "rais", "num_emp", type="top", output="cnae"),
                    Stat(self, "attr", "neighbors")
                ],
                "col": 2,
                "width": 3
            }
        ]

    def summary(self):
        p, text = [], []
        location = self.attr
        cbo = self.filter_attr
        REGION, STATE, MESO, MICRO, PLN_REG, MUNIC = 1, 3, 5, 7, 8, 9
        MAIN_GROUP, FAMILY = 1, 4
        #___________________________________
        # Overview
        #-----------------------------------
        num_emp = Stat(self, "rais", "num_emp").value()
        year = Stat(self, "rais", "num_emp").year()
        if num_emp:
            if location.id == "sabra":
                total_num_emp = db.session.query(func.sum(Yo.num_emp)).filter_by(year=year, cbo_id_len=1).scalar()
            else:
                total_num_emp = Stat(self, "rais", "num_emp", filter_attr=None).value()
            rank, rank_total = Stat(self, "rais", "wage", "top", "cbo_id.{}".format(len(cbo.id))).rank(with_total=True)
            if rank <= (rank_total/2):
                lg_or_sm = _("largest")
            else:
                lg_or_sm = _("smallest")
                rank = rank_total - rank
            rank = "" if rank == 1 else num_format(rank, "ordinal")
            p.append(_(u"%(occupation)s are the %(rank)s %(lg_or_sm)s occupation in %(location)s by number of employees.",
                occupation=cbo.name(), rank=rank, lg_or_sm=lg_or_sm, location=location.name()))
            num_est = Stat(self, "rais", "num_est").format()
            wage_avg = Stat(self, "rais", "wage_avg").value()
            p.append(_(u"In %(location)s there are %(num_emp)s %(occupation)s in %(num_est)s " \
                u"establishments that receive an average monthly wage of %(wage_avg)s.",
                occupation=cbo.name(), location=location.name(), num_est=num_est, num_emp=num_format(num_emp),
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
                    employees = _(u"%(demonym)s %(occupation)s", demonym=demonym, occupation=cbo.name())
                else:
                    employees = _(u"%(occupation)s in %(location)s", occupation=cbo.name(), location=location.name())
                p.append(_(u"Compared to the national average (%(bra_wage_avg)s), %(employees)s " \
                u"are paid roughly %(ratio).3g times %(more_or_less)s.",
                bra_wage_avg=num_format(bra_wage_avg, "wage"), employees=employees, ratio=ratio, more_or_less=more_or_less))
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
                    bra_wage_avg=num_format(state_wage_avg, "wage"), state=state_link, employees=employees, ratio=ratio, more_or_less=more_or_less))
        # new paragraph
        text.append(" ".join(p).strip()); p = []
        #___________________________________
        # Occupations
        #-----------------------------------
        common_cnae = Stat(self, "rais", "num_emp", "top", "cnae_id").list(val_num_format="num_emp", with_location=True)
        if common_cnae:
            p.append(_(u"In %(location)s the industries that employ the highest number of %(occupation)s are %(common_cnae)s.",
                location=location.name(), occupation=cbo.name(), common_cnae=common_cnae))
        rich_cnaes = Stat(self, "rais", "wage_avg", "top", "cnae_id").list(val_num_format="wage", with_location=True)
        if rich_cnaes:
            p.append(_(u"Whereas the industries that pay the highest wages to %(occupation)s in %(location)s are %(rich_cnaes)s.",
                occupation=cbo.name(), location=location.name(), rich_cnaes=rich_cnaes))
        # new paragraph
        text.append(" ".join(p).strip()); p = []
        #___________________________________
        # Demographics: gender
        #-----------------------------------
        m_wage = Stat(self, "rais", "wage_avg", "val", "d_id.A", attr=None).value()
        f_wage = Stat(self, "rais", "wage_avg", "val", "d_id.B", attr=None).value()
        if m_wage and f_wage:
            higher_paid_gender = _("women") if f_wage > m_wage else _("men")
            ratio = max(m_wage, f_wage) / min(m_wage, f_wage)
            p.append(_(u"The average monthly wage for male %(occupation)s in Brazil is %(m_wage)s, " \
                u"whereas female %(occupation)s are paid %(f_wage)s on average. This means that, on average, " \
                u"%(higher_paid_gender)s are paid %(ratio).3g times more.",
                occupation=cbo.name(), m_wage=num_format(m_wage, "wage"),
                f_wage=num_format(f_wage, "wage"), higher_paid_gender=higher_paid_gender, ratio=ratio))
        elif m_wage or f_wage:
            gender = _("male") if m_wage else _("female")
            opposite_gender = _("female") if m_wage else _("male")
            wage = m_wage or f_wage
            p.append(_(u"The average monthly wage for %(gender)s %(occupation)s in Brazil is %(wage)s, " \
                u"there are no %(opposite_gender)s %(occupation)s employed in Brazil.",
                gender=gender, occupation=cbo.name(), wage=num_format(wage, "wage"), opposite_gender=opposite_gender))
        if location.id != "sabra":
            m_wage = Stat(self, "rais", "wage_avg", "val", "d_id.A").value()
            f_wage = Stat(self, "rais", "wage_avg", "val", "d_id.B").value()
            if m_wage and f_wage:
                higher_paid_gender = _("women") if f_wage > m_wage else _("men")
                ratio = max(m_wage, f_wage) / min(m_wage, f_wage)
                p.append(_(u"In %(location)s the average wage for male %(occupation)s is %(m_wage)s, " \
                    u"while female %(occupation)s are paid %(f_wage)s on average. This means that, on average, " \
                    u"%(higher_paid_gender)s in %(location)s are paid %(ratio).3g times more.",
                    location=location.name(), occupation=cbo.name(), m_wage=num_format(m_wage, "wage"),
                    f_wage=num_format(f_wage, "wage"), higher_paid_gender=higher_paid_gender, ratio=ratio))
            elif m_wage or f_wage:
                gender = _("male") if m_wage else _("female")
                opposite_gender = _("female") if m_wage else _("male")
                wage = m_wage or f_wage
                p.append(_(u"In %(location)s the average wage for %(gender)s %(occupation)s is %(wage)s, " \
                    u"there are no %(opposite_gender)s %(occupation)s employed in %(location)s.",
                    location=location.name(), gender=gender, occupation=cbo.name(), wage=num_format(wage, "wage"),
                    opposite_gender=opposite_gender))
        text.append(" ".join(p).strip()); p = []
        #___________________________________
        # Demographics: ethnicity
        #-----------------------------------
        wages_by_eth = Stat(self, "rais", "wage_avg", "top", "d_id.ethnicity", exclude="H").value()
        if wages_by_eth:
            rich_eth, rich_eth_wage = wages_by_eth.pop(0)
            rich_ratio = max(rich_eth_wage, wage_avg) / min(rich_eth_wage, wage_avg)
            rich_lower_or_higher = _("lower") if wage_avg > rich_eth_wage else _("higher")
            p.append(_(u"In %(location)s, %(rich_eth)s %(occupation)s " \
                u"are paid the highest average wage of %(rich_eth_wage)s which is %(rich_ratio).3g times " \
                u"%(rich_lower_or_higher)s than the average wage of %(wage_avg)s.",
                location=location.name(), occupation=cbo.name(), rich_eth=rich_eth.name().lower(),
                rich_eth_wage=num_format(rich_eth_wage, "wage"), rich_ratio=rich_ratio,
                rich_lower_or_higher=rich_lower_or_higher, wage_avg=num_format(wage_avg, "wage")))
            if wages_by_eth:
                eths = []
                for i, eth in enumerate(wages_by_eth):
                    eth, eth_wage = eth
                    ethname = eth.name().lower() if i != 0 else eth.name()
                    ratio = max(eth_wage, wage_avg) / min(eth_wage, wage_avg)
                    more_or_less = _("less") if wage_avg > eth_wage else _("more")
                    eths.append(_(u"%(eth)s employees are paid %(ratio).3g times %(more_or_less)s (%(eth_wage)s)",
                        eth=ethname, ratio=ratio, more_or_less=more_or_less,
                        eth_wage=num_format(eth_wage, "wage")))
                p.append(u"{} {} {}.".format(", ".join(eths[:-1]), gettext("and"), eths[-1]))
        text.append(" ".join(p).strip()); p = []
        return text
