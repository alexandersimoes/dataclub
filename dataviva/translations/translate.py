# -*- coding: utf-8 -*-
from dataviva.translations.dictionary import singulars, plurals
from dataviva.utils.title_case import title_case

''' Translates the columns names '''
def translate(key=None, n=1):

    if key:
        if key in singulars:
            return unicode(singulars[key])
        return plurals(key=key, n=n) or title_case(key)

    returnDict = {}
    for d, v in singulars.iteritems():
        returnDict[d] = unicode(v)
    sing = plurals(n=1)
    for d, v in sing.iteritems():
        returnDict[d] = unicode(v)
    plur = plurals(n=2)
    for d, v in plur.iteritems():
        returnDict["{0}_plural".format(d)] = unicode(v)
    return returnDict
