from flask.ext.babel import gettext

def title(args):

    filters = len(args["filters"])

    if args["display_key"] == "bra_s":

        if filters == 5:
            return gettext("Locations <bra_s_article_in> <cnae_s_article_with> that sell <hs> <cnae_r_article_to> <bra_r_article_in>")

        if filters == 4:
            return gettext("Locations <cnae_s_article_with> that sell <hs> <cnae_r_article_to> <bra_r_article_in>")

        if filters == 3:

            if "bra_r" in args["filters"]:
                if "cnae_s" in args["filters"]:
                    if "cnae_r" in args["filters"]:
                        return gettext("Locations <cnae_s_article_with> that sell <cnae_r_article_to> <bra_r_article_in>")
                    if "hs" in args["filters"]:
                        return gettext("Locations that sell <hs> <cnae_r_article_to> <bra_r_article_in>")
                if "cnae_r" in args["filters"] and "hs" in args["filters"]:
                    return gettext("Locations <cnae_s_article_with> that sell <hs> <bra_r_article_to>")
            return gettext("Locations that purchase <hs> domestically <cnae_r_article_from> <bra_s_article_in>")

        if filters == 2:

            if "bra_r" in args["filters"]:
                if "bra_s" in args["filters"]:
                    return gettext("Locations <bra_s_article_in> that sell domestically <bra_r_active_to>")
                if "cnae_s" in args["filters"]:
                    return gettext("Locations <cnae_s_article_with> that sell domestically <bra_r_active_to>")
                if "cnae_r" in args["filters"]:
                    return gettext("Locations that sell domestically <cnae_r_article_to> <bra_r_article_in>")
                if "hs" in args["filters"]:
                    return gettext("Locations that sell <hs> domestically <bra_r_article_to>")

            if "cnae_s" in args["filters"]:
                if "bra_s" in args["filters"]:
                    return gettext("Locations <bra_s_article_in> <cnae_s_article_with> that sell domestically")
                if "cnae_r" in args["filters"]:
                    return gettext("Locations <cnae_s_article_with> that sell domestically <cnae_r_article_to>")
                if "hs" in args["filters"]:
                    return gettext("Locations <cnae_s_article_with> that sell <hs> domestically")

            if "cnae_r" in args["filters"]:
                if "bra_s" in args["filters"]:
                    return gettext("Locations <bra_s_article_in> that sell domestically <cnae_r_article_to>")
                if "hs" in args["filters"]:
                    return gettext("Locations that sell <hs> domestically <cnae_r_article_to>")

            return gettext("Locations <bra_article_in> that sell <hs> domestically")

        if filters == 1:

            if "bra_s" in args["filters"]:
                return gettext("Locations <bra_r_article_in> that sell domestically")
            if "bra_r" in args["filters"]:
                return gettext("Locations that sell domestically <bra_r_article_to>")
            if "cnae_s" in args["filters"]:
                return gettext("Locations <cnae_s_article_with> that sell domestically")
            if "cnae_r" in args["filters"]:
                return gettext("Locations that sell domestically <cnae_r_article_to>")
            if "hs" in args["filters"]:
                return gettext("Locations that sell <hs> domestically")

    if args["display_key"] == "cnae_s":

        if filters == 4:
            return gettext("Industries <bra_s_article_in> that purchase <hs> domestically <cnae_r_article_from> <bra_r_article_in>")

        if filters == 3:

            if "bra_r" in args["filters"]:
                if "cnae_r" in args["filters"]:
                    if "bra_s" in args["filters"]:
                        return gettext("Industries <bra_s_article_in> that purchase domestically <cnae_r_article_from> <bra_r_article_in>")
                    if "hs" in args["filters"]:
                        return gettext("Industries that purchase <hs> domestically <cnae_r_article_from> <bra_r_article_in>")
                if "bra_s" in args["filters"] and "hs" in args["filters"]:
                    return gettext("Industries <bra_s_article_in> that purchase <hs> domestically <cnae_r_article_from>")
            return gettext("Industries <bra_s_article_in> that purchase <hs> domestically <cnae_r_article_from>")

        if filters == 2:

            if "bra_r" in args["filters"]:
                if "cnae_r" in args["filters"]:
                    return gettext("Industries in Minas Gerais that purchase domestically <cnae_r_article_from> <bra_r_article_in>")
                if "bra_s" in args["filters"]:
                    return gettext("Industries <bra_s_article_in> that purchase domestically <bra_r_article_from>")
                if "hs" in args["filters"]:
                    return gettext("Industries that purchase <hs> domestically <bra_r_article_from>")

            if "cnae_r" in args["filters"]:
                if "bra_s" in args["filters"]:
                    return gettext("Industries <bra_s_article_in> that purchase domestically <cnae_r_article_from>")
                if "hs" in args["filters"]:
                    return gettext("Industries in Minas Gerais that purchase <hs> domestically <cnae_r_article_from>")

            return gettext("Industries <bra_s_article_in> that purchase <hs> domestically")

        if filters == 1:
            if "bra_s" in args["filters"]:
                return gettext("Industries <bra_s_article_from> that purchase domestically")
            if "cnae_r" in args["filters"]:
                return gettext("Industries that sell domestically <cnae_r_article_to>")
            if "bra_r" in args["filters"]:
                return gettext("Industries that sell domestically <bra_s_article_to>")
            if "hs" in args["filters"]:
                return gettext("Industries that purchase <hs> domestically")

    if args["display_key"] == "bra_r":

        if filters == 4:
            return gettext("Locations <cnae_r_article_with> that purchase <hs> domestically <cnae_s_article_from> <bra_s_article_in>")

        if filters == 3:

            if "bra_s" in args["filters"]:
                if "cnae_s" in args["filters"]:
                    if "cnae_r" in args["filters"]:
                        return gettext("Locations <cnae_r_article_with> that purchase domestically <cnae_s_article_from> <bra_s_article_in>")
                    if "hs" in args["filters"]:
                        return gettext("Locations that purchase <hs> domestically <cnae_s_article_from> <bra_s_article_in>")
                if "cnae_r" in args["filters"] and "hs" in args["filters"]:
                    return gettext("Locations <cnae_r_article_with> that purchase <hs> domestically <bra_s_article_from>")
            return gettext("Locations <cnae_r_article_with> that purchase <hs> domestically <cnae_s_article_from>")

        if filters == 2:

            if "bra_s" in args["filters"]:
                if "cnae_s" in args["filters"]:
                    return gettext("Locations that purchase domestically <cnae_s_active_from> <bra_s_article_in>")
                if "cnae_r" in args["filters"]:
                    return gettext("Locations <cnae_r_article_with> that purchase domestically <bra_s_article_from>")
                if "hs" in args["filters"]:
                    return gettext("Locations that purchase <hs> domestically <bra_s_article_from>")

            if "cnae_s" in args["filters"]:
                if "cnae_r" in args["filters"]:
                    return gettext("Locations <cnae_r_article_with> that purchase domestically <cnae_s_article_from>")
                if "hs" in args["filters"]:
                    return gettext("Locations that purchase <hs> domestically <cnae_s_article_from>")

            return gettext("Locations <cnae_r_article_with> that purchase <hs> domestically")

        if filters == 1:
            if "bra_s" in args["filters"]:
                return gettext("Locations that purchase domestically <bra_s_article_from>")
            if "cnae_s" in args["filters"]:
                return gettext("Locations that purchase domestically <cnae_s_article_from>")
            if "cnae_r" in args["filters"]:
                return gettext("Locations <cnae_r_article_with> that purchase domestically")
            if "hs" in args["filters"]:
                return gettext("Locations that purchase <hs> domestically")

    if args["display_key"] == "cnae_r":

        if filters == 4:
            return gettext("Industries <bra_r_article_in> that purchase <hs> domestically <cnae_s_article_from> <bra_s_article_in>")

        if filters == 3:

            if "bra_s" in args["filters"]:
                if "cnae_s" in args["filters"]:
                    if "bra_r" in args["filters"]:
                        return gettext("Industries <bra_r_article_in> that purchase domestically <cnae_s_article_from> <bra_s_article_in>")
                    if "hs" in args["filters"]:
                        return gettext("Industries that purchase <hs> domestically <cnae_s_article_from> <bra_s_article_in>")
                if "bra_r" in args["filters"] and "hs" in args["filters"]:
                    return gettext("Industries <bra_r_article_in> that purchase <hs> domestically <cnae_s_article_from>")
            return gettext("Industries that purchase <hs> domestically <cnae_r_article_from> <bra_r_article_in>")

        if filters == 2:

            if "bra_s" in args["filters"]:
                if "cnae_s" in args["filters"]:
                    return gettext("Industries that purchase domestically <cnae_s_article_from> <bra_s_article_in>")
                if "bra_r" in args["filters"]:
                    return gettext("Industries <bra_r_article_in> that purchase domestically <bra_r_article_from>")
                if "hs" in args["filters"]:
                    return gettext("Industries that purchase <hs> domestically <bra_s_article_from>")

            if "cnae_s" in args["filters"]:
                if "bra_r" in args["filters"]:
                    return gettext("Industries <bra_r_article_in> that purchase domestically <cnae_s_article_from>")
                if "hs" in args["filters"]:
                    return gettext("Industries that purchase <hs> domestically <cnae_s_article_from>")

            return gettext("Industries <bra_r_article_in> that purchase <hs> domestically")

        if filters == 1:
            if "bra_s" in args["filters"]:
                return gettext("Industries that purchase domestically <bra_s_article_from>")
            if "cnae_s" in args["filters"]:
                return gettext("Industries that purchase domestically <cnae_s_article_from>")
            if "bra_r" in args["filters"]:
                return gettext("Industries <bra_r_article_in> that purchase domestically")
            if "hs" in args["filters"]:
                return gettext("Industries that purchase <hs> domestically")

    if args["display_attr"] == "hs":

        if filters == 4:
            return gettext("Domestic trade <cnae_s_article_from> <bra_s_article_in> <cnae_s_article_to> <bra_r_article_in>")

        if filters == 3:

            if "bra_s" in args["filters"]:
                if "cnae_s" in args["filters"]:
                    if "bra_r" in args["filters"]:
                        return gettext("Domestic trade <cnae_s_article_from> <bra_s_article_in> <bra_r_article_to>")
                    if "cnae_r" in args["filters"]:
                        return gettext("Domestic trade <cnae_s_article_from> <bra_s_article_in> <cnae_r_article_to>")
                if "bra_r" in args["filters"] and "cnae_r" in args["filters"]:
                    return gettext("Domestic trade <bra_s_article_from> <cnae_r_article_to> <bra_r_article_in>")
            return gettext("Domestic trade <cnae_s_article_from> <cnae_r_article_to> <bra_r_article_in>")

        if filters == 2:

            if "bra_s" in args["filters"]:
                if "cnae_s" in args["filters"]:
                    return gettext("Domestic production <cnae_s_article_of> <bra_s_article_in>")
                if "bra_r" in args["filters"]:
                    return gettext("Domestic trade <bra_s_article_from> <bra_r_article_to>")
                if "cnae_r" in args["filters"]:
                    return gettext("Domestic trade <bra_s_article_from> <cnae_r_article_to>")

            if "cnae_s" in args["filters"]:
                if "bra_r" in args["filters"]:
                    return gettext("Domestic trade <cnae_s_article_from> <bra_r_article_to>")
                if "cnae_r" in args["filters"]:
                    return gettext("Domestic trade <cnae_s_article_from> <cnae_r_article_to>")

            return gettext("Domestic purchases <cnae_r_article_of> <bra_r_article_in>")

        if filters == 1:
            if "bra_s" in args["filters"]:
                return gettext("Domestic production <bra_s_article_in>")
            if "cnae_s" in args["filters"]:
                return gettext("Domestic production <cnae_s_article_of>")
            if "bra_r" in args["filters"]:
                return gettext("Domestic purchases <bra_r_article_of>")
            if "cnae_r" in args["filters"]:
                return gettext("Domestic purchases <cnae_r_article_of>")
