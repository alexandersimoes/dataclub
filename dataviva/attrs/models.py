from flask.ext.babel import gettext
from dataviva import db
from dataviva.attrs.article import get_article
from dataviva.utils.auto_serialize import AutoSerialize
from dataviva.utils.exist_or_404 import exist_or_404
from dataviva.utils.title_case import title_case
from sqlalchemy import func, Float, desc
from sqlalchemy.sql.expression import cast
from decimal import *

from flask import g

class Attrs(db.Model, AutoSerialize):

    __abstract__ = True

    id = db.Column(db.String(10), primary_key=True)
    name_en = db.Column(db.String(200))
    name_pt = db.Column(db.String(200))
    color = db.Column(db.String(7))
    gender_pt = db.Column(db.String(1))
    plural_pt = db.Column(db.Boolean())
    article_pt = db.Column(db.Boolean())

    image_link = db.Column(db.String(200))
    image_author = db.Column(db.String(200))

    def name(self, lang=None, article=False):
        lang = lang or getattr(g, "locale", "en")
        text = title_case(getattr(self,"name_"+lang))
        if article:
            word = get_article(self, article)
            if word:
                text = "{0} {1}".format(word, text)
        return text

    def attr(self):
        return self.__class__.__name__.lower()

    def display_id(self):
        return self.id.upper()

    def icon(self):
        t = self.attr()
        if t == "university":
            return None
        return "/static/img/icons/{0}/{0}_{1}.png".format(t, self.id[:self.depths[0]])

    def image(self):

        link = False
        cat = self.attr()
        depths = self.depths[:self.depths.index(len(self.id)) + 1]

        while len(depths) > 0:

            depth = depths.pop()

            if depth == len(self.id):
                attr = self
            else:
                attr = self.__class__.query.get(self.id[:depth])

            if attr.image_link:
                url = "/static/img/profiles/{}/{}.jpg".format(cat, attr.id)
                link = attr.image_link
                author = attr.image_author
                break

        if link:
            return {"url": url, "link": link, "author": author}
        else:
            return None

    def get_palette(self):

        if not hasattr(self, "palette"):
            return []

        palette = False
        cat = self.attr()
        depths = self.depths[:self.depths.index(len(self.id)) + 1]

        while len(depths) > 0:

            depth = depths.pop()

            if depth == len(self.id):
                attr = self
            else:
                attr = self.__class__.query.get(self.id[:depth])

            if attr.palette:
                palette = attr.palette
                break

        return palette

    def url(self, attr=None, attr_type=None):
        if attr:
            filter_type = None
            if isinstance(attr, Bra) or attr_type == "bra":
                attr_id     = attr.id if isinstance(attr, Bra) else attr
                filter_type = self.attr()
                filter_id   = self.id
            elif isinstance(self, Bra):
                attr_id = self.id
                if attr_type or not isinstance(attr, (unicode, str)):
                    filter_type = attr_type if attr_type else attr.attr()
                filter_id = attr if isinstance(attr, (unicode, str)) else attr.id

            if filter_type:
                return "/profile/bra/{}/{}/{}/".format(attr_id, filter_type, filter_id)
        return "/profile/{}/{}/".format(self.attr(), self.id)

    def __repr__(self):
        return u"<{0} {1!r}>".format(self.__class__.__name__, self.name())

    def serialize(self, lang=None):
        return {
            "id": self.id,
            "color": self.color,
            "name": self.name(lang),
            "icon": self.icon(),
            "gender": self.gender_pt,
            "plural": self.plural_pt,
            "article": self.article_pt,
            "url": self.url()
        }

class Classification(Attrs):

    __abstract__ = True

    desc_en = db.Column(db.Text())
    desc_pt = db.Column(db.Text())
    keywords_en = db.Column(db.String(100))
    keywords_pt = db.Column(db.String(100))

############################################################
# ----------------------------------------------------------
# Employment Attrs (RAIS)
#
############################################################
class Cnae(Classification):

    __tablename__ = 'attrs_cnae'

    depths = [1,3,6]

    # profile colors
    palette = db.Column(db.String(200))

    yi = db.relationship("Yi", backref = 'cnae', lazy = 'dynamic')
    ybi = db.relationship("Ybi", backref = 'cnae', lazy = 'dynamic')
    yio = db.relationship("Yio", backref = 'cnae', lazy = 'dynamic')
    ybio = db.relationship("Ybio", backref = 'cnae', lazy = 'dynamic')

    # similar industries
    similar = db.relationship('Ii', primaryjoin = "(Cnae.id == Ii.cnae_id)", lazy='dynamic')
    prox = db.relationship('Ii', primaryjoin = "(Cnae.id == Ii.cnae_id_t)", backref = 'cnae', uselist=False)

    def get_similar(self, n=5, remove_self=True):
        if remove_self: n+=1
        q = self.similar.order_by(desc("proximity")).limit(n)
        if remove_self: return q.all()[1:]
        return q.all()

