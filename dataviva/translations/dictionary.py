# -*- coding: utf-8 -*-
from flask.ext.babel import lazy_gettext, ngettext

singulars = {

    # Page Titles
    "builder": lazy_gettext("Advanced Visualization Builder"),

    # MONTHS
    "month_1": lazy_gettext("January"),
    "month_1_short": lazy_gettext("Jan"),
    "month_2": lazy_gettext("February"),
    "month_2_short": lazy_gettext("Feb"),
    "month_3": lazy_gettext("March"),
    "month_3_short": lazy_gettext("Mar"),
    "month_4": lazy_gettext("April"),
    "month_4_short": lazy_gettext("Apr"),
    "month_5": lazy_gettext("May"),
    "month_5_short": lazy_gettext("May"),
    "month_6": lazy_gettext("June"),
    "month_6_short": lazy_gettext("Jun"),
    "month_7": lazy_gettext("July"),
    "month_7_short": lazy_gettext("Jul"),
    "month_8": lazy_gettext("August"),
    "month_8_short": lazy_gettext("Aug"),
    "month_9": lazy_gettext("September"),
    "month_9_short": lazy_gettext("Sep"),
    "month_10": lazy_gettext("October"),
    "month_10_short": lazy_gettext("Oct"),
    "month_11": lazy_gettext("November"),
    "month_11_short": lazy_gettext("Nov"),
    "month_12": lazy_gettext("December"),
    "month_12_short": lazy_gettext("Dec"),

    # RAIS
    "rais": lazy_gettext("Employment"),
    "rais_search": lazy_gettext("Employment Visualizations"),
    "wage": lazy_gettext("Total Wages"),
    "wage_avg": lazy_gettext("Average Monthly Wage"),
    "num_emp": lazy_gettext("Employees"),
    "num_est": lazy_gettext("Establishments"),
    "wage_growth": lazy_gettext("Annual Wage Growth Rate (1 year)"),
    "wage_growth_5": lazy_gettext("Annual Wage Growth Rate (5 year)"),
    "num_emp_growth": lazy_gettext("Annual Employee Growth Rate (1 year)"),
    "num_emp_growth_5": lazy_gettext("Annual Employee Growth Rate (5 year)"),

    # SECEX
    "secex": lazy_gettext("International Trade"),
    "secex_search": lazy_gettext("International Trade Visualizations"),
    "export_val": lazy_gettext("Total Exports"),
    "import_val": lazy_gettext("Total Imports"),
    "trade_val": lazy_gettext("Trade Value"),
    "trade_net": lazy_gettext("Net Exports"),
    "export_import": lazy_gettext("Exports and Imports"),
    "import_val_growth": lazy_gettext("Annual Import Growth Rate (1 year)"),
    "import_val_growth_5": lazy_gettext("Annual Import Growth Rate (5 year)"),
    "export_val_growth": lazy_gettext("Annual Export Growth Rate (1 year)"),
    "export_val_growth_5": lazy_gettext("Annual Export Growth Rate (5 year)"),

    # EI
    "purchase_value": lazy_gettext("Total Domestic Trade"),

    # School Census
    "num_schools": lazy_gettext("Number of Schools"),

    # Higher Education (HEDU)
    "enrolled": lazy_gettext("Enrolled Students"),
    "graduates": lazy_gettext("Graduating Students"),
    "students": lazy_gettext("Registered Students"),
    "num_universities": lazy_gettext("Number of Universities"),
    "morning": lazy_gettext("Morning"),
    "afternoon": lazy_gettext("Afternoon"),
    "night": lazy_gettext("Night"),
    "full_time": lazy_gettext("Full Time"),

    # Calculations
    "distance": lazy_gettext("Distance"),
    "eci": lazy_gettext("Economic Complexity"),
    "opp_gain": lazy_gettext("Opportunity Gain"),
    "opp_gain_wld": lazy_gettext("International Opportunity Gain"),
    "pci": lazy_gettext("Product Complexity"),
    "rca": lazy_gettext("Domestic RCA"),
    "rca_wld": lazy_gettext("International RCA"),
    "rcd": lazy_gettext("Domestic RCD"),
    "bra_diversity": lazy_gettext("Location Diversity"),
    "cnae_diversity": lazy_gettext("Industry Diversity"),
    "cbo_diversity": lazy_gettext("Occupation Diversity"),
    "hs_diversity": lazy_gettext("Product Diversity"),
    "wld_diversity": lazy_gettext("Export Destination Diversity"),
    "importance": lazy_gettext("Importance"),
    "distance_wld": lazy_gettext("International Distance"),
    "proximity": lazy_gettext("Proximity"),

    # Population Statistics
    "pop": lazy_gettext("Population"),
    "pop_total": lazy_gettext("Total Population"),
    "pop_density": lazy_gettext("Population Density"),
    "pop_100km": lazy_gettext("Population within 100km"),
    "pop_employed": lazy_gettext("Employed Population"),
    "pop_active": lazy_gettext("Economically Active Population"),
    "pop_eligible": lazy_gettext("Work Eligible Population"),
    "pop_unemployed": lazy_gettext("Unemployed Population"),

    # Geography Statistics
    "capital_dist": lazy_gettext("Distance to Capital"),
    "capital_dist_med": lazy_gettext("Median Municipal Distance to Capital"),
    "area": lazy_gettext("Area"),
    "demonym": lazy_gettext("Demonym"),
    "climate": lazy_gettext("Climate"),
    "elevation": lazy_gettext("Elevation"),
    "airport_dist": lazy_gettext("Closest Airport"),
    "airport_dist_med": lazy_gettext("Median Municipal Airport Distance"),
    "seaport_dist": lazy_gettext("Closest Seaport"),
    "seaport_dist_med": lazy_gettext("Median Municipal Seaport Distance"),
    "neighbors": lazy_gettext("Neighboring Locations"),
    "inet_users": lazy_gettext("Internet Users (per 100)"),
    "gini": lazy_gettext("GINI"),
    "subregion": lazy_gettext("Subregion"),

    # Economy Statistics
    "gdp": lazy_gettext("GDP"),
    "gdp_per_capita": lazy_gettext("GDP/capita"),
    "hdi": lazy_gettext("HDI"),
    "hdi_edu": lazy_gettext("Education Index"),
    "hdi_health": lazy_gettext("Health Index"),
    "hdi_income": lazy_gettext("Income Index"),

    # Similar Statistic Lists
    "prox.cnae": lazy_gettext("Similar Industries"),
    "prox.cbo": lazy_gettext("Similar Occupations"),
    "prox.hs": lazy_gettext("Similar Products"),

    # Statistic Units
    "growth_unit": lazy_gettext("Percent"),

    # Visualization Small UI Buttons
    "comments": lazy_gettext("View Discussion"),
    "enlarge": lazy_gettext("Enlarge Visualization"),
    "minimize": lazy_gettext("Minimize Visualization"),

    # Visualiztion Controls
    "axes": lazy_gettext("Axes"),
    "color": lazy_gettext("Color"),
    "depth": lazy_gettext("Depth"),
    "grouping": lazy_gettext("Group"),
    "layout": lazy_gettext("Layout"),
    "order": lazy_gettext("Order"),
    "size": lazy_gettext("Sizing"),
    "scale": lazy_gettext("Scale"),
    "sort": lazy_gettext("Sort"),
    "spotlight": lazy_gettext("Highlight RCA"),
    "x": lazy_gettext("X Axis"),
    "y": lazy_gettext("Y Axis"),
    "asc": lazy_gettext("Ascending"),
    "desc": lazy_gettext("Descending"),
    "value": lazy_gettext("Value"),
    "share": lazy_gettext("Market Share"),
    "rca_scope": lazy_gettext("RCA Scope"),
    "bra_rca": lazy_gettext("Domestic"),
    "wld_rca": lazy_gettext("International"),
    "log": lazy_gettext("Log"),
    "linear": lazy_gettext("Linear"),
    "on": lazy_gettext("On"),
    "off": lazy_gettext("Off"),

    # User Messages
    "loading": lazy_gettext("Loading"),
    "search": lazy_gettext("Search")

}

