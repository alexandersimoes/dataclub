import json
from datetime import datetime
from flask import Blueprint, render_template, g, request, current_app, session, redirect, url_for, flash, abort, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.babel import gettext
from sqlalchemy import func, or_

import time

mod = Blueprint('general', __name__, url_prefix='/')

from dataviva import app, db, babel, __data_years__, view_cache
from dataviva.general.forms import AccessForm
from dataviva.general.models import Short
from dataviva.account.models import User

from dataviva.attrs.models import Bra, Cnae, Hs, Cbo, Wld, Course_hedu

from dataviva.profile.profiles import *

from dataviva.rais.models import Yio, Ii
from dataviva.stats.helper import stats_list, recent_profile_pages, percapita_exports
from dataviva.stats.helper import cbo_demographic_breakdown, hedu_demographic_breakdown

from dataviva.utils.cached_query import cached_query, make_cache_key
from dataviva.utils.num_format import affixes
from dataviva.translations.translate import translate

from config import ACCOUNTS, ERROR_EMAIL, DEBUG
from dataviva.account.views import get_userid


#utils
# from ..utils import send_mail

###############################
# General functions for ALL views
# ---------------------------
@app.before_request
def before_request():
    g.accounts = True if ACCOUNTS in ["True","true","Yes","yes","Y","y",1] else False
    g.page_type = mod.name
    g.latest_year = {}
    for dataset in __data_years__:
        g.latest_year[dataset] = __data_years__[dataset][1]

    # Save variable in session so we can determine if this is the user's
    # first time on the site
    if 'first_time' in session:
        session['first_time'] = False
    else:
        session['first_time'] = True

    # Check if the user is logged in, if so give the global object
    # a reference to the user from DB
    g.user = current_user
    if g.user.is_authenticated() and request.endpoint != 'static':
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

    # Set the locale to either 'pt' or 'en' on the global object
    if request.endpoint != 'static':
        g.locale = get_locale()

    # Set local storage timeouts for the attr types
    g.storage = {
        "bra": 8,
        "hs": 8,
        "wld": 8,
        "cnae": 8,
        "cbo": 8,
        "school": 8,
        "course_sc": 8,
        "university": 8,
        "course_hedu": 8,
        "d": 8,
    }

    g.dict    = json.dumps(translate())
    g.affixes = json.dumps(affixes())

@babel.localeselector
def get_locale(lang=None):
    supported_langs = current_app.config['LANGUAGES'].keys()
    new_lang = request.accept_languages.best_match(supported_langs, "en")
    # user = getattr(g, 'user', None)
    user = current_user
    if lang:
        if lang in supported_langs:
            new_lang = lang
        if user.is_authenticated():
            # set users preferred lang
            user.language = new_lang
            db.session.add(user)
            db.session.commit()
        else:
            session['locale'] = new_lang
    else:
        current_locale = getattr(g, 'locale', None)
        # return new_lang
        if current_locale:
            new_lang = current_locale
        elif user.is_authenticated():
            user_preferred_lang = getattr(user, 'language', None)
            if user_preferred_lang and user_preferred_lang in supported_langs:
                new_lang = user_preferred_lang
            else:
                # set users preferred lang
                user.language = new_lang
                db.session.add(user)
                db.session.commit()
        elif 'locale' in session:
            new_lang = session['locale']
        else:
            session['locale'] = new_lang

    return new_lang

@babel.timezoneselector
def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone

###############################
# General views
# ---------------------------
@app.after_request
def after_request(response):
    return response