class Cbo(Classification):

    __tablename__ = 'attrs_cbo'

    depths = [1,4]

    # profile colors
    palette = db.Column(db.String(200))

    yo = db.relationship("Yo", backref = 'cbo', lazy = 'dynamic')
    ybo = db.relationship("Ybo", backref = 'cbo', lazy = 'dynamic')
    yio = db.relationship("Yio", backref = 'cbo', lazy = 'dynamic')
    ybio = db.relationship("Ybio", backref = 'cbo', lazy = 'dynamic')

    # similar occupations
    similar = db.relationship('Oo', primaryjoin = "(Cbo.id == Oo.cbo_id)", lazy='dynamic')
    prox = db.relationship("Oo", primaryjoin = "(Cbo.id == Oo.cbo_id_t)", backref = 'cbo', uselist=False)

    def get_similar(self, n=5, remove_self=True):
        if remove_self: n+=1
        q = self.similar.order_by(desc("proximity")).limit(n)
        if remove_self: return q.all()[1:]
        return q.all()

############################################################
# ----------------------------------------------------------
# Product Attrs (SECEX)
#
############################################################
class Hs(Classification):

    __tablename__ = 'attrs_hs'

    depths = [2,4,6]

    # profile colors
    palette = db.Column(db.String(200))

    # ymp = db.relationship("Ymp", backref = 'hs', lazy = 'dynamic')
    ympw = db.relationship("Ympw", backref = 'hs', lazy = 'dynamic')
    ymbp = db.relationship("Ymbp", backref = 'hs', lazy = 'dynamic')
    ymbpw = db.relationship("Ymbpw", backref = 'hs', lazy = 'dynamic')

    # similar occupations
    similar = db.relationship('Pp', primaryjoin = "(Hs.id == Pp.hs_id)", lazy='dynamic')
    prox = db.relationship('Pp', primaryjoin = "(Hs.id == Pp.hs_id_t)", backref = 'hs', uselist=False)

    def get_similar(self, n=5, remove_self=True):
        if remove_self: n+=1
        q = self.similar.order_by(desc("proximity")).limit(n)
        if remove_self: return q.all()[1:]
        return q.all()

    def display_id(self):
        if len(self.id) == 2:
            roman_lookup = {1:'I', 2:'II', 3:'III', 4:'IV', 5:'V',
                            6:'VI', 7:'VII', 8:'VIII', 9:'IX', 10:'X',
                            11:'XI', 12:'XII', 13:'XIII', 14:'XIV', 15:'XV',
                            16:'XVI', 17:'XVII', 18:'XVIII', 19:'XIX', 20:'XX',
                            21:'XXI', 22:'XXII', 23:'XXIII', 24:'XXIV', 25:'XXV'}
            return roman_lookup[int(self.id)]
        return self.id[2:]

############################################################
# ----------------------------------------------------------
# School Census Attrs (SC)
#
############################################################
class Grade(Attrs):

    __tablename__ = 'attrs_grade'
    depths = [2]

class Course_sc(Classification):

    __tablename__ = 'attrs_course_sc'
    depths = [2,5]

class School(Classification):

    __tablename__ = 'attrs_school'
    depths = [8]

############################################################
# ----------------------------------------------------------
# Higher Education Attrs (hedu)
#
############################################################
class Course_hedu(Classification):

    __tablename__ = 'attrs_course_hedu'
    depths = [2,6]

    # profile colors
    palette = db.Column(db.String(200))

    yc = db.relationship("hedu.models.Yc", backref = 'course_hedu', lazy = 'dynamic')
    ybc = db.relationship("hedu.models.Ybc", backref = 'course_hedu', lazy = 'dynamic')
    yuc = db.relationship("hedu.models.Yuc", backref = 'course_hedu', lazy = 'dynamic')
    yucd = db.relationship("hedu.models.Yucd", backref = 'course_hedu', lazy = 'dynamic')

