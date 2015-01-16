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

class Course_heduProfile(Profile):
    """A university major profile, which extends from the parent profile class.
        instantiate like: Course_heduProfile(), Course_heduProfile('142P01') or
        Course_heduProfile('142P01', '4mg')
    """

    def __init__(self, course_hedu_id=None, bra_id=None):
        """Defaults to most ubiquitous country = USA"""
        course_hedu_id = course_hedu_id or "142P01"
        attr_type = "bra" if bra_id else "wld"
        bra_id = bra_id if bra_id else "sabra"
        super(Course_heduProfile, self).__init__(attr_type, bra_id, "course_hedu", course_hedu_id)

    def title_stem(self):
        if isinstance(self.attr, attrs.Bra) and self.attr.id != "sabra":
            return gettext("<course_hedu> <bra_article_in>")
        return gettext("<course_hedu>")

    def sections(self):
        s = []

        munic_depth = attrs.Cnae.depths[-1]
        show_loc = len(self.attr.id) < munic_depth
        if show_loc:
            locations = Stat(self, "hedu", "enrolled", "top", "bra_id", exclude="0xx000007").value()
            show_loc = locations != None and len(locations) > 1

        show_univ = Stat(self, "hedu", "enrolled", "top", "university_id").value() and len(Stat(self, "hedu", "enrolled", "top", "university_id").value()) > 1

        if show_loc or show_univ:
            s.append({
                "title": gettext("Locations"),
                "anchor": "loc",
                "sections": []
            })

            if show_loc:
                s[0]["sections"].append({
                    "title": gettext("Municipalities"),
                    "anchor": "bra",
                    "builds": [
                        TreeMap("hedu", {"bra": self.attr, "course_hedu": self.filter_attr}, "bra")
                    ]
                })

            if show_univ:
                s[0]["sections"].append({
                    "title": gettext("Universities"),
                    "anchor": "univ",
                    "builds": [
                        Line("hedu", {"bra": self.attr, "course_hedu": self.filter_attr}, "university", size="graduates")
                    ]
                })

        s.append({
            "title": gettext("Demographics"),
            "anchor": "demo",
            "sections": [
                {
                    "title": gettext("Gender Breakdown"),
                    "anchor": "gender",
                    "builds": [
                        Stacked("hedu", {"bra": self.attr, "course_hedu": self.filter_attr, "demo": "gender"}, "course_hedu")
                    ]
                },
                {
                    "title": gettext("Ethnicity Breakdown"),
                    "anchor": "ethnicity",
                    "builds": [
                        Stacked("hedu", {"bra": self.attr, "course_hedu": self.filter_attr, "demo": "ethnicity"}, "course_hedu")
                    ]
                }
            ]
        })

        if show_loc:
            s[-1]["sections"][0]["builds"].append(Bar("hedu", {"bra": self.attr, "course_hedu": self.filter_attr, "demo": "gender"}, "bra", x="bra_{}".format(munic_depth), y="graduates", limit=10, exclude="0xx000007", order="graduates"))
            s[-1]["sections"][1]["builds"].append(Bar("hedu", {"bra": self.attr, "course_hedu": self.filter_attr, "demo": "ethnicity"}, "bra", x="bra_{}".format(munic_depth), y="graduates", limit=10, exclude="0xx000007", order="graduates"))

        return s

    def headlines(self):
        return [
            Stat(self, "hedu", "graduates"),
            Stat(self, "hedu", "enrolled"),
            Stat(self, "hedu", "enrolled", type="top", output="bra", exclude="0xx000007", num_items=1),
            # Stat(self, "hedu", "maleratio")
        ]

    def stats(self):
        return []

    def summary(self):
        p, text = [], []
        location = self.attr
        course_hedu = self.filter_attr
        year = Stat(self, "hedu", "enrolled").year()
        #___________________________________
        # Overview (for specified location)
        #-----------------------------------
        if location.id != "sabra":
            enrolled = Stat(self, "hedu", "enrolled").value()
            year = Stat(self, "hedu", "enrolled").year()
            if enrolled:
                grads = Stat(self, "hedu", "graduates").format()
                p.append(_(u"In %(location)s there were %(enrolled)s students enrolled and %(grads)s who graduated with degrees in %(major)s in %(year)d.",
                    location=location.name(), enrolled=num_format(enrolled), grads=grads, major=course_hedu.name(), year=year))
                rank, rank_total = Stat(self, "hedu", "enrolled", "top", "course_hedu_id.{}".format(len(course_hedu.id))).rank(with_total=True)
                if rank <= (rank_total/2):
                    largest_or_smallest = _("largest")
                else:
                    largest_or_smallest = _("smallest")
                    rank = rank_total - rank
                rank = " "+num_format(rank, "ordinal") if rank > 1 else ""
                p.append(_(u"%(major)s was the %(rank)s %(largest_or_smallest)s major by enrolled students in %(year)d.",
                    major=course_hedu.name(), year=year, rank=rank, largest_or_smallest=largest_or_smallest))
                age = Stat(self, "hedu", "age").value()
                p.append(_(u"The average age of a student studying %(major)s in %(location)s is %(age)d years old.",
                    major=course_hedu.name(), location=location.name(), age=age))
                text.append(" ".join(p).strip()); p = []
                #___________________________________
                # Gender breakdown
                #-----------------------------------
                genders = Stat(self, "hedu", "enrolled", "top", "d_id.gender").value()
                m_enrolled = [e for g, e in genders if g.id == 'A'][0]
                f_enrolled = [e for g, e in genders if g.id == 'B'][0]
                male_pct = (m_enrolled / float(enrolled)) * 100
                female_pct = (f_enrolled / float(enrolled)) * 100
                dom_gender = max(genders, key=lambda g:g[1])
                non_dom_gender = min(genders, key=lambda g:g[1])
                if non_dom_gender[1]:
                    gender_ratio = dom_gender[1] / float(non_dom_gender[1])
                else:
                    gender_ratio = dom_gender[1]
                # raise Exception(genders, enrolled)
                p.append(_(u"%(male_pct).2g%% of %(major)s students in %(location)s are male while " \
                    u"%(female_pct).2g%% are female making the gender ratio %(gender_ratio).2g to 1 in favor of %(dom_gender)s.",
                    location=location.name(), male_pct=male_pct, major=course_hedu.name(), female_pct=female_pct, gender_ratio=gender_ratio, dom_gender=dom_gender[0].name(noun=True)))
                text.append(" ".join(p).strip()); p = []
                #___________________________________
                # Ethnicity breakdown
                #-----------------------------------
                eths = Stat(self, "hedu", "enrolled", "top", "d_id.ethnicity").value()
                eths = [eth for eth in eths if eth[1] > 0]
                dom_eth = eths.pop(0)
                dom_eth_pct = (dom_eth[1] / float(enrolled)) * 100
                if eths:
                    if len(eths) > 1:
                        other_eths = []
                        for e in eths:
                            other_eth_pct = (e[1] / float(enrolled)) * 100
                            other_eths.append(_(u"%(other_eth_pct).2g%% of students report being %(other_eth)s", other_eth_pct=other_eth_pct, other_eth=e[0].name()))
                        other_eths = u"{} {} {}".format(", ".join(other_eths[:-1]), gettext("and"), other_eths[-1])
                    else:
                        eth = eths[0]
                        eth_pct = (eth[1] / float(enrolled)) * 100
                        other_eths = _(u"%(eth_pct).2g%% of students report being %(eth)s", eth_pct=eth_pct, eth=eth[0].name())
                    p.append(_(u"In %(location)s, %(dom_eth_pct).2g%% of %(major)s students report being %(dom_eth)s while %(other_eths)s.",
                        location=location.name(), dom_eth_pct=dom_eth_pct, major=course_hedu.name(), dom_eth=dom_eth[0].name(), other_eths=other_eths))
                text.append(" ".join(p).strip()); p = []
                #___________________________________
                # Top Universities
                #-----------------------------------
                top_univ_list = Stat(self, "hedu", "enrolled", "top", output="university_id").value()
                top_univ = Stat(self, "hedu", "enrolled", "top", output="university_id").list(with_location=True)
                if len(top_univ_list) == 1:
                    p.append(_(u"In %(location)s, The only university to offer %(major)s in %(year)d was %(top_univ)s.",
                        location=location.name(), major=course_hedu.name(), year=year, top_univ=top_univ))
                else:
                    p.append(_(u"In %(location)s, the universities with the highest enrollment in %(major)s were %(top_univ)s.",
                        location=location.name(), major=course_hedu.name(), top_univ=top_univ))
                text.append(" ".join(p).strip()); p = []
            # TODO: get closest university/bra that has this major...
            else:
                num_universities = Stat(self, "hedu", "num_universities")
                if not num_universities:
                    p.append(_(u"There are no universities in %(location)s.", location=location.name()))
                else:
                    p.append(_(u"The %(major)s major was not offered by any of the universities in %(location)s in %(year)d.",
                        major=course_hedu.name(), location=location.name(), year=year))
            text.append(" ".join(p).strip()); p = []
        #___________________________________
        # All Brazil summary
        #-----------------------------------
        enrolled = Stat(self, "hedu", "enrolled", attr=None).value()
        if enrolled:
            grads = Stat(self, "hedu", "graduates", attr=None).format()
            rank, rank_total = Stat(self, "hedu", "enrolled", "top", "course_hedu_id.{}".format(len(course_hedu.id)), attr=None).rank(with_total=True)
            if rank <= (rank_total/2):
                largest_or_smallest = _("largest")
            else:
                largest_or_smallest = _("smallest")
                rank = rank_total - rank
            rank = " "+num_format(rank, "ordinal") if rank > 1 else ""
            p.append(_(u"In Brazil, %(major)s is the %(rank)s %(largest_or_smallest)s major " \
                u"with %(enrolled)s students enrolled and %(grads)s graduating in %(year)d.",
                major=course_hedu.name(), year=year, rank=rank, largest_or_smallest=largest_or_smallest,
                enrolled=num_format(enrolled), grads=grads))
            morn = ("morning", Stat(self, "hedu", "morning", attr=None).value())
            afternoon = ("afternoon", Stat(self, "hedu", "afternoon", attr=None).value())
            night = ("night", Stat(self, "hedu", "night", attr=None).value())
            full_time = ("full time", Stat(self, "hedu", "full_time", attr=None).value())
            time_of_day = [morn, afternoon, night, full_time]
            time_of_day = [t for t in time_of_day if t[1]]
            if len(time_of_day) == 1:
                p.append(_(u"All students studying %(major)s are enrolled in %(time_of_day)s classes.",
                    major=course_hedu.name(), time_of_day=time_of_day[0][0]))
            else:
                time_of_day = sorted(time_of_day, key=lambda v: v[1], reverse=True)
                total = sum(v for t, v in time_of_day)
                dom_t = time_of_day.pop(0)
                dom_t_pct = (dom_t[1] / float(total)) * 100
                if len(time_of_day) > 1:
                    other_t = []
                    for t in time_of_day:
                        other_t_pct = (t[1] / float(total)) * 100
                        other_t.append(_(u"%(other_t_pct).2g%% of students are %(other_t)s", other_t_pct=other_t_pct, other_t=t[0]))
                    other_t = u"{} {} {}".format(", ".join(other_t[:-1]), gettext("and"), other_t[-1])
                    p.append(_(u"Most students, %(dom_t_pct).2g%%, are enrolled in %(dom_t)s classes while %(other_t)s.",
                        dom_t=dom_t[0], dom_t_pct=dom_t_pct, other_t=other_t))
                else:
                    t = time_of_day[0]
                    t_pct = (t[1] / float(total)) * 100
                    other_t = _(u"%(t_pct).2g%% of students are %(t)s", t_pct=t_pct, t=t[0])
                    if t_pct == dom_t_pct:
                        p.append(_(u"Half of the students are enrolled in %(dom_t)s classes while the other half are %(other_t)s.",
                            dom_t=dom_t[0], dom_t_pct=dom_t_pct, other_t=t[0]))
                    else:
                        p.append(_(u"Most students, %(dom_t_pct).2g%%, are enrolled in %(dom_t)s classes while %(other_t)s.",
                            dom_t=dom_t[0], dom_t_pct=dom_t_pct, other_t=other_t))
            text.append(" ".join(p).strip()); p = []
            #___________________________________
            # Top Universities
            #-----------------------------------
            top_univ_list = Stat(self, "hedu", "enrolled", "top", output="university_id", attr=None).value()
            top_univ = Stat(self, "hedu", "enrolled", "top", output="university_id", attr=None).list()
            if len(top_univ_list) == 1:
                p.append(_(u"In all of Brazil, The only university to offer %(major)s in %(year)d was %(top_univ)s.",
                    major=course_hedu.name(), year=year, top_univ=top_univ))
            else:
                p.append(_(u"In all of Brazil, the universities with the highest enrollment in %(major)s were %(top_univ)s.",
                    major=course_hedu.name(), top_univ=top_univ))
                # top_univ_rca = Stat(self, "hedu", "enrolled_rca", "top", output="course_hedu_id").list(with_value=False)
                # p.append(_(u"Ordered by RCA, %(university)s specializes in the following courses %(top_univ_rca)s.",
                #     university=university.name(), top_univ_rca=top_univ_rca))
            text.append(" ".join(p).strip()); p = []
            #___________________________________
            # Gender breakdown
            #-----------------------------------
            genders = Stat(self, "hedu", "enrolled", "top", "d_id.gender", attr=None).value()
            m_enrolled = [e for g, e in genders if g.id == 'A'][0]
            f_enrolled = [e for g, e in genders if g.id == 'B'][0]
            male_pct = (m_enrolled / float(enrolled)) * 100
            female_pct = (f_enrolled / float(enrolled)) * 100
            dom_gender = max(genders, key=lambda g:g[1])
            non_dom_gender = min(genders, key=lambda g:g[1])
            if non_dom_gender[1]:
                gender_ratio = dom_gender[1] / float(non_dom_gender[1])
            else:
                gender_ratio = dom_gender[1]
            p.append(_(u"%(male_pct).2g%% of %(major)s students in %(location)s are male while " \
                u"%(female_pct).2g%% are female making the gender ratio %(gender_ratio).2g to 1 in favor of %(dom_gender)s.",
                location=location.name(), male_pct=male_pct, major=course_hedu.name(), female_pct=female_pct, gender_ratio=gender_ratio, dom_gender=dom_gender[0].name(noun=True)))
            text.append(" ".join(p).strip()); p = []
        else:
            p.append(_(u"In %(year)d there were no students enrolled in %(major)s.",
                major=course_hedu.name(), year=year))
            text.append(" ".join(p).strip()); p = []
        # raise Exception(text)
        return text