@mod.route('/', methods=['GET', 'POST'])
@view_cache.cached(key_prefix=make_cache_key)
def home():
    g.page_type = "home"
    lists = []
    limit = 10
    param_str = "/stats/carosel/?metric=%s&show=%s&profile=%s&limit=%s"

    featured = [
        BraProfile("4mg030000"),
        BraProfile("2al010103"),
        BraProfile("4sp140505"),
        BraProfile("3go000000"),
        BraProfile("2pe020206"),
    ]

    metric, show, profile = "export_val", "bra_id", BraProfile
    cities = stats_list(metric, show, limit=limit, depth=9)
    pages = [profile(b) for b in cities]
    lists.append({"title": gettext("Top Exporting Municipalities"), "pages": pages, "parameters" : param_str % (metric,show,profile.__name__,limit)})

    metric, show, profile = "export_val", "hs_id", HsProfile
    prods = stats_list(metric, show, limit=limit)
    pages = [profile(p) for p in prods]
    lists.append({"title": gettext("Largest Brazilian Exports"), "pages": pages, "parameters":  param_str % (metric,show,profile.__name__,limit)})
    
    metric, show, profile = "wage_avg", "cbo_id", CboProfile
    cbos = stats_list(metric, show, limit=limit)
    pages = [profile(c) for c in cbos]
    lists.append({"title": gettext("Highest Paid Occupations"), "pages": pages, "parameters": param_str % (metric,show,profile.__name__,limit)})

    metric, show, profile = "export_val", "wld_id", WldProfile
    prods = stats_list(metric, show, limit=limit)
    pages = [profile(p) for p in prods]
    lists.append({"title": gettext("Top Export Destinations"), "pages": pages, "parameters":  param_str % (metric,show,profile.__name__,limit)})

    metric, show, profile = "enrolled", "course_hedu_id", Course_heduProfile
    courses = stats_list(metric, show, limit=limit, depth=6)
    pages = [profile(u) for u in courses]
    lists.append({"title": gettext("Most Popular Majors"), "pages": pages, "parameters" : param_str % (metric,show,profile.__name__,limit)})
    
    majors = hedu_demographic_breakdown(d_id='B')
    pages = [Course_heduProfile(m) for m in majors]
    lists.append({"title": gettext("Majors With A High Majority of Female Students"), "pages": pages, "parameters" : "/stats/hedu/course_hedu/d/?d_id=B&limit=%s" % (limit)})

    majors = hedu_demographic_breakdown(d_id='A')
    pages = [Course_heduProfile(m) for m in majors]
    lists.append({"title": gettext("Majors With A High Majority of Male Students"), "pages": pages, "parameters" : "/stats/hedu/course_hedu/d/?d_id=A&limit=%s" % (limit)})

    metric, show, profile = "enrolled", "university_id", UniversityProfile
    universities = stats_list(metric, show, limit=limit, depth=5)
    pages = [profile(u) for u in universities]
    lists.append({"title": gettext("Largest Universities"), "pages": pages, "parameters" : param_str % (metric,show,profile.__name__,limit)})

    cities = percapita_exports()
    pages = [BraProfile(b) for b in cities]
    lists.append({"title": gettext("Top Exporting Municipalities Per Capita"), "pages": pages, "parameters" : "/stats/secex/percapita?limit=%s" % (limit)})

    metric, show, profile = "import_val", "hs_id", HsProfile
    prods = stats_list(metric, show, limit=limit)
    pages = [profile(p) for p in prods]
    lists.append({"title": gettext("Largest Brazilian Imports"), "pages": pages, "parameters":  param_str % (metric,show,profile.__name__,limit)})

    cities = cbo_demographic_breakdown(d_id='B')
    pages = [CboProfile(b) for b in cities]
    lists.append({"title": gettext("Highest Percentage Female Occupations"), "pages": pages, "parameters" : "/stats/rais/cbo/d/?d_id=B&limit=%s" % (limit)})

    cities = cbo_demographic_breakdown(d_id='A')
    pages = [CboProfile(b) for b in cities]
    lists.append({"title": gettext("Highest Percentage Male Occupations"), "pages": pages, "parameters" : "/stats/rais/cbo/d/?d_id=A&limit=%s" % (limit)})

    metric, show, profile = "num_emp_growth", "cnae_id", CnaeProfile
    prods = stats_list(metric, show, limit=limit)
    pages = [profile(p) for p in prods]
    lists.append({"title": gettext("Industries with Highest Employee Growth"), "pages": pages, "parameters":  param_str % (metric,show,profile.__name__,limit)})

    metric, show, profile = "num_emp_growth", "cnae_id", CnaeProfile
    prods = stats_list(metric, show, sort="asc", limit=limit)
    pages = [profile(p) for p in prods]
    lists.append({"title": gettext("Industries with Lowest Employee Growth"), "pages": pages, "parameters":  (param_str + "&sort=asc") % (metric,show,profile.__name__,limit)})

    return render_template("general/home.html", featured = featured, lists = lists)

@mod.route('close/')
def close():
    return render_template("general/close.html")

@mod.route('upgrade/')
def upgrade():
    return render_template("general/upgrade.html")

@mod.route('access/')
@mod.route('access/logout/')
def access():
    session['has_access'] = False
    return redirect(url_for('general.home'))

###############################
# Set language views
# ---------------------------
@mod.route('set_lang/<lang>/')
def set_lang(lang):
    g.locale = get_locale(lang)
    return redirect(request.args.get('next') or \
               request.referrer or \
               url_for('general.home'))

###############################
# Handle shortened URLs
# ---------------------------
# @mod.route('<slug>/')
# def redirect_short_url(slug):
    # short = Short.query.filter_by(slug = slug).first_or_404()
    # short.clicks += 1
    # db.session.add(short)
    # db.session.commit()

    # return redirect(short.long_url)

def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']

@mod.route('med_num_emp/<cnae>/')
def med_num_emp(cnae):
    return render_template("general/med_num_emp.html", cnae=cnae)

@mod.route('med_num_emp/<cnae>/data/')
def med_num_emp_data(cnae):
    q = Yio.query \
            .filter_by(year=2002) \
            .filter_by(cnae_id=cnae) \
            .filter(or_(Yio.med_num_emp_sm != None, Yio.med_num_emp_med != None, Yio.med_num_emp_lg != None, Yio.med_num_emp_xl != None)) \
            .filter(func.char_length(Yio.cbo_id) == 4)
    # raise Exception(q.all()[0])
    return jsonify(data=[yio.serialize() for yio in q.all()])