############################################################
# ----------------------------------------------------------
# Geography
#
############################################################
class Wld(Attrs):

    __tablename__ = 'attrs_wld'

    depths = [2,5]

    # profile colors
    palette = db.Column(db.String(200))

    id_2char = db.Column(db.String(2))
    id_3char = db.Column(db.String(3))
    id_num = db.Column(db.Integer)
    id_mdic = db.Column(db.Integer)

    ymw = db.relationship("Ymw", backref = 'wld', lazy = 'dynamic')
    ympw = db.relationship("Ympw", backref = 'wld', lazy = 'dynamic')
    ymbw = db.relationship("Ymbw", backref = 'wld', lazy = 'dynamic')
    ymbpw = db.relationship("Ymbpw", backref = 'wld', lazy = 'dynamic')

    stats = db.relationship("Wld_stats", backref = 'wld', uselist=False)

    def display_id(self):
        if len(self.id) == 5:
            return self.id[2:].upper()
        return self.id.upper()

    def icon(self):
        return "/static/img/icons/wld/wld_{0}.png".format(self.id)

class Wld_stats(db.Model, AutoSerialize):

    __tablename__ = 'attrs_wld_stats'

    wld_id = db.Column(db.String(5), db.ForeignKey(Wld.id), primary_key=True)
    demonym = db.Column(db.String(100))
    gdp = db.Column(db.Numeric(16,2))
    gdp_per_capita = db.Column(db.Numeric(14,2))
    area = db.Column(db.Float())
    pop = db.Column(db.Integer)
    pop_density = db.Column(db.Integer)
    neighbors = db.Column(db.String(255))
    capital = db.Column(db.String(255))
    gini = db.Column(db.Numeric(3,1))
    subregion = db.Column(db.String(50))
    inet_users = db.Column(db.Numeric(3,1))
    export_val = db.Column(db.Numeric(16,2))
    import_val = db.Column(db.Numeric(16,2))

    def __repr__(self):
        return '<Wld_stat %r>' % (self.wld_id)

# bra_pr = db.Table('attrs_bra_pr',
#     db.Column('bra_id', db.Integer, db.ForeignKey('attrs_bra.id')),
#     db.Column('pr_id', db.Integer, db.ForeignKey('attrs_bra.id'))
# )

class Bra(Attrs):

    __tablename__ = 'attrs_bra'

    id_ibge = db.Column(db.Integer)

    depths = [1,3,5,7,9]

    distance = 0

    # profile colors
    palette = db.Column(db.String(200))

    # SECEX relations
    Ymb = db.relationship("Ymb", backref = 'bra', lazy = 'dynamic')
    ymbp = db.relationship("Ymbp", backref = 'bra', lazy = 'dynamic')
    ymbw = db.relationship("Ymbw", backref = 'bra', lazy = 'dynamic')
    ymbpw = db.relationship("Ymbpw", backref = 'bra', lazy = 'dynamic')
    # RAIS relations
    yb = db.relationship("rais.models.Yb", backref = 'bra', lazy = 'dynamic')
    ybi = db.relationship("Ybi", backref = 'bra', lazy = 'dynamic')
    ybo = db.relationship("Ybo", backref = 'bra', lazy = 'dynamic')
    ybio = db.relationship("Ybio", backref = 'bra', lazy = 'dynamic')
    # Neighbors
    neighbors = db.relationship('Distances', primaryjoin = "(Bra.id == Distances.bra_id_origin)", backref='bra_origin', lazy='dynamic')
    bb = db.relationship('Distances', primaryjoin = "(Bra.id == Distances.bra_id_dest)", backref='bra', lazy='dynamic')
    # Planning Regions
    # pr = db.relationship('Bra',
    #         secondary = bra_pr,
    #         primaryjoin = (bra_pr.c.pr_id == id),
    #         secondaryjoin = (bra_pr.c.bra_id == id),
    #         backref = db.backref('bra', lazy = 'dynamic'),
    #         lazy = 'dynamic')

    stats = db.relationship("Bra_stats", foreign_keys='Bra_stats.bra_id', backref = 'bra', uselist=False)

    def display_id(self):
        return str(self.id_ibge)

    def get_neighbors(self, dist, remove_self=False):
        q = self.neighbors.filter(Distances.distance <= dist).order_by(Distances.distance)
        if remove_self:
            q = q.filter(Distances.bra_id_dest != self.id) # filter out self
        return q.all()

    def get_neighbors_pop_sum(self, dist):
        q = Distances.query.filter(self.id != Distances.bra_id_dest,
                                   self.id == Distances.bra_id_origin, Distances.distance <= dist )
        results = q.all()
        ids = [x.bra_id_dest for x in results]
        stat = Bra_stats.query.filter(Bra_stats.bra_id.in_(ids)).all()
        stat, = Bra_stats.query.with_entities(func.sum(Bra_stats.pop)).filter(Bra_stats.bra_id.in_(ids)).all()
        return stat[0]

    def capital(self):
        return self.stats.capital_dist == 0

    def icon(self):
        return "/static/img/icons/bra/bra_{0}.png".format(self.id[:3])

