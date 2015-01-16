from dataviva.profile.profiles import *
import re


def profileList(opts = {}):
    attrs = ["bra","hs","wld","cnae","cbo"]

    for a in attrs:
        if a not in opts:
            opts[a] = "<{0}>".format(a)

    profiles = []

    profiles.append(BraProfile(opts["bra"]))
    profiles.append(CnaeProfile(opts["cnae"], opts["bra"]))
    profiles.append(CboProfile(opts["cbo"], opts["bra"]))
    profiles.append(HsProfile(opts["hs"], opts["bra"]))
    profiles.append(WldProfile(opts["wld"], opts["bra"]))

    return profiles

def parseProfileString(url):
    attrs = ["bra", "hs", "wld", "cnae", "cbo", "econ", "edu", "course_hedu", "university"]

    profile_map = { "bra" : BraProfile,
                    "cnae" : CnaeProfile,
                    "cbo" : CboProfile,
                    "hs": HsProfile,
                    "wld" : WldProfile,
                    "course_hedu": Course_heduProfile,
                    "university" : UniversityProfile
    }

    params = url.split("/")[2:]
    params.reverse()
    profile_type = None
    arguments = []
    for param in params:
        if param in attrs and not profile_type:
            profile_type = param
        elif param and not param in attrs and param != 'sabra':
            arguments.append(param)

    if not profile_type or profile_type not in profile_map:
        raise Exception("Could not parse profile type: {0}".format(profile_type))

    profile = profile_map[profile_type]
    return profile, arguments
