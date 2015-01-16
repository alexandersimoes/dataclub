import os
from sqlalchemy import func, desc, and_, or_
from flask import Blueprint, request, jsonify, abort, g, render_template, make_response, redirect, url_for, flash
from flask.views import View

from dataviva import db, __data_years__, app
from dataviva.attrs.models import Bra, Bra_stats, Wld, Hs, Cnae, Cbo, School, University, Course_hedu, Course_sc, D
from dataviva.secex.models import Ymp, Ymw
from dataviva.rais.models import Yi, Yo
from dataviva.hedu.models import Yu, Yc
from dataviva.ask.models import Question

from dataviva.utils.gzip_data import gzipped
from dataviva.utils.cached_query import cached_query

mod = Blueprint('attrs', __name__, url_prefix='/attrs')

@mod.before_request
def before_request():
    lang = request.args.get('lang', None) or g.locale
    lang = lang if lang in ("en", "pt") else g.locale
    cache_key = os.path.join(request.path, lang)
    prev = cached_query(cache_key)
    if prev:
        return prev

@mod.after_request
def after_request(response):
    lang = request.args.get('lang', None) or g.locale
    lang = lang if lang in ("en", "pt") else g.locale
    cache_key = os.path.join(request.path, lang)
    if not cached_query(cache_key):
        cached_query(cache_key, response)
    return response

############################################################
# ----------------------------------------------------------
# All attribute views
#
############################################################
class AttrsView(View):

    def __init__(self):
        self.lang = request.args.get('lang', None) or g.locale
        self.depth = request.args.get('depth', None)
        self.order = request.args.get('order', None)
        self.offset = request.args.get('offset', None)
        self.limit = request.args.get('limit', None)
        if self.offset:
            self.offset = float(self.offset)
            self.limit = self.limit or 50

    def get_objects(self):
        attr_filter = self.attr_filter
        Attr = self.Attr
        Weight = getattr(self, "Weight", None)
        Weight_col = getattr(self, "Weight_col", None)
        query = self.query

        if attr_filter:
            # the .show. indicates that we are looking for a specific nesting
            if ".show." in attr_filter:
                this_attr, nesting_level = attr_filter.split(".show.")
                # filter table by requested nesting level
                query = query.filter(Attr.id.startswith(this_attr)) \
                        .filter(func.char_length(Attr.id) == nesting_level)

            # the show. indicates that we are looking for a specific nesting
            elif "show." in attr_filter:
                nesting_level = attr_filter.split(".")[1]
                # filter table by requested nesting level
                query = query.filter(func.char_length(Attr.id) == nesting_level)

            else:
                return query.filter(Attr.id == attr_filter).all()
        else:

            # is the depth specified?
            if self.depth:
                query = query.filter(func.char_length(Attr.id) == self.depth)
            else:
                query = query.filter(func.char_length(Attr.id).in_(Attr.depths))

        # is an order specified?
        if self.order:
            direction = "asc"

            if "." in self.order:
                o, direction = self.order.split(".")
            else:
                o = self.order

            if o == "name":
                o = "name_{0}".format(self.lang)

            if hasattr(Weight, o):
                order_table = Weight
            else:
                order_table = Attr

            o = getattr(order_table,o,None)
            if o:
                if direction == "desc" or direction == "descending":
                    query = query.order_by(desc(o))
                else:
                    query = query.order_by(o)

        # is a limit specified?
        if self.limit:
            query = query.limit(self.limit).offset(self.offset)

        return query.all()

    def serialize(self, objects, lang=None):
        data = []
        header = [item for sublist in self.columns for item in sublist]
        header = [h.replace("_en", "").replace("_pt", "") for h in header]
        for obj in objects:
            obj = obj if isinstance(obj, (list, tuple)) else (obj,)
            obj_serialized = []
            for o, o_header in zip(obj, self.columns):
                if isinstance(o, self.Attr):
                    obj_serialized += [o.serialize(lang).get(h, None) for h in o_header]
                elif isinstance(o, self.Weight):
                    obj_serialized += [getattr(o, h) if o else None for h in o_header]
                else:
                    obj_serialized += [o]
            data.append(obj_serialized)
        return header, data

    def dispatch_request(self, attr_filter=None):
        lang = request.args.get('lang', None) or g.locale
        lang = lang if lang in ("en", "pt") else g.locale
        self.attr_filter = attr_filter
        objects = self.get_objects()
        headers, serialized_data = self.serialize(objects, lang)
        weight = self.Weight_col.key if getattr(self, "Weight_col", None) else None
        return jsonify(headers=headers, data=serialized_data,
                       depths=self.Attr.depths, weight=weight)