class Bra_stats(db.Model, AutoSerialize):

    __tablename__ = 'attrs_bra_stats'
    bra_id = db.Column(db.String(10), db.ForeignKey(Bra.id), primary_key=True)
    demonym = db.Column(db.String(100))
    climate = db.Column(db.String(100))
    elevation = db.Column(db.Integer)
    gdp = db.Column(db.Numeric(14,2))
    gdp_per_capita = db.Column(db.Numeric(14,2))
    area = db.Column(db.Float())
    pop = db.Column(db.Integer)
    pop_density = db.Column(db.Integer)
    pop_active = db.Column(db.Integer)
    pop_eligible = db.Column(db.Integer)
    pop_employed = db.Column(db.Integer)
    neighbors = db.Column(db.String(255))
    airport_dist = db.Column(db.Float())
    airport_name = db.Column(db.String(255))
    seaport_dist = db.Column(db.Float())
    seaport_name = db.Column(db.String(255))
    capital_dist = db.Column(db.Float())
    capital_id = db.Column(db.String(10), db.ForeignKey(Bra.id))
    hdi = db.Column(db.Numeric(3,3))
    hdi_edu = db.Column(db.Numeric(3,3))
    hdi_health = db.Column(db.Numeric(3,3))
    hdi_income = db.Column(db.Numeric(3,3))

    capital = db.relationship("Bra", primaryjoin = "(Bra.id == Bra_stats.capital_id)")

    def __repr__(self):
        return '<Bra_stat {0}>'.format(self.bra_id)

class Distances(db.Model):

    __tablename__ = 'attrs_bb'
    bra_id_origin = db.Column(db.String(10), db.ForeignKey(Bra.id), primary_key=True)
    bra_id_dest = db.Column(db.String(10), db.ForeignKey(Bra.id), primary_key=True)
    distance = db.Column(db.Float())

    def __repr__(self):
        return '<Bra_Dist {0}-{1}:{2}>'.format(self.bra_id_origin, self.bra_id_dest, self.distance)

    def serialize(self):
        return {
            "bra_id_origin": self.bra_id_origin,
            "bra_id_dest": self.bra_id_dest,
            "distance": self.distance
        }


class D(Attrs):
    ''' Demographic ID table '''
    __tablename__ = 'attrs_d'
    depths = [1]

    name_noun_en = db.Column(db.String(200))
    name_noun_pt = db.Column(db.String(200))
    category = db.Column(db.String(20))

    # HEDU relations
    Yd = db.relationship("hedu.models.Yd", backref = 'd', lazy = 'dynamic')
    University = db.relationship("attrs.models.University", backref = 'school_type', lazy = 'dynamic')

    def name(self, lang=None, article=False, adjective=True, noun=False):
        lang = lang or getattr(g, "locale", "en")
        if noun:
            text = title_case(getattr(self,"name_noun_"+lang))
        else:
            text = title_case(getattr(self,"name_"+lang))
        if article:
            word = get_article(self, article)
            if word:
                text = "{0} {1}".format(word, text)
        return text

    def icon(self):
        if self.category == "gender":
            return "/static/img/icons/d/d_{0}.png".format(self.id)
        elif self.category == "ethnicity":
            return "/static/img/icons/d/d_ethnicity.png"
        else:
            return None

    def __repr__(self):
        return '<Demographic attribute ({0}, {1})>'.format(self.name_en, self.category)

    def serialize(self, lang=None):
        results = super(D, self).serialize(lang)
        results["category"] = self.category
        return results


class University(Classification):

    __tablename__ = 'attrs_university'
    depths = [5]

    yu = db.relationship("hedu.models.Yu", backref = 'university', lazy = 'dynamic')
    ybu = db.relationship("hedu.models.Ybu", backref = 'university', lazy = 'dynamic')
    yuc = db.relationship("hedu.models.Yuc", backref = 'university', lazy = 'dynamic')
    yucd = db.relationship("hedu.models.Yucd", backref = 'university', lazy = 'dynamic')

    bras = db.relationship('hedu.models.Ybu', primaryjoin = "(University.id == Ybu.university_id)", lazy='dynamic')

    school_type_id = db.Column(db.String(1), db.ForeignKey(D.id))

    def get_locations(self, n=1):
        q = self.bras.order_by(desc("enrolled")).filter("bra_id_len = 9").filter("bra_id != '0xx000007'").filter("year = 2012").limit(n).all()
        if len(q) == 0:
            q = [Bra.query.get("0xx000007")]
        else:
            q = [Bra.query.get(b.bra_id) for b in q]
        return q

    # def icon(self):
    #     b = self.get_locations()[0]
    #     return b.icon()
