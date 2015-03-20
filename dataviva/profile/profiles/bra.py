# -*- coding: utf-8 -*-
from sqlalchemy import func
from flask.ext.babel import gettext
from dataviva.attrs import models as attrs
from dataviva.profile.profiles import Profile
from dataviva.profile.stat import Stat
from dataviva.visualize.build_models import *
from dataviva.translations.translate import translate
from dataviva.utils.num_format import num_format
from dataviva.secex.models import Ymbp
from dataviva.hedu.models import Yd

class BraProfile(Profile):
    """A Bra profile, which extends from the parent profile class.
        instantiate like: BraProfile('mg')
    """

    def __init__(self, bra_id=None):
        attr_type = "bra" if bra_id else "wld"
        bra_id = bra_id or "sabra"
        super(BraProfile, self).__init__(attr_type, bra_id)

    def title_stem(self):
        if self.attr == "<bra>":
            return "<bra>"
        else:
            name = self.attr.name()
            if len(self.attr.id) > 3:
                name = u"{0}, {1}".format(name, self.attr.id[1:3].upper())
            return name

    def next(self):
        next = attrs.Bra.query.with_entities(func.min(attrs.Bra.id)) \
                    .filter(func.char_length(attrs.Bra.id)==len(self.attr.id), attrs.Bra.id > self.attr.id).first()
        if next:
            return attrs.Bra.query.get(next[0])

    def prev(self):
        prev = attrs.Bra.query.with_entities(func.max(attrs.Bra.id)) \
                    .filter(func.char_length(attrs.Bra.id)==len(self.attr.id), attrs.Bra.id < self.attr.id).first()
        if prev:
            return attrs.Bra.query.get(prev[0])

    def sections(self):
        cbo_depth = attrs.Cbo.depths[-1]
        hedu_depth = attrs.Course_hedu.depths[-1]
        sc_depth = attrs.Course_sc.depths[-1]
        s = [
            {
                "title": gettext("Economy"),
                "anchor": "econ",
                "sections": [
                    {
                        "title": gettext("Employment"),
                        "anchor": "rais",
                        "summary": self.text_employment(),
                        "sections": [
                            {
                                "title": gettext("Occupations"),
                                "anchor": "rais_cbo",
                                "builds": [
                                    Line("rais", {"bra": self.attr}, "cbo", y="num_emp"),
                                    Line("rais", {"bra": self.attr}, "cbo", y="wage_avg"),
                                    TreeMap("rais", {"bra": self.attr}, "cbo", size="num_emp")
                                ]
                            },
                            {
                                "title": gettext("Gender Wage Gaps"),
                                "anchor": "rais_gender",
                                "builds": [
                                    Bar("rais", {"bra": self.attr, "demo": "gender"}, "cbo", x="cbo_{0}".format(cbo_depth), y="wage_avg", limit=10, order="wage_avg.A", exclude="xxxx"),
                                    Bar("rais", {"bra": self.attr, "demo": "gender"}, "cbo", x="cbo_{0}".format(cbo_depth), y="wage_avg", limit=10, order="wage_avg.B", exclude="xxxx"),
                                    Bar("rais", {"bra": self.attr, "demo": "gender"}, "cbo", x="cbo_{0}".format(cbo_depth), y="wage_avg", limit=10, order="num_emp", exclude="xxxx"),
                                    Bar("rais", {"bra": self.attr, "demo": "gender"}, "cbo", x="cbo_{0}".format(cbo_depth), y="wage_avg", limit=10, order="wage_avg", exclude="xxxx")
                                ]
                            },
                            {
                                "title": gettext("Ethnicity Wage Gaps"),
                                "anchor": "rais_ethnicity",
                                "builds": [
                                    Bar("rais", {"bra": self.attr, "demo": "ethnicity"}, "cbo", x="cbo_{0}".format(cbo_depth), y="wage_avg", limit=10, order="num_emp", exclude="xxxx"),
                                    Bar("rais", {"bra": self.attr, "demo": "ethnicity"}, "cbo", x="cbo_{0}".format(cbo_depth), y="wage_avg", limit=10, order="wage_avg", exclude="xxxx")
                                ]
                            },
                            # {
                            #     "title": gettext("Wage Dynamics"),
                            #     "builds": [
                            #         Bar("rais", {"bra": self.attr}, "cbo", x="cbo_{0}".format(cbo_depth), y="wage_growth_10", limit=10, order="wage_growth_10")
                            #     ]
                            # }
                        ]
                    },
                    {
                        "title": gettext("International Trade"),
                        "anchor": "secex",
                        "summary": self.text_intl_trade(),
                        "sections": [
                            {
                                "title": gettext("Exports and Imports"),
                                "anchor": "secex_hs",
                                "builds": [
                                    TreeMap("secex", {"bra": self.attr}, "hs", size="export_val"),
                                    TreeMap("secex", {"bra": self.attr}, "hs", size="import_val")
                                    # TreeMap("secex", {"bra": self.attr, "hs": "<hs>"}, "wld", size="export_val"),
                                ]
                            },
                            {
                                "title": gettext("Destinations and Origins"),
                                "anchor": "secex_wld",
                                "builds": [
                                    TreeMap("secex", {"bra": self.attr}, "wld", size="export_val"),
                                    TreeMap("secex", {"bra": self.attr}, "wld", size="import_val")
                                    # TreeMap("secex", {"bra": self.attr, "wld": "<wld>"}, "hs", size="export_val")
                                ]
                            }
                        ]
                    },
                    # {
                    #     "title": gettext("Domestic Economy"),
                    #     "anchor": "ei",
                    #     "builds": [
                    #         TreeMap("rais", {"bra": self.attr}, "cnae", size="num_emp"),
                    #         TreeMap("ei", {"bra_s": self.attr}, "hs"),
                    #         TreeMap("ei", {"bra_r": self.attr}, "hs"),
                    #         TreeMap("ei", {"bra_r": self.attr}, "bra_s"),
                    #         TreeMap("ei", {"bra_s": self.attr}, "bra_r")
                    #     ]
                    # },
                    {
                        "title": gettext("Economic Opportunities"),
                        "anchor": "opp",
                        "sections": [
                            {
                                "title": gettext("Product Space"),
                                "anchor": "opp_hs",
                                "builds": [
                                    Network("secex", {"bra": self.attr}, "hs")
                                ]
                            },
                            {
                                "title": gettext("Industry Space"),
                                "anchor": "opp_cnae",
                                "builds": [
                                    Network("rais", {"bra": self.attr}, "cnae")
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "title": gettext("Education"),
                "anchor": "edu",
                "sections": [
                    {
                        "title": gettext("School Census"),
                        "anchor": "sc",
                        "summary": self.text_sc(),
                        "builds": [
                            Bar("sc", {"bra": self.attr, "course_sc": "xx", "demo": "ethnicity"}, "course_sc", x="course_sc_{0}".format(sc_depth), y="enrolled")
                        ]
                    }
                ]
            }
        ]

        num_courses = Stat(self, "hedu", "enrolled", "top", "course_hedu_id", num_items=11).value()

        if num_courses and len(num_courses) > 0:
            s[-1]["sections"].insert(0, {
                    "title": gettext("Higher Education"),
                    "anchor": "hedu",
                    "summary": self.text_hedu(),
                    "sections": [
                        {
                            "title": gettext("University Majors"),
                            "anchor": "hedu_course",
                            "builds": [
                                Line("hedu", {"bra": self.attr}, "course_hedu", y="graduates"),
                                TreeMap("hedu", {"bra": self.attr}, "course_hedu", size="graduates")
                            ]
                        },
                        {
                            "title": gettext("Gender Gaps"),
                            "anchor": "hedu_gender",
                            "builds": []
                        }
                    ]
            })
            if num_courses > 10:
                s[-1]["sections"][0]["sections"][1]["builds"].append(
                    Bar("hedu", {"bra": self.attr, "demo": "gender"}, "course_hedu", x="course_hedu_{0}".format(hedu_depth), y="enrolled", limit=10, order="enrolled.A")
                )
                s[-1]["sections"][0]["sections"][1]["builds"].append(
                    Bar("hedu", {"bra": self.attr, "demo": "gender"}, "course_hedu", x="course_hedu_{0}".format(hedu_depth), y="enrolled", limit=10, order="enrolled.B")
                )
            else:
                s[-1]["sections"][0]["sections"][1]["builds"].append(
                    Bar("hedu", {"bra": self.attr, "demo": "gender"}, "course_hedu", x="course_hedu_{0}".format(hedu_depth), y="enrolled", order="enrolled")
                )

        return s

    def headlines(self):
        return [
            Stat(self, "attr", "pop"),
            Stat(self, "rais", "wage"),
            Stat(self, "secex", "export_val"),
            Stat(self, "attr", "gdp_per_capita")
        ]

    def stats(self):
        return [
            {
                "title": gettext("Population"),
                "stats": [
                    Stat(self, "attr", "pop"),
                    Stat(self, "attr", "pop_density"),
                    Stat(self, "attr", "pop_100km"),
                    Stat(self, "attr", "pop_active")
                ],
                "col": 1
            },
            {
                "title": gettext("HDI"),
                "stats": [
                    Stat(self, "attr", "hdi"),
                    Stat(self, "attr", "hdi_edu"),
                    Stat(self, "attr", "hdi_health"),
                    Stat(self, "attr", "hdi_income")
                ],
                "col": 1
            },
            {
                "title": gettext("Geography"),
                "stats": [
                    Stat(self, "attr", "capital_dist"),
                    Stat(self, "attr", "demonym"),
                    Stat(self, "attr", "climate"),
                    Stat(self, "attr", "elevation"),
                    Stat(self, "attr", "airport_dist"),
                    Stat(self, "attr", "seaport_dist"),
                    Stat(self, "attr", "neighbors")
                ],
                "col": 1
            },
            {
                "title": gettext("Economy"),
                "stats": [
                    Stat(self, "attr", "gdp"),
                    Stat(self, "attr", "gdp_per_capita"),
                    Stat(self, "secex", "import_val", type="top", output="hs_id"),
                    Stat(self, "secex", "export_val", type="top", output="hs_id"),
                    Stat(self, "rais", "num_emp", type="top", output="cnae_id")
                ],
                "col": 2,
                "width": 3
            },
            {
                "title": gettext("Employment"),
                "stats": [
                    Stat(self, "rais", "wage"),
                    Stat(self, "rais", "wage_avg"),
                    Stat(self, "attr", "pop_employed"),
                    Stat(self, "attr", "pop_eligible"),
                    Stat(self, "attr", "pop_active"),
                    Stat(self, "rais", "num_emp", type="top", output="cbo_id")
                ],
                "col": 2
            },
            {
                "title": gettext("Education"),
                "stats": [
                    Stat(self, "hedu", "num_universities"),
                    Stat(self, "hedu", "enrolled", type="top", output="course_hedu_id"),
                    Stat(self, "hedu", "enrolled", type="top", output="university_id")
                ],
                "col": 2
            }
        ]

    def text_employment(self):
        bra = self.attr
        num_emp = Stat(self, "rais", "num_emp").format(labels=True)
        top_cat = Stat(self, "rais", "num_emp", "top", "cbo_id.1", num_items=1).value()[0]
        top_cat = u"<a href='{0}'>{1}</a> ({2})".format(top_cat[0].url(bra), top_cat[0].name(), num_format(top_cat[1], "num_emp"))
        genders = Stat(self, "rais", "num_emp", "top", "d_id.gender").value()
        dom_gender = max(genders, key=lambda g:g[1])
        non_dom_gender = min(genders, key=lambda g:g[1])
        gender_ratio = dom_gender[1] / float(non_dom_gender[1])
        top_occ = Stat(self, "rais", "num_emp", "top", "cbo_id", num_items=1).value()[0]
        top_occ = u"<a href='{0}'>{1}</a> ({2})".format(top_occ[0].url(bra), top_occ[0].name(), num_format(top_occ[1], "num_emp"))
        rich_occ, rich_occ_wage = Stat(self, "rais", "wage_avg", "top", "cbo_id").value()[0]
        rich_occ = u"<a href='{0}'>{1}</a>".format(rich_occ.url(bra), rich_occ.name())
        rich_occ_wage = num_format(rich_occ_wage, "wage")
        text = gettext(u"%(bra)s employs %(num_emp)s, the majority of which work as %(top_cat)s. " \
            "%(dom_gender)s outnumber %(non_dom_gender)s in the workforce by a factor of %(gender_ratio).2f to 1. " \
            "The most common occupation in %(bra)s is %(top_occ)s, " \
            "whereas the highest paid occupation is %(rich_occ)s, which are compensated on average with %(rich_occ_wage)s per month.",
            bra=bra.name(), num_emp=num_emp, top_cat=top_cat, dom_gender=dom_gender[0].name(),
            non_dom_gender=non_dom_gender[0].name(), gender_ratio=gender_ratio, top_occ=top_occ,
            rich_occ=rich_occ, rich_occ_wage=rich_occ_wage)
        return [text]

    def text_intl_trade(self):
        text = []
        bra = self.attr
        exp_stat = Stat(self, "secex", "export_val")
        imp_stat = Stat(self, "secex", "import_val")
        exp = exp_stat.format() or "$0 USD"
        imp = imp_stat.format() or "$0 USD"
        year = exp_stat.year()
        exp_val = exp_stat.value()
        imp_val = imp_stat.value()
        if exp_val and imp_val:
            ratio = max(exp_val, imp_val) / min(exp_val, imp_val)
            if float("{:.2g}".format(ratio)) == 1:
                text.append(gettext(u"In %(year)s %(bra)s exported %(exp)s and imported %(imp)s, " \
                    "making the balance of trade between exports and imports roughly equal.",
                    year=year, bra=bra.name(), exp=exp, imp=imp))
            else:
                t_balance = gettext("exports") if exp_val > imp_val else gettext("imports")
                text.append(gettext(u"In %(year)s %(bra)s exported %(exp)s and imported %(imp)s, " \
                    "making the balance of trade %(ratio)d to 1 in favor of %(t_balance)s.",
                    year=year, bra=bra.name(), exp=exp, imp=imp, ratio=ratio, t_balance=t_balance))
        elif exp_val:
            text.append(gettext(u"In %(year)s %(bra)s exported %(exp)s and did not import any products.",
                year=year, bra=bra.name(), exp=exp))
        elif imp_val:
            text.append(gettext(u"In %(year)s %(bra)s imported %(imp)s and did not export any products.",
                year=year, bra=bra.name(), imp=imp))
        else:
            return [gettext(u"In %(year)s %(bra)s had no exports or imports.", year=year, bra=bra.name())]
        #___________________________________
        # Top exports
        #-----------------------------------
        if exp_val:
            num_exp_w_rca = len(Ymbp.query.filter_by(year=year, month=0, bra_id=self.attr.id).filter(Ymbp.rca>=1).all())
            exp_list = Stat(self, "secex", "export_val", "top", "hs_id").value()
            exp_list = [u"<a href='{0}'>{1}</a> ({2})".format(e[0].url(bra), e[0].name(), num_format(e[1], "export_val")) for e in exp_list]
            exp_list = u"{0} {1} {2}".format(", ".join(exp_list[:-1]), gettext("and"), exp_list[-1])
            dest_list = Stat(self, "secex", "export_val", "top", "wld_id").value()
            dest_list = [u"<a href='{0}'>{1}</a> ({2})".format(d[0].url(bra), d[0].name(), num_format(d[1], "export_val")) for d in dest_list]
            dest_list = u"{0} {1} {2}".format(", ".join(dest_list[:-1]), gettext("and"), dest_list[-1])
            text.append(gettext(u"%(bra)s exports include %(num_exp_w_rca)s products (exported with revealed comparative advantage) " \
                "which include predominantly %(exp_list)s. The top five destinations of the products exported by %(bra)s are: %(dest_list)s.",
                bra=bra.name(), num_exp_w_rca=num_exp_w_rca, exp_list=exp_list, dest_list=dest_list))
        #___________________________________
        # Top imports
        #-----------------------------------
        if imp_val:
            imp_list = Stat(self, "secex", "import_val", "top", "hs_id").value()
            imp_list = [u"<a href='{0}'>{1}</a> ({2})".format(i[0].url(bra), i[0].name(), num_format(i[1], "export_val")) for i in imp_list]
            imp_list = u"{0} {1} {2}".format(", ".join(imp_list[:-1]), gettext("and"), imp_list[-1])
            origin_list = Stat(self, "secex", "import_val", "top", "wld_id").value()
            origin_list = [u"<a href='{0}'>{1}</a> ({2})".format(o[0].url(bra), o[0].name(), num_format(o[1], "export_val")) for o in origin_list]
            origin_list = u"{0} {1} {2}".format(", ".join(origin_list[:-1]), gettext("and"), origin_list[-1])
            text.append(gettext(u"The imports of %(bra)s include predominantly %(imp_list)s. The top five origins of the products imported by %(bra)s are: %(origin_list)s.",
                bra=bra.name(), imp_list=imp_list, origin_list=origin_list))
        return text

    def text_hedu(self):
        text = []
        bra = self.attr
        num_univ = Stat(self, "hedu", "num_universities").value()
        year = Stat(self, "hedu", "num_universities").year()
        if not num_univ:
            return [gettext(u"There are no universities found in %(bra)s.", bra=bra.name())]
        lgst_univ, lgst_univ_enrolled = Stat(self, "hedu", "enrolled", "top", "university_id", num_items=1).value()[0]
        lgst_univ_enrolled = num_format(lgst_univ_enrolled, "enrolled")
        course_list = Stat(self, "hedu", "graduates", "top", "course_hedu_id").value()
        course_list = [u"<a href='{0}'>{1}</a> ({2})".format(c[0].url(bra), c[0].name(), num_format(c[1], "enrolled")) for c in course_list]
        course_list = u"{0} {1} {2}".format(", ".join(course_list[:-1]), gettext("and"), course_list[-1])
        genders = Stat(self, "hedu", "graduates", "top", "d_id.gender").value()
        dom_gender = max(genders, key=lambda g:g[1])
        non_dom_gender = min(genders, key=lambda g:g[1])
        if non_dom_gender[1]:
            gender_ratio = dom_gender[1] / float(non_dom_gender[1])
        else:
            gender_ratio = dom_gender[1]
        genders_br = Yd.query.filter_by(year=year).filter(Yd.d_id.in_(['A', 'B']))
        dom_gender_br = max(genders_br, key=lambda g:g.enrolled)
        non_dom_gender_br = min(genders_br, key=lambda g:g.enrolled)
        gender_ratio_br = dom_gender_br.enrolled / float(non_dom_gender_br.enrolled)
        text.append(gettext(u"%(bra)s has %(num_univ)s universities, the largest being %(lgst_univ)s with %(lgst_univ_enrolled)s " \
            "enrolled students as of %(year)s. The 5 majors with the highest number of graduates are %(course_list)s. " \
            "The gender ratio favors %(dom_gender)s across all universities found in %(bra)s by a factor of %(ratio).2f to 1. " \
            "The average gender ratio for all universities in Brazil favors %(dom_gender_br)s by a factor of %(gender_ratio_br).2f to 1.",
            bra=bra.name(), num_univ=num_univ, lgst_univ=lgst_univ.name(), lgst_univ_enrolled=lgst_univ_enrolled,
            year=year, course_list=course_list, dom_gender=dom_gender[0].name(), ratio=gender_ratio,
            dom_gender_br=dom_gender_br.d.name(), gender_ratio_br=gender_ratio_br))
        return text

    def text_sc(self):
        text = []
        bra = self.attr
        num_schools = Stat(self, "sc", "num_schools").format()
        num_enrolled = Stat(self, "sc", "enrolled").format()
        text.append(gettext(u"There are %(num_schools)s schools in %(bra)s with a total of %(num_enrolled)s students.",
            bra=bra.name(), num_schools=num_schools, num_enrolled=num_enrolled))
        return text

    def summary(self):
        text = []
        p = []
        REGION, STATE, MESO, MICRO, PLN_REG, MUNIC = 1, 3, 5, 7, 8, 9
        bra = self.attr
        stats = bra.stats
        is_capital = True if stats.capital_dist == 0 else False
        bra_type = translate("bra_{0}".format(len(bra.id)))
        bra_type_pl = translate("bra_{0}".format(len(bra.id)), n=2)
        start = "The Brazilian %(bra_type)s of %(bra)s "
        region, state, capital = None, None, None

        if len(bra.id) == REGION:
            capital = attrs.Bra.query.get("3df000000")
            if is_capital:
                p.append(gettext(u"The %(bra)s contains the capital city of %(capital)s.",
                                    bra=bra.name(), capital=capital.name()))
            else:
                p.append(gettext(u"The %(bra)s is located in Brazil.", bra=bra.name()))

        if len(bra.id) == STATE:
            region = attrs.Bra.query.get(bra.id[:1])
            if is_capital:
                capital = attrs.Bra.query.get("3df000000")
                p.append(gettext(u"The Brazilian %(bra_type)s of %(bra)s is located in the %(region)s " \
                    u"and contains the capital city, %(capital)s.",
                    bra_type=bra_type, bra=bra.name(), region=region.name(), capital_url=capital, capital=capital.name()))
            else:
                capital = attrs.Bra.query.get(bra.id+"000000").stats.capital
                p.append(gettext(u"The Brazilian %(bra_type)s of %(bra)s is located in the %(region)s of Brazil. " \
                    u"The median municipal distance to the capital of %(capital)s is %(capital_dist)d km.",
                    bra_type=bra_type, bra=bra.name(), region=region.name(),
                    capital_dist=stats.capital_dist, capital=u"<a href='{0}'>{1}</a>".format(capital.url(), capital.name())))

        if len(bra.id) == MESO or len(bra.id) == MICRO:
            state = attrs.Bra.query.get(bra.id[:3])
            capital = stats.capital
            if is_capital:
                p.append(gettext(u"The Brazilian %(bra_type)s of %(bra)s is located in the state of " \
                    u"%(state)s and contains the capital city of %(capital)s.",
                    bra_type=bra_type, bra=bra.name(), state=u"<a href='{0}'>{1}</a>".format(state.url(), state.name()), capital_url=capital.url(), capital=capital))
            else:
                p.append(gettext(u"The Brazilian %(bra_type)s of %(bra)s is located in the state of " \
                    u"%(state)s, %(capital_dist)d km from the " \
                    u"capital city of %(capital)s.",
                    bra_type=bra_type, bra=bra.name(), state=u"<a href='{0}'>{1}</a>".format(state.url(), state.name()),
                    capital_dist=stats.capital_dist, capital=u"<a href='{0}'>{1}</a>".format(capital.url(), capital.name())))

        if len(bra.id) == MUNIC:
            state = attrs.Bra.query.get(bra.id[:3])
            capital = stats.capital
            if is_capital:
                p.append(gettext(u"The Brazilian %(bra_type)s of %(bra)s is the capital of the " \
                    u"state of %(state)s.",
                    bra_type=bra_type, bra=bra.name(),
                    state=u"<a href='{0}'>{1}</a>".format(state.url(), state.name()), capital=u"<a href='{0}'>{1}</a>".format(capital.url(), capital.name())))
            else:
                p.append(gettext(u"The Brazilian %(bra_type)s of %(bra)s is located in the " \
                    u"state of %(state)s, %(capital_dist)d " \
                    u"km from the capital city of %(capital)s.",
                    bra_type=bra_type, bra=bra.name(), state=u"<a href='{0}'>{1}</a>".format(state.url(), state.name()),
                    capital_dist=stats.capital_dist, capital=u"<a href='{0}'>{1}</a>".format(capital.url(), capital.name())))
        #___________________________________
        # Population
        #-----------------------------------
        pop_stat = Stat(self, "attr", "pop")
        pop = pop_stat.format()
        year = pop_stat.year()
        pop_text = ""
        if pop:
            pop_text = gettext(u"As of %(year)s the estimated population of %(bra)s was %(pop)s", year=year, bra=bra.name(), pop=pop)
            pop_density = Stat(self, "attr", "pop_density").format()
            if pop_density:
                pop_text += gettext(u" and its population density was %(pop_density)s inhabitants per km².", bra=bra.name(), pop_density=pop_density)
            else:
                pop_text += "."
        p.append(pop_text)
        # new paragraph
        text.append(" ".join(p).strip()); p = []
        #___________________________________
        # Workforce
        #-----------------------------------
        num_emp = Stat(self, "rais", "num_emp").format()
        wage_avg = Stat(self, "rais", "wage_avg").format()
        p.append(gettext(u"The workforce of %(bra)s is %(num_emp)s strong, " \
            "and the average monthly wage paid is %(wage_avg)s.",
            bra=bra.name(), num_emp=num_emp, wage_avg=wage_avg))
        # new paragraph
        text.append(" ".join(p).strip()); p = []
        #___________________________________
        # Exports
        #-----------------------------------
        exp_stat = Stat(self, "secex", "export_val")
        year = exp_stat.year()
        exp_val = exp_stat.value()
        imp_val = Stat(self, "secex", "import_val").value()
        if exp_val and imp_val:
            ratio = max(exp_val, imp_val) / min(exp_val, imp_val)
            if float("{:.2g}".format(ratio)) == 1:
                text.append(gettext(u"In %(year)s %(bra)s exported %(exp)s and imported %(imp)s, " \
                    "making the balance of trade between exports and imports roughly equal.",
                    year=year, bra=bra.name(), exp=num_format(exp_val, "export_val"), imp=num_format(imp_val, "import_val")))
            else:
                t_balance = gettext("exports") if exp_val > imp_val else gettext("imports")
                text.append(gettext(u"In %(year)s %(bra)s exported %(exp)s and imported %(imp)s, " \
                    "making the balance of trade %(ratio)d to 1 in favor of %(t_balance)s.",
                    year=year, bra=bra.name(), exp=num_format(exp_val, "export_val"), imp=num_format(imp_val, "import_val"), ratio=ratio, t_balance=t_balance))
        elif exp_val or imp_val:
            trade_flow = gettext("exported") if exp_val else gettext("imported")
            opp_trade_flow = gettext("import") if exp_val else gettext("export")
            val = exp_val or imp_val
            text.append(gettext(u"In %(year)s %(bra)s %(trade_flow)s %(val)s but did not %(opp_trade_flow)s any products.",
                year=year, bra=bra.name(), trade_flow=trade_flow, val=num_format(val, "export_val"), opp_trade_flow=opp_trade_flow))
        # new paragraph
        text.append(" ".join(p).strip()); p = []
        #___________________________________
        # HDI
        #-----------------------------------
        if len(bra.id) == STATE or len(bra.id) == MUNIC:
            hdi = Stat(self, "attr", "hdi").value()
            hdi_rank = Stat(self, "attr", "hdi").rank()
        if len(bra.id) == STATE:
            p.append(gettext(u"The Human Development Index (HDI) of %(bra)s is %(hdi).3f (on a scale from 0 to 1). " \
                u"This makes %(bra)s ranked %(rank)s out of the 27 states in Brazil, according to HDI.",
                bra=bra.name(), hdi=hdi, rank=num_format(hdi_rank, "ordinal")))
        if len(bra.id) == MUNIC:
            hdi_rank_state = Stat(self, "attr", "hdi").rank(within_state=True)
            state = attrs.Bra.query.get(bra.id[:3])
            p.append(gettext(u"The Human Development Index (HDI) of %(bra)s is %(hdi).3f (in a scale from 0 to 1). " \
                u"This makes %(bra)s ranked %(rank)s out of all the municipalities in Brazil and %(state_rank)s " \
                "within %(state)s, according to HDI.",
                bra=bra.name(), hdi=hdi, rank=num_format(hdi_rank, "ordinal"), state_rank=num_format(hdi_rank_state, "ordinal"), state=u"<a href='{0}'>{1}</a>".format(state.url(), state.name())))
        if p:
            # new paragraph
            text.append(" ".join(p).strip()); p = []
        #___________________________________
        # Borders
        #-----------------------------------
        if stats.neighbors:
            neighbors = stats.neighbors.split(", ")
            if len(neighbors) == 1:
                # 5rs050103
                n = attrs.Bra.query.get(neighbors[0])
                neighbors = u"<a href='{0}'>{1}</a>".format(n.url(), n.name())
                neighbor_bra_type = bra_type
            else:
                neighbors_arr = [attrs.Bra.query.get(b) for b in neighbors]
                neighbors_arr = [u"<a href='{0}'>{1}</a>".format(n.url(), n.name()) for n in neighbors_arr]
                neighbors = u"{0} {1} {2}".format(", ".join(neighbors_arr[:-1]), gettext("and"), neighbors_arr[-1])
                neighbor_bra_type = bra_type_pl
            p.append(gettext(u"""%(bra)s borders the %(bra_type)s of %(neighbors)s.""",
                bra=bra.name(), bra_type=neighbor_bra_type, neighbors=neighbors))
        else:
            # 2pe020000
            p.append(gettext(u"""%(bra)s is an island bordering no other %(bra_type)s.""",
                bra=bra.name(), bra_type=bra_type_pl))
        # new paragraph
        text.append(" ".join(p).strip()); p = []
        #___________________________________
        # Schools
        #-----------------------------------
        num_univ = Stat(self, "hedu", "num_universities").format() or gettext("no")
        num_schools = Stat(self, "sc", "num_schools").format()
        top_univ = Stat(self, "hedu", "enrolled", "top", output="university_id", num_items=1).value()
        p.append(gettext(u"There are %(num_schools)s schools and %(num_univ)s universities in %(bra)s.",
            num_schools=num_schools, num_univ=num_univ, bra=bra.name()))
        if top_univ:
            top_univ, top_univ_enrolled = top_univ[0]
            top_univ_enrolled = num_format(top_univ_enrolled, "enrolled")
            p.append(gettext(u" The largest university being %(top_univ)s with %(top_univ_enrolled)s students enrolled.",
                num_schools=num_schools, num_univ=num_univ, bra=bra.name(), top_univ=u"<a href='{0}'>{1}</a>".format(top_univ.url(bra), top_univ.name()),
                top_univ_enrolled=top_univ_enrolled))
        # new paragraph
        text.append(" ".join(p).strip()); p = []

        return text