def plurals(key=None, n=1):

    plurals = {

        "profile": ngettext("Profile", "Profiles", n),

        # BRA Attributes
        "bra": ngettext("Location", "Locations", n),
        "bra_1": ngettext("Region", "Regions", n),
        "bra_3": ngettext("State", "States", n),
        "bra_5": ngettext("Mesoregion", "Mesoregions", n),
        "bra_7": ngettext("Microregion", "Microregions", n),
        "bra_8": ngettext("Planning Region", "Planning Regions", n),
        "bra_9": ngettext("Municipality", "Municipalities", n),

        # HS Attributes
        "hs": ngettext("Product", "Products", n),
        "hs_2": ngettext("Section", "Sections", n),
        "hs_4": ngettext("Chapter", "Chapters", n),
        "hs_6": ngettext("Position", "Positions", n),
        "hs_8": ngettext("Sub-Position", "Sub-Positions", n),

        # WLD Attributes
        "wld": ngettext("Country", "Countries", n),
        "wld_2": ngettext("Continent", "Continents", n),
        "wld_5": ngettext("Country", "Countries", n),

        # CNAE Attributes
        "cnae": ngettext("Industry", "Industries", n),
        "cnae_1": ngettext("Section", "Sections", n),
        "cnae_3": ngettext("Division", "Divisions", n),
        "cnae_4": ngettext("Group", "Groups", n),
        "cnae_6": ngettext("Class", "Classes", n),

        # CBO Attributes
        "cbo": ngettext("Occupation", "Occupations", n),
        "cbo_1": ngettext("Main Group", "Main Groups", n),
        "cbo_2": ngettext("Principal Subgroup", "Principal Subgroups", n),
        "cbo_3": ngettext("Subgroup", "Subgroups", n),
        "cbo_4": ngettext("Family", "Families", n),
        "cbo_6": ngettext("Occupation", "Occupations", n),

        # COURSE_SC Attributes
        "course_sc": ngettext("Course", "Courses", n),
        "course_sc_2": ngettext("Field", "Fields", n),
        "course_sc_5": ngettext("Course", "Courses", n),

        # COURSE_HEDU Attributes
        "course_hedu": ngettext("Course", "Courses", n),
        "course_hedu_2": ngettext("Field", "Fields", n),
        "course_hedu_6": ngettext("Course", "Courses", n),

        # UNIVERSITY Attributes
        "university": ngettext("University", "Universities", n),
        "university_5": ngettext("University", "Universities", n),

        # Number Formatting
        "T": ngettext("Trillion", "Trillions", n),
        "B": ngettext("Billion", "Billions", n),
        "M": ngettext("Million", "Millions", n),
        "k": ngettext("Thousand", "Thousands", n),

        # Top Statistic Lists
        "top_bra": ngettext("Top Location", "Top Locations", n),
        "top.secex.export_val.hs_id": ngettext("Top Export", "Top Exports", n),
        "top.secex.import_val.hs_id": ngettext("Top Import", "Top Imports", n),
        "top.secex.import_val.wld_id": ngettext("Top Origin", "Top Origins", n),
        "top.secex.export_val.wld_id": ngettext("Top Destination", "Top Destinations", n),
        "top.rais.num_emp.cbo_id": ngettext("Top Occupation", "Top Occupations", n),
        "top.rais.num_emp.cnae_id": ngettext("Largest Industry", "Largest Industries", n),
        "top_hs_export": ngettext("Top Product Export", "Top Product Exports", n),
        "top_hs_import": ngettext("Top Product Import", "Top Product Imports", n),
        "top_input": ngettext("Top Domestic Input (EI)", "Top Domestic Inputs (EI)", n),
        "top_output": ngettext("Top Domestic Product (EI)", "Top Domestic Production (EI)", n),
        "top_school": ngettext("Top School", "Top Schools", n),
        "top.hedu.enrolled.university_id": ngettext("Top Universitie", "Top Universities", n),
        "top.hedu.enrolled.course_hedu_id": ngettext("Top Major", "Top Majors", n),
        "top.hedu.enrolled.bra_id": ngettext("Top Location", "Top Locations", n),
        "top.sc.enrolled.course_sc_id": ngettext("Top Vocational Course", "Top Vocational Courses", n),
        "top_bra_s": ngettext("Top Production Location", "Top Production Locations", n),
        "top_bra_r": ngettext("Top Consumption Location", "Top Consumption Locations", n),
        "top_cnae_s": ngettext("Top Production Industry", "Top Production Industries", n),
        "top_cnae_r": ngettext("Top Consumption Industry", "Top Consumption Industries", n),

        # Statistic Units
        "emp_unit": ngettext("Person", "People", n),
        "usd_unit": ngettext("US Dollar", "US Dollars", n),
        "brl_unit": ngettext("Brazilian Real", "Brazilian Reais", n),
        "pop_unit": ngettext("Person", "People", n),
        "stu_unit": ngettext("Student", "Students", n),

    }

    if key:
        return unicode(plurals[key]) if key in plurals else None
    return plurals