class BraView(AttrsView):

    def __init__(self):
        super(BraView, self).__init__()
        self.Attr = Bra
        self.Weight = Bra_stats
        self.Weight_col = Bra_stats.pop
        self.query = db.session.query(self.Attr, self.Weight) \
            .outerjoin(self.Weight, self.Weight.bra_id == self.Attr.id)
        if self.lang == 'en':
            attr_cols = ('name', 'icon')
        else:
            attr_cols = ('name', 'icon', 'gender', 'plural', 'article')
        self.columns = [('id',)+attr_cols+('color',), ('pop',)]

class HsView(AttrsView):

    def __init__(self):
        super(HsView, self).__init__()
        self.latest_year = __data_years__["secex"][1]
        self.Attr = Hs
        self.Weight = Ymp
        self.Weight_col = Ymp.export_val
        self.query = db.session.query(self.Attr, Ymp) \
            .outerjoin(Ymp, and_(Ymp.hs_id == self.Attr.id, Ymp.year == self.latest_year, Ymp.month == 0))
        if self.lang == 'en':
            attr_cols = ('name', 'icon')
        else:
            attr_cols = ('name', 'icon', 'gender', 'plural', 'article')
        self.columns = [('id',)+attr_cols+('color',), ('export_val',)]

class WldView(AttrsView):

    def __init__(self):
        super(WldView, self).__init__()
        self.latest_year = __data_years__["secex"][1]
        self.Attr = Wld
        self.Weight = Ymw
        self.Weight_col = self.Weight.export_val
        self.query = db.session.query(self.Attr, self.Weight) \
            .outerjoin(self.Weight, and_(self.Weight.wld_id == self.Attr.id, self.Weight.year == self.latest_year, self.Weight.month == 0))
        if self.lang == 'en':
            attr_cols = ('name', 'icon')
        else:
            attr_cols = ('name', 'icon', 'gender', 'plural', 'article')
        self.columns = [('id',)+attr_cols+('color',), ('export_val',)]


class CnaeView(AttrsView):

    def __init__(self):
        super(CnaeView, self).__init__()
        self.latest_year = __data_years__["rais"][1]
        self.Attr = Cnae
        self.Weight = Yi
        self.Weight_col = self.Weight.num_emp
        self.query = db.session.query(self.Attr, self.Weight) \
            .outerjoin(self.Weight, and_(self.Weight.cnae_id == self.Attr.id, self.Weight.year == self.latest_year))
        if self.lang == 'en':
            attr_cols = ('name', 'icon')
        else:
            attr_cols = ('name', 'icon', 'gender', 'plural', 'article')
        self.columns = [('id',)+attr_cols+('color',), ('num_emp',)]



class CboView(AttrsView):

    def __init__(self):
        super(CboView, self).__init__()
        self.latest_year = __data_years__["rais"][1]
        self.Attr = Cbo
        self.Weight = Yo
        self.Weight_col = self.Weight.num_emp
        self.query = db.session.query(self.Attr, self.Weight) \
            .outerjoin(self.Weight, and_(self.Weight.cbo_id == self.Attr.id, self.Weight.year == self.latest_year))
        if self.lang == 'en':
            attr_cols = ('name', 'icon')
        else:
            attr_cols = ('name', 'icon', 'gender', 'plural', 'article')
        self.columns = [('id',)+attr_cols+('color',), ('num_emp',)]



class SchoolView(AttrsView):

    def __init__(self):
        super(SchoolView, self).__init__()
        self.latest_year = __data_years__["sc"][1]
        self.Attr = School
        bra = request.args.get('bra', '4mg')
        bra = Bra.query.get(bra[:3]).id_ibge
        # self.Weight = Yo
        # self.Weight_col = self.Weight.num_emp
        self.query = self.Attr.query.filter(self.Attr.id.startswith(bra))
        if self.lang == 'en':
            attr_cols = ('name', 'icon')
        else:
            attr_cols = ('name', 'icon', 'gender', 'plural', 'article')
        self.columns = [('id',)+attr_cols+('color',)]

