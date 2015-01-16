from datetime import datetime
from flask import Blueprint, render_template, g, request, current_app, session, redirect, url_for, flash, abort, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.babel import gettext
from sqlalchemy import func, or_

import time

mod = Blueprint('general', __name__, url_prefix='/')

from dataviva import app, db, babel, __latest_year__, view_cache
from dataviva.general.forms import AccessForm
from dataviva.general.models import Short
from dataviva.account.models import User

from dataviva.attrs.models import Bra, Cnae, Hs, Cbo, Wld
from dataviva.visualize.profile_models import *
from dataviva.rais.models import Yio

from dataviva.utils.cached_query import cached_query, make_cache_key

from config import ACCOUNTS, ERROR_EMAIL, DEBUG

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
    for dataset in __latest_year__:
        g.latest_year[dataset] = __latest_year__[dataset]

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
#@view_cache.cached(timeout=604800, key_prefix=make_cache_key)
def home():
    g.page_type = "home"
    lists = []

    prods = [("rj050000","052709"),("pa040304","052601"),("sp140505","178802"),("rj040102","052709"),("es000101","052601")]
    cbos = ["2542", "2514", "6311", "6128", "6127"]
    pages = [CboProfile(c) for c in cbos]
    lists.append({"title": gettext("Rarest Occupations"), "pages": pages})

    cities = ["sp090607","rj020212","ba030106","df000000","ce020003"]
    pages = [BraProfile(b) for b in cities]
    lists.append({"title": gettext("Most Populated Cities"), "pages": pages})

    prods = [("rj050000","052709"),("pa040304","052601"),("sp140505","178802"),("rj040102","052709"),("es000101","052601")]
    pages = [HsProfile(p[1],p[0]) for p in prods]
    lists.append({"title": gettext("Cities with the Largest Production"), "pages": pages})

    cities = ["sp090607", "rj020212", "to010205", "pr030109", "mg030000"]
    pages = [EduProfile(b) for b in cities]
    lists.append({"title": gettext("Largest Student Enrollment"), "pages": pages})

    return render_template("general/home.html", lists = lists)

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
@mod.route('<slug>/')
def redirect_short_url(slug):
    short = Short.query.filter_by(slug = slug).first_or_404()
    short.clicks += 1
    db.session.add(short)
    db.session.commit()

    return redirect(short.long_url)

@mod.route('workshop/view/<dataset>/')
def workshop_table_viewer(dataset):
    return render_template("general/table_viewer.html", dataset=dataset)

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