# OLD UNUSED TRANSLATIONS
#
#   "compare": lazy_gettext("Compare"),
#   "occugrid": lazy_gettext("Occugrid"),
#   "geo_map": lazy_gettext("Geo Map"),
#   "network": lazy_gettext("Network"),
#   "rings": lazy_gettext("Rings"),
#   "scatter": lazy_gettext("Scatter"),
#   "stacked": lazy_gettext("Stacked"),
#   "tree_map": lazy_gettext("Tree Map"),
#
#
#   "axes_desc_compare": lazy_gettext("Changes the X and Y variables used in the chart."),
#   "xaxis_var_desc_scatter": lazy_gettext("Changes the X axis variable."),
#   "yaxis_var_desc_scatter": lazy_gettext("Changes the Y axis variable."),
#
#
#   "order_desc_stacked": lazy_gettext("Changes the ordering of the visible areas based on the selected sorting."),
#
#
#
#   "layout_desc_stacked": lazy_gettext("Changes the X axis between value and market share."),
#
#
#   "rca_scope_desc_network": lazy_gettext("Changes which RCA variable is used when highlighting products in the app."),
#   "rca_scope_desc_rings": lazy_gettext("Changes which RCA variable is used when highlighting products in the app."),
#   "rca_scope_desc_scatter": lazy_gettext("Changes which RCA variable is used when highlighting products in the app."),
#
#
#   "scale_desc_compare": lazy_gettext("Changes the mathematical scale used on both axes."),
#
#
#   "spotlight_desc_network": lazy_gettext("Removes coloring from nodes which do not have RCA."),
#   "spotlight_scatter": lazy_gettext("Hide RCA"),
#   "spotlight_scatter_desc_scatter": lazy_gettext("Hides nodes that have RCA."),
#
#
#   "sort_desc_stacked": lazy_gettext("Changes the variable used to order the areas."),
#   "sort_desc_occugrid": lazy_gettext("Changes the variable used to order the donut charts."),
#
#   "sizing_desc_tree_map": lazy_gettext("Changes the variable used to size the rectangles."),
#   "sizing_desc_stacked": lazy_gettext("Changes the Y axis variable."),
#   "sizing_desc_network": lazy_gettext("Changes the variable used to size the circles."),
#   "sizing_desc_compare": lazy_gettext("Changes the variable used to size the circles."),
#   "sizing_desc_occugrid": lazy_gettext("Changes the variable used to size the circles."),
#   "sizing_desc_scatter": lazy_gettext("Changes the variable used to size the circles."),
#
#
#   "color_var_desc_tree_map": lazy_gettext("Changes the variable used to color the rectangles."),
#   "color_var_desc_stacked": lazy_gettext("Changes the variable used to color the areas."),
#   "color_var_desc_geo_map": lazy_gettext("Changes the variable used to color the locations."),
#   "color_var_desc_network": lazy_gettext("Changes the variable used to color the circles."),
#   "color_var_desc_rings": lazy_gettext("Changes the variable used to color the circles."),
#   "color_var_desc_compare": lazy_gettext("Changes the variable used to color the circles."),
#   "color_var_desc_occugrid": lazy_gettext("Changes the variable used to color the circles."),
#   "color_var_desc_scatter": lazy_gettext("Changes the variable used to color the circles."),
#
#
#   "active": lazy_gettext("Available"),
#   "available": lazy_gettext("Available"),
#   "not_available": lazy_gettext("Not available"),
#   "grouping_desc_occugrid": lazy_gettext("Groups the donut charts into different categorizations."),
#   "none": lazy_gettext("None"),
#   "year": lazy_gettext("Year"),
#
#
#   "depth_desc_tree_map": lazy_gettext("Changes the level of aggregation."),
#   "depth_desc_stacked": lazy_gettext("Changes the level of aggregation."),
#   "depth_desc_geo_map": lazy_gettext("Changes the level of aggregation."),
#   "depth_desc_network": lazy_gettext("Changes the level of aggregation."),
#   "depth_desc_rings": lazy_gettext("Changes the level of aggregation."),
#   "depth_desc_compare": lazy_gettext("Changes the level of aggregation."),
#   "depth_desc_occugrid": lazy_gettext("Changes the level of aggregation."),
#   "depth_desc_scatter": lazy_gettext("Changes the level of aggregation."),
#   "isic_1": lazy_gettext("Section"),
#   "isic_3": lazy_gettext("Division"),
#   "isic_4": lazy_gettext("Group"),
#   "isic_5": lazy_gettext("Class"),
#   "isic_1_plural": lazy_gettext("Sections"),
#   "isic_3_plural": lazy_gettext("Divisions"),
#   "isic_4_plural": lazy_gettext("Groups"),
#   "isic_5_plural": lazy_gettext("Classes"),
#
#   "eci_desc": lazy_gettext("Economic Complexity measures how diversified and complex a location's export production is."),
#   "pci_desc": lazy_gettext("Product Complexity is a measure of how complex a product is, based on how many countries export the product and how diversified those exporters are."),
#
#   "bra_diversity_desc": lazy_gettext("The number of unique municipalities where a given variable is present."),
#   "bra_diversity_eff": lazy_gettext("Effective Location Diversity"),
#   "bra_diversity_eff_desc": lazy_gettext("The diversity of a given variable corrected for the share that ea