class CourseScView(AttrsView):

    def __init__(self):
        super(CourseScView, self).__init__()
        self.latest_year = __data_years__["sc"][1]
        # self.Weight = Yo
        # self.Weight_col = self.Weight.num_emp
        self.Attr = Course_sc
        self.query = self.Attr.query
        # raise Exception(self.query)
        if self.lang == 'en':
            attr_cols = ('name', 'icon')
        else:
            attr_cols = ('name', 'icon', 'gender', 'plural', 'article')
        self.columns = [('id',)+attr_cols+('color',)]

class UniversityView(AttrsView):

    def __init__(self):
        super(UniversityView, self).__init__()
        self.latest_year = __data_years__["hedu"][1]
        self.Weight = Yu
        self.Weight_col = self.Weight.enrolled
        self.Attr = University
        self.query = db.session.query(self.Attr, self.Weight) \
            .outerjoin(self.Weight, and_(self.Weight.university_id == self.Attr.id, self.Weight.year == self.latest_year))
        # raise Exception(self.query)
        if self.lang == 'en':
            attr_cols = ('name', 'icon')
        else:
            attr_cols = ('name', 'icon', 'gender', 'plural', 'article')
        self.columns = [('id',)+attr_cols+('color',), ('enrolled',)]

class CourseHeduView(AttrsView):

    def __init__(self):
        super(CourseHeduView, self).__init__()
        self.latest_year = __data_years__["hedu"][1]
        self.Weight = Yc
        self.Weight_col = self.Weight.enrolled
        self.Attr = Course_hedu
        self.order = "year"
        self.query = db.session.query(self.Attr, func.avg(self.Weight_col)) \
            .outerjoin(self.Weight, and_(self.Weight.course_hedu_id == self.Attr.id)) \
            .group_by(self.Weight.course_hedu_id)
        # raise Exception(self.query)
        if self.lang == 'en':
            attr_cols = ('name', 'icon')
        else:
            attr_cols = ('name', 'icon', 'gender', 'plural', 'article')
        self.columns = [('id',)+attr_cols+('color',), ('enrolled',)]

class DView(AttrsView):

    def __init__(self):
        super(DView, self).__init__()
        # self.Weight = Yo
        # self.Weight_col = self.Weight.num_emp
        self.Attr = D
        self.query = self.Attr.query
        # raise Exception(self.query)
        if self.lang == 'en':
            attr_cols = ('name', 'icon', 'category')
        else:
            attr_cols = ('name', 'icon', 'gender', 'plural', 'article', 'category')
        self.columns = [('id',)+attr_cols+('color',)]

