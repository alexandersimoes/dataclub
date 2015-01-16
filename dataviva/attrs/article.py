# -*- coding: utf-8 -*-
from flask import g
from flask.ext.babel import gettext

def get_article(attr, article):

    if g.locale == "en":
        return article if article != "the" else False

    needed = getattr(attr, "article_{0}".format(g.locale), 0)
    plural = getattr(attr, "plural_{0}".format(g.locale), 0)
    gender = getattr(attr, "gender_{0}".format(g.locale), "m")

    if article == "the" or article == True:
        if not needed:
            return False
        if gender == "m":
            return gettext("article_the_m_p") if plural else gettext("article_the_m")
        if gender == "f":
            return gettext("article_the_f_p") if plural else gettext("article_the_f")

    if article == "at":
        if type(attr) == str or not needed:
            return gettext("article_at")
        if gender == "m":
            return gettext("article_at_m_p") if plural else gettext("article_at_m")
        if gender == "f":
            return gettext("article_at_f_p") if plural else gettext("article_at_f")

    if article == "by":
        if type(attr) == str or not needed:
            return gettext("article_by")
        if gender == "m":
            return gettext("article_by_m_p") if plural else gettext("article_by_m")
        if gender == "f":
            return gettext("article_by_f_p") if plural else gettext("article_by_f")

    if article == "for":
        if type(attr) == str or not needed:
            return gettext("article_for")
        if gender == "m":
            return gettext("article_for_m_p") if plural else gettext("article_for_m")
        if gender == "f":
            return gettext("article_for_f_p") if plural else gettext("article_for_f")

    if article == "from":
        if type(attr) == str or not needed:
            return gettext("article_from")
        if gender == "m":
            return gettext("article_from_m_p") if plural else gettext("article_from_m")
        if gender == "f":
            return gettext("article_from_f_p") if plural else gettext("article_from_f")

    if article == "in":
        if type(attr) == str or not needed:
            return gettext("article_in")
        if gender == "m":
            return gettext("article_in_m_p") if plural else gettext("article_in_m")
        if gender == "f":
            return gettext("article_in_f_p") if plural else gettext("article_in_f")

    if article == "of":
        if type(attr) == str or not needed:
            return gettext("article_of")
        if gender == "m":
            return gettext("article_of_m_p") if plural else gettext("article_of_m")
        if gender == "f":
            return gettext("article_of_f_p") if plural else gettext("article_of_f")

    if article == "to":
        if type(attr) == str or not needed:
            return gettext("article_to")
        if gender == "m":
            return gettext("article_to_m_p") if plural else gettext("article_to_m")
        if gender == "f":
            return gettext("article_to_f_p") if plural else gettext("article_to_f")

    if article == "with":
        if type(attr) == str or not needed:
            return gettext("article_with")
        if gender == "m":
            return gettext("article_with_m_p") if plural else gettext("article_with_m")
        if gender == "f":
            return gettext("article_with_f_p") if plural else gettext("article_with_f")