#   "isic_diversity_desc": lazy_gettext("The number of unique 5-digit ISIC industries that are present for a given variable."),
#   "isic_diversity_eff": lazy_gettext("Effective Industry Diversity"),
#   "isic_diversity_eff_desc": lazy_gettext("The diversity of a given variable corrected for the share that each unit represents."),
#
#   "cbo_diversity_desc": lazy_gettext("The number of unique 4-digit CBO occupations that are present for a given variable."),
#   "cbo_diversity_eff": lazy_gettext("Effective Occupation Diversity"),
#   "cbo_diversity_eff_desc": lazy_gettext("The diversity of a given variable corrected for the share that each unit represents."),
#
#   "hs_diversity_desc": lazy_gettext("The number of unique HS4 products that are present for a given variable."),
#   "hs_diversity_eff": lazy_gettext("Effective Product Diversity"),
#   "hs_diversity_eff_desc": lazy_gettext("The diversity of a given variable corrected for the share that each unit represents."),
#
#   "wld_diversity_desc": lazy_gettext("The number of unique import countries that are present for a given variable."),
#   "wld_diversity_eff": lazy_gettext("Effective Export Destination Diversity"),
#   "wld_diversity_eff_desc": lazy_gettext("The diversity of a given variable corrected for the share that each unit represents."),
#
#   "distance_desc": lazy_gettext("Distance is a measure used to indicate how \"far away\" any given location is from a particular industry, occupation or product."),
#   "employed": lazy_gettext("Employed"),
#   "importance_desc": lazy_gettext("Importance measures the ubiquity of a given occupation in a particular industry. Occupations with a high importance in an industry are commonly employed in said industry."),
#   "elsewhere": lazy_gettext("Employees Available In Other Industries"),
#   "required": lazy_gettext("Estimated Employees"),
#   "required_desc": lazy_gettext("The estimated number of employees per establishment needed in order to have a successful establishment in an industry in a particular location."),
#   "growth_val": lazy_gettext("Wage Growth"),
#   "growth_val_total": lazy_gettext("Cumulative Wage Growth"),
#   "rca_desc": lazy_gettext("Revealed Comparative Advantage is a numeric value used to connote whether a particular product or industry is especially prominent in a location."),\
#
#   "opp_gain_desc": lazy_gettext("Opportunity gain is a measure that indicates how much diversity is offered by an industry or product should the given location develop it."),
#
#
#   "rais": lazy_gettext("Establishments and Employment (RAIS)"),
#   "num_emp_est": lazy_gettext("Employees per Establishment"),
#   "total_wage": lazy_gettext("Total Monthly Wage"),
#   "wage_avg_bra": lazy_gettext("Brazilian Average Wage"),
#
#
#   "secex": lazy_gettext("Product Exports (SECEX)"),
#   "total_val_usd": lazy_gettext("Total Exports"),
#
#
#   "brazil": lazy_gettext("Brazil"),
#   "bra_id": lazy_gettext("BRA ID"),
#   "category": lazy_gettext("Sector"),
#   "cbo_id": lazy_gettext("CBO ID"),
#   #"color": lazy_gettext("Sector"),
#   "color": lazy_gettext("Color"),
#   "display_id": lazy_gettext("ID"),
#   "hs_id": lazy_gettext("HS ID"),
#   "id_ibge": lazy_gettext("IBGE ID"),
#   "id": lazy_gettext("ID"),
#   "isic_id": lazy_gettext("ISIC ID"),
#   "name": lazy_gettext("Name"),
#   "name_en": lazy_gettext("Name (English)"),
#   "name_pt": lazy_gettext("Name (Portuguese)"),
#   "population": lazy_gettext("Population"),
#   "top": lazy_gettext("Top"),
#   "wld_id": lazy_gettext("WLD ID"),
#   "id_mdic": lazy_gettext("MDIC ID"),
#   "rank": lazy_gettext(" "),
#
#
#   "bra": lazy_gettext("Location"),
#   "bra_plural": lazy_gettext("Locations"),
#   "cbo": lazy_gettext("Occupation"),
#   "cbo_plural": lazy_gettext("Occupations"),
#   "hs": lazy_gettext("Product Export"),
#   "hs_plural": lazy_gettext("Product Exports"),
#   "icon": lazy_gettext("Icon"),
#   "isic": lazy_gettext("Industry"),
#   "isic_plural": lazy_gettext("Industries"),
#   "wld": lazy_gettext("Export Destination"),
#   "wld_plural": lazy_gettext("Export Destinations"),
#
#   "bra_add": lazy_gettext("add a location"),
#   "cbo_add": lazy_gettext("add an occupation"),
#   "hs_add": lazy_gettext("add a product"),
#   "isic_add": lazy_gettext("add an industry"),
#   "wld_add": lazy_gettext("add an export destination"),
#
#
#   "download": lazy_gettext("Download"),
#   "download_desc": lazy_gettext("Choose from the following file types:"),
#   "csv": lazy_gettext("Save as CSV"),
#   "csv_desc": lazy_gettext("A table format that can be imported into a database or opened with Microsoft Excel."),
#   "pdf": lazy_gettext("Save as PDF"),
#   "pdf_desc": lazy_gettext("Similar to SVG files, PDF files are vector-based and can be dynamically scaled."),
#   "png": lazy_gettext("Save as PNG"),
#   "png_desc": lazy_gettext("A standard image file, similar to JPG or BMP."),
#   "svg": lazy_gettext("Save as SVG"),
#   "svg_desc": lazy_gettext("A vector-based file that can be resized without worrying about pixel resolution."),
#
#
#   "basics": lazy_gettext("Basic Values"),
#   "growth": lazy_gettext("Growth"),
#   "calculations": lazy_gettext("Strategic Indicators"),
#   "Data Provided by": lazy_gettext("Data Provided by"),
#   "View more visualizations on the full DataViva.info website.": lazy_gettext("View more visualizations on the full DataViva.info website."),
#   "related_apps": lazy_gettext("Related Apps"),
#   "other_apps": lazy_gettext("Other Apps"),
#   "Show All Years": lazy_gettext("Show All Years"),
#   "Build Not Available": lazy_gettext("Build Not Available"),
#   "Building App": lazy_gettext("Building App"),
#   "Downloading Additional Years": lazy_gettext("Downloading Additional Years"),
#   "and": lazy_gettext("and"),
#   "showing": lazy_gettext("Showing only"),
#   "excluding": lazy_gettext("Excluding"),
#   "of": lazy_gettext("of"),
#   "with": lazy_gettext("with"),
#   "and": lazy_gettext("and"),
#   "fill": lazy_gettext("Fill"),
#   "embed_url": lazy_gettext("Embed URL"),
#   "share_url": lazy_gettext("Shortened URL"),
#   "social_media": lazy_gettext("Social Networks"),
#   "secex_2": lazy_gettext("Based on State Production"),
#   "secex_8": lazy_gettext("Based on the Exporting Municipality"),
#
#
#   "Click for More Info": lazy_gettext("Click for more data and related apps."),
#   "Click to Zoom": lazy_gettext("Click to Zoom"),
#   "filter": lazy_gettext("Hide Group"),
#   "solo": lazy_gettext("Solo Group"),
#   "reset": lazy_gettext("Click to Reset all Filters"),
#   "Primary Connections": lazy_gettext("Primary Connections"),
#   "No Data Available": lazy_gettext("No Data Available"),
#   "No Connections Available": lazy_gettext("No Connections Available"),
#
#
#   "Asked": lazy_gettext("Asked"),
#   "by": lazy_gettext("by"),
#   "point": lazy_gettext("Point"),
#   "points": lazy_gettext("Points"),
#   "reply": lazy_gettext("Reply"),
#   "replies": lazy_gettext("Replies"),
#   "votes": lazy_gettext("Most Active"),
#   "newest": lazy_gettext("Most Recent"),
#   "questions": lazy_gettext("Questions"),
#   "learnmore_plural": lazy_gettext("Learn more"),
#   "flagged": lazy_gettext("This reply has been flagged."),
#   "unflagged": lazy_gettext("This flag on this reply has been removed."),
#   "voted": lazy_gettext("Your vote has been added."),
#   "unvoted": lazy_gettext("Your vote was removed."),
#
#
#   "edit": lazy_gettext("Edit"),
#   "visible": lazy_gettext("Visible"),
#   "hidden": lazy_gettext("Hidden"),
#   "user": lazy_gettext("User"),
#   "admin": lazy_gettext("Admin"),
#   "remove": lazy_gettext("Remove"),
#   "remove_confirmation": lazy_gettext("Are you sure to delete this item?"),
#
#
#   "search": lazy_gettext("Search"),
#   "search_results": lazy_gettext("Search Results"),
#   "select": lazy_gettext("Select"),
#   "show": lazy_gettext("Show"),
#   "loading_attrs": lazy_gettext("Loading Attribute List"),
#   "loading_items": lazy_gettext("Loading More Items"),
#   "wait": lazy_gettext("Please Wait"),
#   "back": lazy_gettext("Back"),
#   "Municipalities within": lazy_gettext("Municipalities within"),
#   "No municipalities within that distance.": lazy_gettext("No municipalities within that distance."),
#   "Including": lazy_gettext("Including"),
#
#   "article_pt": lazy_gettext("Portuguese content"),
#   "gender_pt": lazy_gettext("Gender"),
#   "gender": lazy_gettext("Gender"),
#   "id_ibge": lazy_gettext("IBGE ID"),
#   "plural_pt": lazy_gettext("Plural"),
#   "population": lazy_gettext("Population"),
#   "num_emp": lazy_gettext("Employees"),
#   "val_usd": lazy_gettext("Exports"),
#   "desc_en": lazy_gettext("Description"),
#   "id_2char": lazy_gettext("ISO Code"),
#   "id_3char": lazy_gettext("Name abbr"),
#   "id_mdic": lazy_gettext("MDIC ID"),
#   "id_num": lazy_gettext("NUM ID"),
#   "plr": lazy_gettext("plr"),
