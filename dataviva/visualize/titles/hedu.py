from flask.ext.babel import gettext

def title(args):

    demo    = args["demo"]
    order   = args["order"]
    filters = args["filters"]
    size    = args["size"]
    split   = args["split"]
    out     = args["display_attr"]

    if "bra" in filters:
        use_bra = isinstance(filters["bra"], (str, unicode)) or filters["bra"].id != "sabra"
    else:
        use_bra = False

    if args["limit"]:
        if "university" in filters:
            if use_bra:
                if demo == "gender":
                    if order == "enrolled.A":
                        return gettext("Common majors <university_article_at> <bra_article_in> with a majority of men")
                    if order == "enrolled.B":
                        return gettext("Common majors <university_article_at> <bra_article_in> with a majority of women")
                    return gettext("Common majors <university_article_at> <bra_article_in> by gender")
                if demo == "ethnicity":
                    return gettext("Common majors <university_article_at> <bra_article_in> by ethnicity")
                return gettext("Common majors <university_article_at> <bra_article_in>")
            else:
                if demo == "gender":
                    if order == "enrolled.A":
                        return gettext("Common majors <university_article_at> with a majority of men")
                    if order == "enrolled.B":
                        return gettext("Common majors <university_article_at> with a majority of women")
                    return gettext("Common majors <university_article_at> by gender")
                if demo == "ethnicity":
                    return gettext("Common majors <university_article_at> by ethnicity")
                return gettext("Common majors <university_article_at>")
        elif "course_hedu" in filters:
            if demo == "gender":
                if order == "enrolled.A":
                    return gettext("Common locations <course_hedu_article_for> <bra_article_in> with a majority of men")
                if order == "enrolled.B":
                    return gettext("Common locations <course_hedu_article_for> <bra_article_in> with a majority of women")
                return gettext("Common locations <course_hedu_article_for> <bra_article_in> by gender")
            if demo == "ethnicity":
                return gettext("Common locations <course_hedu_article_for> <bra_article_in> by ethnicity")
            return gettext("Common locations <course_hedu_article_for> <bra_article_in>")
        else:
            if out == "course_hedu":
                if demo == "gender":
                    if order == "enrolled.A":
                        return gettext("Common majors <bra_article_in> with a majority of men")
                    if order == "enrolled.B":
                        return gettext("Common majors <bra_article_in> with a majority of women")
                    return gettext("Common majors <bra_article_in> by gender")
                if demo == "ethnicity":
                    return gettext("Common majors <bra_article_in> by ethnicity")
                return gettext("Common majors <bra_article_in>")

    if demo == "gender":
        if out == "course_hedu":
            if "university" in filters:
                if use_bra:
                    return gettext("Majors by gender <university_article_at> <bra_article_in>")
                else:
                    return gettext("Majors by gender <university_article_at>")
            else:
                return gettext("Majors by gender <bra_article_in>")
        else:
            if "university" in filters:
                if use_bra:
                    return gettext("Gender of students <university_article_at> <bra_article_in>")
                else:
                    return gettext("Gender of students <university_article_at>")
            elif "course_hedu" in filters:
                return gettext("Gender <course_hedu_article_of> majors <bra_article_in>")
            else:
                return gettext("Gender of students <bra_article_in>")
    elif demo == "ethnicity":
        if out == "course_hedu":
            if "university" in filters:
                if use_bra:
                    return gettext("Majors by ethnicity <university_article_at> <bra_article_in>")
                else:
                    return gettext("Majors by ethnicity <university_article_at>")
            else:
                return gettext("Majors by ethnicity <bra_article_in>")
        else:
            if "university" in filters:
                if use_bra:
                    return gettext("Ethnicity of students <university_article_at> <bra_article_in>")
                else:
                    return gettext("Ethnicity of students <university_article_at>")
            elif "course_hedu" in filters:
                return gettext("Ethnicity <course_hedu_article_of> majors <bra_article_in>")
            else:
                return gettext("Ethnicity of students <bra_article_in>")

    if split == "time":
        if "university" in filters:
            if use_bra:
                return gettext("Program enrollment <university_article_at> <bra_article_in>")
            else:
                return gettext("Program enrollment <university_article_at>")
        elif "course_hedu" in filters:
            return gettext("Program enrollment <course_hedu_article_for> <bra_article_in>")
        else:
            return gettext("Program enrollment <bra_article_in>")

    if out == "course_hedu":
        if size == "graduates":
            if "university" in filters:
                if use_bra:
                    return gettext("Graduating student majors <university_article_from> <bra_article_in>")
                else:
                    return gettext("Graduating student majors <university_article_from>")
            return gettext("Graduating student majors <bra_article_in>")
        else:
            if "university" in filters:
                if use_bra:
                    return gettext("Majors offered <university_article_by> <bra_article_in>")
                else:
                    return gettext("Majors offered <university_article_by>")
            return gettext("Majors available <bra_article_in>")
    elif out == "university":
        if "course_hedu" in filters:
            return gettext("Universities <course_hedu_article_with> <bra_article_in>")
        return gettext("Universities <bra_article_in>")
    elif out == "bra":
        if "course_hedu" in filters:
            return gettext("Locations <bra_article_in> <course_hedu_article_with>")
        elif "university" in filters:
            if use_bra:
                return gettext("Locations <university_article_of> <bra_article_in>")
            else:
                return gettext("Locations <university_article_of>")
        return gettext("Locations <bra_article_in>")