@mod.route('cnae_space/data/')
def cnae_space_generate_data():
    def frange(x, y, jump):
        while x < y:
            yield x
            x += jump
    # select cnae_id, cnae_id_t, proximity from rais_ii where cnae_id = "a01610" and length(cnae_id)=6 and proximity >= 0.5 and proximity < 1 order by proximity desc;
    cnaes = db.session.query(Ii.cnae_id.distinct()).all()
    cnaes = [c[0] for c in cnaes if len(c[0])==6]
    edges = []
    for c in cnaes:
        nothing = True
        cutoffs = list(frange(0.5, 0.81, 0.01))
        cutoffs.reverse()
        # for cutoff in [0.8, 0.75, 0.725, 0.7, 0.675, 0.65, 0.6, 0.55, 0.5]:
        for cutoff in cutoffs:
            conns = Ii.query.filter_by(cnae_id=c) \
                .filter(Ii.proximity >= cutoff) \
                .filter(Ii.proximity < 1) \
                .order_by(Ii.proximity.desc()).all()
            if len(conns) >= 3:
                # print c, len(conns)
                edges += conns
                nothing = False
                break
        if nothing:
            edges += [Ii.query.filter_by(cnae_id=c).filter(Ii.proximity < 1).order_by(Ii.proximity.desc()).first()]
    edges = [{"source":e.cnae_id, "target":e.cnae_id_t, "prox":e.proximity} for e in edges]
    return jsonify(data=edges)

@mod.route('cnae_space/')
def cnae_space():
    return render_template("general/cnae_space.html")

@mod.route('cnae_space/fixed/')
def cnae_space_fixed():
    return render_template("general/cnae_space_fixed.html")

@mod.route('get_colors/', methods = ['GET', 'POST'])
def get_colors():
    Attrs = {"bra":Bra, "cnae":Cnae, "cbo":Cbo, "hs":Hs, "wld":Wld, "course_hedu": Course_hedu}
    if request.method == 'POST':
        id = request.get_json().get('id', None)
        attr_type = request.get_json().get('attr_type', None)
        palette = request.get_json().get('palette', None)
        attr = Attrs[attr_type].query.get(id)
        attr.palette = palette
        db.session.commit()
        return jsonify(response={"worked":True})
    if request.is_xhr:
        bras = Bra.query.filter(Bra.image_link!=None, Bra.color!=None, Bra.palette==None).all()
        cnaes = Cnae.query.filter(Cnae.image_link!=None, Cnae.palette==None).all()
        cbos = Cbo.query.filter(Cbo.image_link!=None, Cbo.palette==None).all()
        hss = Hs.query.filter(Hs.image_link!=None, Hs.palette==None).all()
        wlds = Wld.query.filter(Wld.image_link!=None, Wld.palette==None).all()
        course_hedus = Course_hedu.query.filter(Course_hedu.image_link!=None, Course_hedu.palette==None).all()
        attrs = {
            "bra": [{"id":b.id, "image":b.image()["url"]} for b in bras],
            "cnae": [{"id":b.id, "image":b.image()["url"]} for b in cnaes],
            "cbo": [{"id":b.id, "image":b.image()["url"]} for b in cbos],
            "hs": [{"id":b.id, "image":b.image()["url"]} for b in hss],
            "wld": [{"id":b.id, "image":b.image()["url"]} for b in wlds],
            "course_hedu": [{"id":b.id, "image":b.image()["url"]} for b in course_hedus]
        }
        # attrs = {"bra": [{"id":b.id, "image":b.image()["url"]} for b in Bra.query.filter_by(id="4mg000100").all()]}
        return jsonify(attrs=attrs)
    return render_template("general/get_colors.html")


###############################
# 404 view
# ---------------------------
# @app.errorhandler(Exception)
# @mod.route('413/')
# def page_not_found(e="413"):

#     #if DEBUG:
#         #raise Exception(e)

#     error = str(e).split(":")[0]
#     try:
#         error_code = int(error)
#     except:
#         error = "500"
#         error_code = int(error)

#     request_info = {
#         "Date": datetime.today().ctime(),
#         "IP": request.remote_addr,
#         "Method": request.method,
#         "URL": request.url,
#         "Data": request.data
#     }

#     headers = list(request.headers)

#     allowed = True
#     requester = request.headers.get("from")
#     if requester:
#       if "googlebot" in requester:
#         allowed = False

#     if "fancybox" in request.url:
#       allowed = False

#     if allowed and ERROR_EMAIL and error_code != 404:
#         admins = User.query.filter(User.role == 1).filter(User.email != "").filter(User.agree_mailer == 1).all()
#         emails = [str(getattr(a,"email")) for a in admins]

#         if len(emails) > 0:
#             subject = "DataViva Error: "+error

#             if e == "413":
#                 request_info["URL"] = ''
#                 error_text = "413: Request entity too large"
#             else:
#                 error_text = str(e)

#             send_mail(subject, emails,
#                 render_template('admin/mail/error.html', title=subject,
#                 error=error_text, request_info=request_info, headers=headers))

#     g.page_type = "error"

#     sabrina = {}
#     sabrina["outfit"] = "lab"
#     sabrina["face"] = "scared"
#     sabrina["hat"] = None

#     return render_template('general/error.html',
#         error = error, sabrina = sabrina), error_code
