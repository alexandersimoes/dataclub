from flask.ext.babel import gettext

def title(args):

    if args["size"] == "trade_val":
        if args["display_attr"] == "hs":
            return gettext("Trade Balance <hs_article_for> <bra_article_in>")
        if args["display_attr"] == "wld":
            return gettext("Trade Balance <bra_article_from> <wld_article_to>")

    if args["size"] == "trade_net":
        if args["display_attr"] == "hs":
            return gettext("Net trade <hs_article_for> <bra_article_in>")
        if args["display_attr"] == "wld":
            return gettext("Net trade <bra_article_from> <wld_article_to>")

    if args["display_attr"] == "hs":

        if "wld" in args["filters"]:
            if args["size"] == "import_val":
                return gettext("Imports <bra_article_of> <wld_article_from>")
            if args["size"] == "export_val":
                return gettext("Exports <bra_article_of> <wld_article_to>")
            return gettext("Product trade between <bra_article_the> and <wld_article_the>")
        if args["size"] == "import_val":
            return gettext("Imports <bra_article_of>")
        if args["size"] == "export_val":
            return gettext("Exports <bra_article_of>")
        return gettext("International product trade <bra_article_of>")

    if args["display_attr"] == "wld":

        if "hs" in args["filters"]:
            if args["size"] == "import_val":
                return gettext("Import origins <hs_article_of> <bra_article_for>")
            if args["size"] == "export_val":
                return gettext("Export destinations <hs_article_of> <bra_article_from>")
            return gettext("Trade partners <hs_article_of> <bra_article_from>")
        if args["size"] == "import_val":
            return gettext("Import origins of products <bra_article_for>")
        if args["size"] == "export_val":
            return gettext("Export destinations of products <bra_article_from>")
        return gettext("Trade partners <bra_article_of>")

    if args["display_attr"] == "bra":

        if "hs" in args["filters"] and "wld" in args["filters"]:
            if args["size"] == "import_val":
                return gettext("Locations <bra_article_in> that import <hs> <wld_article_from>")
            return gettext("Locations <bra_article_in> that export <hs> <wld_article_to>")
        if "wld" in args["filters"] and "bra" in args["filters"]:
            if args["size"] == "import_val":
                return gettext("Locations <bra_article_in> that import <wld_article_from>")
            return gettext("Locations <bra_article_in> that export <wld_article_to>")
        if "hs" in args["filters"]:
            if args["size"] == "import_val":
                return gettext("Locations <bra_article_in> that import <hs>")
            return gettext("Locations <bra_article_in> that export <hs>")
        if args["size"] == "import_val":
            if "bra" not in args["filters"]:
                return gettext("Imports <bra_article_of> by State")
            return gettext("Imports <bra_article_of> by Municipality")
        if "bra" not in args["filters"]:
            return gettext("Exports <bra_article_of> by State")
        return gettext("Exports <bra_article_of> by Municipality")
