from flask.ext.babel import gettext

def title(args):

    if args["display_attr"] == "cnae":

        if args["size"] == "wage_avg":
            if args["limit"]:
                if args["demo"] == "gender":
                    if args["order"] == "wage_avg.A":
                        if "cbo" in args["filters"]:
                            return gettext("Highest paying industries <bra_article_in> that employ <cbo> and favor men")
                        return gettext("Highest paying industries <bra_article_in> favoring men")
                    if args["order"] == "wage_avg.B":
                        if "cbo" in args["filters"]:
                            return gettext("Highest paying industries <bra_article_in> that employ <cbo> and favor women")
                        return gettext("Highest paying industries <bra_article_in> favoring women")
                    if "cbo" in args["filters"]:
                        return gettext("Highest paying industries <bra_article_in> by gender that employ <cbo>")
                    return gettext("Highest paying industries <bra_article_in> by gender")
                if args["demo"] == "ethnicity":
                    if "cbo" in args["filters"]:
                        return gettext("Highest paying industries <bra_article_in> by ethnicity that employ <cbo>")
                    return gettext("Highest paying industries <bra_article_in> by ethnicity")
                if "cbo" in args["filters"]:
                    return gettext("Highest paying industries <bra_article_in> that employ <cbo>")
                return gettext("Highest paying industries <bra_article_in>")
            if "cbo" in args["filters"]:
                return gettext("Average wages paid <bra_article_in> that employ <cbo> by industry")
            return gettext("Average wages paid <bra_article_in> by industry")
        if args["size"] == "num_emp":
            if args["limit"]:
                if args["demo"] == "gender":
                    if args["order"] == "wage_avg.A":
                        if "cbo" in args["filters"]:
                            return gettext("Largest industries <bra_article_in> that employ <cbo> and favor men")
                        return gettext("Largest industries <bra_article_in> favoring men")
                    if args["order"] == "wage_avg.B":
                        if "cbo" in args["filters"]:
                            return gettext("Largest industries <bra_article_in> that employ <cbo> and favor women")
                        return gettext("Largest industries <bra_article_in> favoring women")
                    if "cbo" in args["filters"]:
                        return gettext("Largest industries <bra_article_in> by gender that employ <cbo>")
                    return gettext("Largest industries <bra_article_in> by gender")
                if args["demo"] == "ethnicity":
                    if "cbo" in args["filters"]:
                        return gettext("Largest industries <bra_article_in> by ethnicity that employ <cbo>")
                    return gettext("Largest industries <bra_article_in> by ethnicity")
                if "cbo" in args["filters"]:
                    return gettext("Largest industries <bra_article_in> that employ <cbo>")
                return gettext("Largest industries <bra_article_in>")
            if "cbo" in args["filters"]:
                return gettext("Number of employees <bra_article_in> by industry that employ <cbo>")
            return gettext("Number of employees <bra_article_in> by industry")

        if "cbo" in args["filters"]:
            return gettext("Industries <bra_article_in> that employ <cbo>")
        return gettext("Industries <bra_article_in>")

    if args["display_attr"] == "cbo":

        if args["size"] == "wage_avg":
            if args["limit"]:
                if args["demo"] == "gender":
                    if args["order"] == "wage_avg.A":
                        if "cnae" in args["filters"]:
                            return gettext("Highest paid occupations employed <cnae_article_by> <bra_article_in> favoring men")
                        return gettext("Highest paid occupations <bra_article_in> favoring men")
                    if args["order"] == "wage_avg.B":
                        if "cnae" in args["filters"]:
                            return gettext("Highest paid occupations employed <cnae_article_by> <bra_article_in> favoring women")
                        return gettext("Highest paid occupations <bra_article_in> favoring women")
                    if "cnae" in args["filters"]:
                        return gettext("Highest paid occupations employed <cnae_article_by> <bra_article_in> by gender")
                    return gettext("Highest paid occupations <bra_article_in> by gender")
                if args["demo"] == "ethnicity":
                    if "cnae" in args["filters"]:
                        return gettext("Highest paid occupations employed <cnae_article_by> <bra_article_in> by ethnicity")
                    return gettext("Highest paid occupations <bra_article_in> by ethnicity")
                if "cnae" in args["filters"]:
                    return gettext("Highest paid occupations employed <cnae_article_by> <bra_article_in>")
                return gettext("Highest paid occupations <bra_article_in>")
            if "cnae" in args["filters"]:
                return gettext("Average wages paid employed <cnae_article_by> <bra_article_in> by occupation")
            return gettext("Average wages paid <bra_article_in> by occupation")
        if args["size"] == "num_emp":
            if args["limit"]:
                if args["demo"] == "gender":
                    if args["order"] == "wage_avg.A":
                        if "cnae" in args["filters"]:
                            return gettext("Common occupations employed <cnae_article_by> <bra_article_in> favoring men")
                        return gettext("Common occupations <bra_article_in> favoring men")
                    if args["order"] == "wage_avg.B":
                        if "cnae" in args["filters"]:
                            return gettext("Common occupations employed <cnae_article_by> <bra_article_in> favoring women")
                        return gettext("Common occupations <bra_article_in> favoring women")
                    if "cnae" in args["filters"]:
                        return gettext("Common occupations employed <cnae_article_by> <bra_article_in> by gender")
                    return gettext("Common occupations <bra_article_in> by gender")
                if args["demo"] == "ethnicity":
                    if "cnae" in args["filters"]:
                        return gettext("Common occupations employed <cnae_article_by> <bra_article_in> by ethnicity")
                    return gettext("Common occupations <bra_article_in> by ethnicity")
                if "cnae" in args["filters"]:
                    return gettext("Common occupations employed <cnae_article_by> <bra_article_in>")
                return gettext("Common occupations <bra_article_in>")
            if "cnae" in args["filters"]:
                return gettext("Number of employees employed <cnae_article_by> <bra_article_in> by occupation")
            return gettext("Number of employees <bra_article_in> by occupation")

        if "cnae" in args["filters"]:
            return gettext("Occupations <bra_article_in> employed <cnae_article_by>")
        return gettext("Occupations <bra_article_in>")

    if args["display_attr"] == "bra":

        if "cnae" in args["filters"] and "cbo" in args["filters"]:
            return gettext("Locations <bra_article_in> that employ <cbo> <cnae_article_in>")
        if "cnae" in args["filters"]:
            return gettext("Locations <bra_article_in> <cnae_article_with>")
        if "cbo" in args["filters"]:
            return gettext("Locations <bra_article_in> that employ <cbo>")
        return gettext("Industrial Activity <bra_article_in> by Municipality")
