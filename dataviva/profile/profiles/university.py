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

class UniversityProfile(Profile):
    """A university major profile, which extends from the parent profile class.
        instantiate like: CourseHeduProfile(), CourseHeduProfile('211A02') or
        CourseHeduProfile('211A02', 'mg')
    """

    def __init__(self, university_id=None, bra_id=None):
        """Defaults to most ubiquitous country = USA"""
        university_id = university_id or "00316"
        attr_type = "bra" if bra_id else "wld"
        bra_id = bra_id if bra_id else "sabra"
        super(UniversityProfile, self).__init__(attr_type, bra_id, "university", university_id)

    def title_stem(self):
        if isinstance(self.attr, attrs.Bra) and self.attr.id != "sabra":
            return gettext("<university> <bra_article_in>")
        return gettext("<university>")

    def sections(self):
        course_depth = attrs.Course_hedu.depths[-1]
        num_courses = len(Stat(self, "hedu", "enrolled", "top", "course_hedu_id", num_items=11).value())

        s = [
            {
                "title": gettext("Enrollment"),
                "anchor": "enrolled",
                "builds": [
                    Line("hedu", {"bra": self.attr, "university": self.filter_attr}, "course_hedu", y="enrolled"),
                    Stacked("hedu", {"bra": self.attr, "university": self.filter_attr}, "course_hedu", y="enrolled", split="time")
                ]
            },
            {
                "title": gettext("Demographics"),
                "anchor": "demo",
                "sections": [
                    {
                        "title": gettext("Gender Breakdown"),
                        "anchor": "gender",
                        "builds": [
                            Stacked("hedu", {"bra": self.attr, "university": self.filter_attr, "demo": "gender"}, "university")
                        ]
                    },
                    {
                        "title": gettext("Ethnicity Breakdown"),
                        "anchor": "ethnicity",
                        "builds": [
                            Stacked("hedu", {"bra": self.attr, "university": self.filter_attr, "demo": "ethnicity"}, "university")
                        ]
                    }
                ]
            }
        ]

        if num_courses > 10:
            s[-1]["sections"][0]["builds"].append(
                Bar("hedu", {"bra": self.attr, "university": self.filter_attr, "demo": "gender"}, "course_hedu", x="course_hedu_{0}".format(course_depth), y="enrolled", limit=10, order="enrolled.A")
            )
            s[-1]["sections"][0]["builds"].append(
                Bar("hedu", {"bra": self.attr, "university": self.filter_attr, "demo": "gender"}, "course_hedu", x="course_hedu_{0}".format(course_depth), y="enrolled", limit=10, order="enrolled.B")
            )
        elif num_courses > 1:
            s[-1]["sections"][0]["builds"].append(
                Bar("hedu", {"bra": self.attr, "university": self.filter_attr, "demo": "gender"}, "course_hedu", x="course_hedu_{0}".format(course_depth), y="enrolled", order="enrolled")
            )

        return s


    def headlines(self):
        return [
            Stat(self, "hedu", "enrolled", type="top", output="bra_id", exclude="0xx000007", num_items=1),
            Stat(self, "hedu", "enrolled"),
            Stat(self, "hedu", "graduates"),
            Stat(self, "hedu", "enrolled", type="top", output="course_hedu_id", num_items=1)
        ]

    def stats(self):
        return []

    def summary(self):
        p, text = [], []
        location = self.attr
        university = self.filter_attr
        #___________________________________
        # Overview
        #-----------------------------------
        school_type = university.school_type.name()
        locations = Stat(self, "hedu", "enrolled", "value", "bra_id", exclude="0xx000007").value()
        state = attrs.Bra.query.get(locations[0][0].id[:3])
        state_link = u"<a href='{}'>{}</a>".format(state.url(), state.name())
        if len(locations) > 1:
            locations = Stat(self, "hedu", "enrolled", "value", "bra_id", exclude="0xx000007").list(with_filter=True)
            num_locations = Stat(self, "hedu", "enrolled", "value", "bra_id", exclude="0xx000007").count()
            p.append(_(u"%(university)s is a %(school_type)s with %(num_locations)d campuses " \
                u"located thoughout the state of %(state)s, the largest locations being %(locations)s.",
                university=university.name(), school_type=school_type, state=state_link,
                num_locations=num_locations, locations=locations))
            rank, rank_total = Stat(self, "hedu", "enrolled", "top", "university_id", attr=state).rank(with_total=True)
            rank = " "+num_format(rank, "ordinal") if rank > 1 else ""
            p.append(_(u"It is the%(rank)s largest university (out of %(total)s) in the state of %(state)s by number of enrolled students.",
                rank=rank, total=rank_total, state=state.name()))
        else:
            munic = locations[0][0]
            munic_link = u"<a href='{}'>{}</a>".format(munic.url(), munic.name())
            p.append(_(u"%(university)s is a %(school_type)s located in %(munic)s in the state of %(state)s.",
                university=university.name(), school_type=school_type, munic=munic_link, state=state_link))
            rank, rank_total = Stat(self, "hedu", "enrolled", "top", "university_id", attr=munic).rank(with_total=True)
            rank = " "+num_format(rank, "ordinal") if rank > 1 else ""
            p.append(_(u"It is the%(rank)s largest university (out of %(total)s) in %(munic)s by number of enrolled students",
                rank=rank, total=rank_total, munic=munic_link))
            rank, rank_total = Stat(self, "hedu", "enrolled", "top", "university_id", attr=state).rank(with_total=True)
            rank = " "+num_format(rank, "ordinal") if rank > 1 else ""
            p.append(_(u"and the%(rank)s largest (out of %(total)s) in the state of %(state)s.",
                university=university.name(), rank=rank, total=rank_total, state=state_link))
        text.append(" ".join(p).strip()); p = []
        #___________________________________
        # Deep dive
        #-----------------------------------
        year = Stat(self, "hedu", "enrolled").year()
        enrolled = Stat(self, "hedu", "enrolled").value()
        if enrolled:
            entrants = Stat(self, "hedu", "entrants").format()
            grads = Stat(self, "hedu", "graduates").format()
            p.append(_(u"In %(year)d there were %(enrolled)s enrolled with %(entrants)s " \
                u"entering and %(grads)s graduating in that year.",
                university=university.name(), enrolled=num_format(enrolled, "enrolled"), year=year, entrants=entrants,
                grads=grads))
            morn = ("morning", Stat(self, "hedu", "morning", attr=None).value())
            afternoon = ("afternoon", Stat(self, "hedu", "afternoon", attr=None).value())
            night = ("night", Stat(self, "hedu", "night", attr=None).value())
            full_time = ("full time", Stat(self, "hedu", "full_time", attr=None).value())
            time_of_day = [morn, afternoon, night, full_time]
            time_of_day = [t for t in time_of_day if t[1]]
            time_of_day = sorted(time_of_day, key=lambda v: v[1], reverse=True)
            total = sum(v for t, v in time_of_day)
            dom_t = time_of_day.pop(0)
            dom_t_pct = (dom_t[1] / float(total)) * 100
            if time_of_day:
                if len(time_of_day) > 1:
                    other_t = []
                    for t in time_of_day:
                        other_t_pct = (t[1] / float(total)) * 100
                        other_t.append(_(u"%(other_t_pct).2g%% of students are %(other_t)s", other_t_pct=other_t_pct, other_t=t[0]))
                    other_t = u"{} {} {}".format(", ".join(other_t[:-1]), gettext("and"), other_t[-1])
                else:
                    t = time_of_day[0]
                    t_pct = (t[1] / float(total)) * 100
                    other_t = _(u"%(t_pct).2g%% of students are %(t)s", t_pct=t_pct, t=t[0])
                p.append(_(u"Most students, %(dom_t_pct).2g%%, are enrolled in %(dom_t)s classes while %(other_t)s.",
                    dom_t=dom_t[0], dom_t_pct=dom_t_pct, other_t=other_t))
            else:
                p.append(_(u"All students are enrolled in %(dom_t)s classes.",
                    dom_t=dom_t[0]))
            age = Stat(self, "hedu", "age").value()
            p.append(_(u"The average age of a student studying at %(university)s is %(age)d.",
                university=university.name(), age=age))
            text.append(" ".join(p).strip()); p = []
            #___________________________________
            # Top courses
            #-----------------------------------
            top_majors_list = Stat(self, "hedu", "enrolled", "top", output="course_hedu_id").value()
            top_majors = Stat(self, "hedu", "enrolled", "top", output="course_hedu_id").list(with_location=True)
            if len(top_majors_list) == 1:
                p.append(_(u"The only major offered at %(university)s is %(top_majors)s.",
                    university=university.name(), top_majors=top_majors))
            else:
                p.append(_(u"The top majors offered at %(university)s by number of enrolled students are %(top_majors)s.",
                    university=university.name(), top_majors=top_majors))
                top_majors_rca = Stat(self, "hedu", "enrolled_rca", "top", output="course_hedu_id").list(with_value=False, with_location=True)
                p.append(_(u"Ordered by RCA, %(university)s specializes in the following courses %(top_majors_rca)s.",
                    university=university.name(), top_majors_rca=top_majors_rca))
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
            if float("{:.2g}".format(gender_ratio)) == 1:
                p.append(_(u"%(male_pct).3g%% of the students at %(university)s are male while " \
                    u"%(female_pct).2g%% are female making the gender ratio roughly equal.",
                    university=university.name(), male_pct=male_pct, female_pct=female_pct))
            else:
                p.append(_(u"%(male_pct).3g%% of the students at %(university)s are male while " \
                    u"%(female_pct).2g%% are female making the gender ratio %(gender_ratio).2g to 1 in favor of %(dom_gender)s.",
                    university=university.name(), male_pct=male_pct, female_pct=female_pct,
                    gender_ratio=gender_ratio, dom_gender=dom_gender[0].name(noun=True)))
            text.append(" ".join(p).strip()); p = []
            #___________________________________
            # Ethnicity breakdown
            #-----------------------------------
            eths = Stat(self, "hedu", "enrolled", "top", "d_id.ethnicity").value()
            eths = [eth for eth in eths if eth[1] > 0]
            dom_eth = eths.pop(0)
            dom_eth_pct = (dom_eth[1] / float(enrolled)) * 100
            if len(eths) > 1:
                other_eths = []
                for e in eths:
                    other_eth_pct = (e[1] / float(enrolled)) * 100
                    other_eths.append(_(u"%(other_eth_pct).2g%% of students report being %(other_eth)s", other_eth_pct=other_eth_pct, other_eth=e[0].name()))
                other_eths = u"{} {} {}".format(", ".join(other_eths[:-1]), gettext("and"), other_eths[-1])
            else:
                eth = eths[0]
                eth_pct = (eth[1] / float(enrolled)) * 100
                other_eths = _(u"%(eth_pct).2g%% of students are %(eth)s", eth_pct=eth_pct, eth=eth[0].name())
            p.append(_(u"At %(university)s %(dom_eth_pct).3g%% of students report being %(dom_eth)s while %(other_eths)s.",
                university=university.name(), dom_eth_pct=dom_eth_pct, dom_eth=dom_eth[0].name(), other_eths=other_eths))
            text.append(" ".join(p).strip()); p = []
        else:
            p.append(_(u"%(university)s does not have a campus located in %(location)s.",
                university=university.name(), location=location.name()))
            text.append(" ".join(p).strip()); p = []
        # raise Exception(text)
        return text
