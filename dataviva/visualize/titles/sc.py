from flask.ext.babel import gettext

def title(args):

    demo = args["demo"]

    if demo == "ethnicity":
        return gettext("Early education <bra_article_in> by ethnicity")

    if args["display_attr"] == "course_sc":
        return gettext("Early education <bra_article_in>")
