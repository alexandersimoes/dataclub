from dataviva import db
from dataviva.utils.auto_serialize import AutoSerialize
from dataviva.attrs.models import Bra

class Sc(db.Model, AutoSerialize):
    __abstract__ = True

    year = db.Column(db.Integer, primary_key=True)    
    age = db.Column(db.Float())
    classes = db.Column(db.Integer)
    enrolled = db.Column(db.Integer)
    enrolled_growth = db.Column(db.Float())

class Ybd(Sc):
    __tablename__ = 'sc_ybd'

    bra_id = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    d_id = db.Column(db.String(1), primary_key=True)
    
    def __repr__(self):
        return '<Ybd %d.%s.%s>' % (self.year, self.bra_id, self.d_id)

class Yb(Sc):
    __tablename__ = 'sc_yb'

    bra_id = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    bra_id_len = db.Column(db.Integer)
    num_schools = db.Column(db.Integer)
    
    def __repr__(self):
        return '<Yb {0}.{1}>'.format(self.year, self.bra_id)

class Yd(Sc):
    __tablename__ = 'sc_yd'
    
    d_id = db.Column(db.String(1), primary_key=True)
    
    def __repr__(self):
        return '<Yd %d.%s.%s>' % (self.year, self.d_id)

class Ys(Sc):

    __tablename__ = 'sc_ys'
    
    school_id = db.Column(db.String(8), primary_key=True)

    def __repr__(self):
        return '<Ys %d.%s.%s>' % (self.year, self.school_id)

class Ybs(Sc):

    __tablename__ = 'sc_ybs'
    
    bra_id = db.Column(db.String(9), primary_key=True)
    school_id = db.Column(db.String(8), primary_key=True)

    def __repr__(self):
        return '<Ybs %d.%s.%s>' % (self.year, self.bra_id, self.school_id)

class Ybc(Sc):
    __tablename__ = 'sc_ybc'

    bra_id = db.Column(db.String(9), primary_key=True)
    course_sc_id = db.Column(db.String(5), primary_key=True)
    
    bra_id_len = db.Column(db.Integer)
    course_sc_id_len = db.Column(db.Integer)

    def __repr__(self):
        return '<Ybc %d.%s.%s>' % (self.year, self.bra_id, self.course_sc_id)

class Yc(Sc):
    __tablename__ = 'sc_yc'

    course_sc_id = db.Column(db.String(5), primary_key=True)
    course_sc_id_len = db.Column(db.Integer)

    def __repr__(self):
        return '<Ybc %d.%s.%s>' % (self.year, self.course_sc_id)

class Ybcd(Sc):
    __tablename__ = 'sc_ybcd'

    bra_id = db.Column(db.String(9), primary_key=True)
    course_sc_id = db.Column(db.String(5), primary_key=True)
    d_id = db.Column(db.String(1), primary_key=True)
    
    bra_id_len = db.Column(db.Integer)
    course_sc_id_len = db.Column(db.Integer)

    def __repr__(self):
        return '<Ybcd %d.%s.%s.%s>' % (self.year, self.bra_id, self.course_sc_id, self.d_id)