@mod.route('/search/<term>/')
def attrs_search(term=None):
    # Dictionary
    bra_query = {}
    cbo_query = {}
    cnae_query = {}
    hs_query = {}
    question_query = {}
    wld = {}
    lang = request.args.get('lang', None) or g.locale
    result = []


    bra = Bra.query.filter(or_(Bra.id == term, or_(Bra.name_pt.ilike("%"+term+"%"), Bra.name_en.ilike("%"+term+"%"))))
    items = bra.limit(50).all()
    items = [i.serialize() for i in items]

    for i in items:
        bra_query = {}
        bra_query["id"] = i["id"]
        bra_query["name_pt"] = i["name_pt"]

        if i["id"] == "bra":
            icon = "all"
        else:
            icon = i["id"][0:2]

        bra_query["icon"] = "/static/images/icons/bra/bra_" + icon
        bra_query["name_en"] = i["name_en"]
        bra_query["color"] = i["color"]
        bra_query["content_type"] = "bra"
        bra_query = fix_name(bra_query, lang)
        result.append(bra_query)

    if lang == "pt":
        cbo = Cbo.query.filter(or_(Cbo.id == term, Cbo.name_pt.ilike("%"+term+"%")))
    else:
        cbo = Cbo.query.filter(or_(Cbo.id == term, Cbo.name_en.ilike("%"+term+"%")))

    items = cbo.limit(50).all()
    items = [i.serialize() for i in items]

    for i in items:
        cbo_query = {}
        cbo_query["id"] = i["id"]
        cbo_query["name_pt"] = i["name_pt"]
        cbo_query["name_en"] = i["name_en"]
        cbo_query["color"] = i["color"]
        cbo_query["content_type"] = "cbo"
        cbo_query = fix_name(cbo_query, lang)
        result.append(cbo_query)

    cnae_match = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u"]

    if lang == "pt":
        cnae = Cnae.query.filter(and_(Cnae.name_pt.ilike("%"+term+"%"), Cnae.id.in_(cnae_match)))
    else:
        cnae = Cnae.query.filter(and_(Cnae.name_en.ilike("%"+term+"%"), Cnae.id.in_(cnae_match)))

    items = cnae.limit(50).all()
    items = [i.serialize() for i in items]

    for i in items:
        cnae_query = {}
        cnae_query["id"] = i["id"]
        cnae_query["name_pt"] = i["name_pt"]
        cnae_query["name_en"] = i["name_en"]
        cnae_query["color"] = i["color"]
        cnae_query["content_type"] = "cnae"
        cnae_query = fix_name(cnae_query, lang)
        result.append(cnae_query)

    if lang == "pt":
        hs = Hs.query.filter(or_(Hs.id == term, Hs.name_pt.like("%"+term+"%")))
    else:
        hs = Hs.query.filter(or_(Hs.id == term, Hs.name_en.ilike("%"+term+"%")))

    items = hs.limit(50).all()

    items = [i.serialize() for i in items]

    for i in items:
        hs_query = {}
        hs_query["id"] = i["id"]
        hs_query["name_pt"] = i["name_pt"]
        hs_query["name_en"] = i["name_en"]
        hs_query["color"] = i["color"]
        hs_query["content_type"] = "hs"
        hs_query = fix_name(hs_query,lang)
        result.append(hs_query)


    if lang == "pt":
        wld = Wld.query.filter(or_(Wld.id == term, Wld.name_pt.like("%"+term+"%")))
    else:
        wld = Wld.query.filter(or_(Wld.id == term, Wld.name_en.like("%"+term+"%")))

    items = wld.limit(50).all()
    items = [i.serialize() for i in items]

    for i in items:
        wld_query = {}
        wld_query["id"] = i["id"]
        wld_query["name_pt"] = i["name_pt"]
        wld_query["name_en"] = i["name_en"]
        wld_query["color"] = i["color"]
        wld_query["content_type"] = "wld"
        wld_query = fix_name(wld_query, lang)
        result.append(wld_query)

    question = Question.query.filter(and_(Question.language == lang, or_(Question.question.ilike("%"+term+"%"), Question.body.ilike("%"+term+"%"))))

    items = question.limit(50).all()
    items = [i.serialize() for i in items]

    for i in items:
        question_query = {}
        question_query["id"] = i["slug"]
        question_query["name"] = i["question"]
        question_query["color"] = '#D67AB0'
        question_query["content_type"] = "learnmore"
        question_query = fix_name(question_query, lang)
        result.append(question_query)


    ret = jsonify({"activities":result})

    return ret

def register_endpoints():
    views = [('/school/', SchoolView.as_view('school')),
            ('/school/<attr_filter>/', SchoolView.as_view('school_filter')),
            ('/bra/', BraView.as_view('bra')),
            ('/bra/<attr_filter>/', BraView.as_view('bra_filter')),
            ('/hs/', HsView.as_view('hs')),
            ('/hs/<attr_filter>/', HsView.as_view('hs_filter')),
            ('/d/', DView.as_view('d')),
            ('/d/<attr_filter>/', DView.as_view('d_filter')),
            ('/course_hedu/', CourseHeduView.as_view('course_hedu')),
            ('/course_hedu/<attr_filter>/', CourseHeduView.as_view('course_hedu_filter')),
            ('/university/', UniversityView.as_view('university')),
            ('/universiry/<attr_filter>/', UniversityView.as_view('university_filter')),
            ('/course_sc/', CourseScView.as_view('course_sc')),
            ('/course_sc/<attr_filter>/', CourseScView.as_view('course_sc_filter')),
            ('/cbo/', CboView.as_view('cbo')),
            ('/cbo/<attr_filter>/', CboView.as_view('cbo_filter')),
            ('/cnae/', CnaeView.as_view('cnae')),
            ('/cnae/<attr_filter>/', CnaeView.as_view('cnae_filter')),
            ('/wld/', WldView.as_view('wld')),
            ('/wld/<attr_filter>/', WldView.as_view('wld_filter'))]

    for endpoint, view_obj in views:
        gzipped_view = gzipped(view_obj)
        mod.add_url_rule(endpoint, view_func=gzipped_view)

register_endpoints()
