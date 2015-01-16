from dataviva import db
from dataviva.utils.auto_serialize import AutoSerialize
from dataviva.attrs.models import Bra, Course_hedu, University, D

class Hedu(db.Model, AutoSerialize):
    __abstract__ = True
    enrolled = db.Column(db.Integer(11))
    graduates = db.Column(db.Integer(11))
    entrants = db.Column(db.Integer(11))
    students = db.Column(db.Integer(11))
    morning = db.Column(db.Integer(11))
    afternoon = db.Column(db.Integer(11))
    night = db.Column(db.Integer(11))
    full_time = db.Column(db.Integer(11))
    age = db.Column(db.Float())

    graduates_growth = db.Column(db.Float())
    enrolled_growth = db.Column(db.Float())

class Yc(Hedu):
    __tablename__ = 'hedu_yc'
    year = db.Column(db.Integer(4), primary_key=True)
    course_hedu_id = db.Column(db.Integer(2), db.ForeignKey(Course_hedu.id), primary_key=True)

    course_hedu_id_len = db.Column(db.Integer(1))

    def __repr__(self):
        return '<Ybc {}.{}.{}>'.format(self.year, self.bra_id, self.course_hedu_id)

class Ybc(Hedu):
    __tablename__ = 'hedu_ybc'
    year = db.Column(db.Integer(4), primary_key=True)
    bra_id = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    course_hedu_id = db.Column(db.Integer(2), db.ForeignKey(Course_hedu.id), primary_key=True)

    bra_id_len = db.Column(db.Integer(1))
    course_hedu_id_len = db.Column(db.Integer(1))

    def __repr__(self):
        return '<Ybc {}.{}.{}>'.format(self.year, self.bra_id, self.course_hedu_id)

class Ybuc(Hedu):
    __tablename__ = 'hedu_ybuc'
    year = db.Column(db.Integer(4), primary_key=True)
    bra_id = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    university_id = db.Column(db.String(5), db.ForeignKey(University.id), primary_key=True)
    course_hedu_id = db.Column(db.Integer(2), db.ForeignKey(Course_hedu.id), primary_key=True)

    enrolled_rca = db.Column(db.Float())

    bra_id_len = db.Column(db.Integer(1))
    course_hedu_id_len = db.Column(db.Integer(1))

    def __repr__(self):
        return '<Ybuc {}.{}.{}.{}>'.format(self.year, self.bra_id, self.university_id, self.course_hedu_id)

class Ybud(Hedu):
    __tablename__ = 'hedu_ybud'
    year = db.Column(db.Integer(4), primary_key=True)
    bra_id = db.Column(db.String(8), db.ForeignKey(Bra.id), primary_key=True)
    university_id = db.Column(db.Integer(2), db.ForeignKey(University.id), primary_key=True)
    d_id = db.Column(db.String(1), primary_key=True)

    bra_id_len = db.Column(db.Integer(1))
    
    def __repr__(self):
        return '<Ybud {}.{}.{}.{}>'.format(self.year, self.bra_id, self.university_id, self.d_id)

class Ybcd(Hedu):
    __tablename__ = 'hedu_ybcd'
    year = db.Column(db.Integer(4), primary_key=True)
    bra_id = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    course_hedu_id = db.Column(db.Integer(2), db.ForeignKey(Course_hedu.id), primary_key=True)
    d_id = db.Column(db.String(1), primary_key=True)

    bra_id_len = db.Column(db.Integer(1))
    course_hedu_id_len = db.Column(db.Integer(1))

    def __repr__(self):
        return '<Ybcd {}.{}.{}.{}>'.format(self.year, self.bra_id, self.course_hedu_id, self.d_id)

class Yd(Hedu):

    __tablename__ = 'hedu_yd'

    year = db.Column(db.Integer(4), primary_key=True)
    d_id = db.Column(db.String(1), db.ForeignKey(D.id), primary_key=True)

    def __repr__(self):
        return '<Yd {}.{}>'.format(self.year, self.d_id)

class Ybd(Hedu):

    __tablename__ = 'hedu_ybd'

    year = db.Column(db.Integer(4), primary_key=True)
    bra_id = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    d_id = db.Column(db.String(1), primary_key=True)

    bra_id_len = db.Column(db.Integer(1))

    def __repr__(self):
        return '<Ybd {}.{}.{}>'.format(self.year, self.bra_id, self.d_id)

class Yb_hedu(Hedu):

    __tablename__ = 'hedu_yb'

    year = db.Column(db.Integer(4), primary_key=True)
    bra_id = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    num_universities = db.Column(db.Integer(11))

    bra_id_len = db.Column(db.Integer(1))

    def __repr__(self):
        return '<Yb {}.{}>'.format(self.year, self.bra_id)

class Ybu(Hedu):

    __tablename__ = 'hedu_ybu'

    year = db.Column(db.Integer(4), primary_key=True)
    bra_id = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    university_id = db.Column(db.String(5), db.ForeignKey(University.id), primary_key=True)

    bra_id_len = db.Column(db.Integer(1))

    def __repr__(self):
        return '<Ybu {}.{}.{}>'.format(self.year, self.bra_id, self.university_id)

class Yu(Hedu):

    __tablename__ = 'hedu_yu'

    year = db.Column(db.Integer(4), primary_key=True)
    university_id = db.Column(db.String(5), db.ForeignKey(University.id), primary_key=True)

    def __repr__(self):
        return '<Yu {}.{}>'.format(self.year, self.university_id)

class Yuc(Hedu):

    __tablename__ = 'hedu_yuc'

    year = db.Column(db.Integer(4), primary_key=True)
    university_id = db.Column(db.String(5), db.ForeignKey(University.id), primary_key=True)
    course_hedu_id = db.Column(db.Integer(2), db.ForeignKey(Course_hedu.id), primary_key=True)
    enrolled_rca = db.Column(db.Float())

    course_hedu_id_len = db.Column(db.Integer(1))

    def __repr__(self):
        return '<Yuc {}.{}.{}>'.format(self.year, self.university_id, self.course_hedu_id)

class Ycd(Hedu):
    __tablename__ = 'hedu_ycd'
    year = db.Column(db.Integer(4), primary_key=True)
    course_hedu_id = db.Column(db.Integer(2), db.ForeignKey(Course_hedu.id), primary_key=True)
    d_id = db.Column(db.String(1), primary_key=True)

    course_hedu_id_len = db.Column(db.Integer(1))

    def __repr__(self):
        return '<Ycd {}.{}.{}>'.format(self.year, self.course_hedu_id, self.d_id)

class Yud(Hedu):

    __tablename__ = 'hedu_yud'

    year = db.Column(db.Integer(4), primary_key=True)
    university_id = db.Column(db.String(5), db.ForeignKey(University.id), primary_key=True)
    d_id = db.Column(db.String(1), primary_key=True)

    def __repr__(self):
        return '<Yud {}.{}.{}>'.format(self.year, self.university_id, self.d_id)

class Yucd(Hedu):

    __tablename__ = 'hedu_yucd'

    year = db.Column(db.Integer(4), primary_key=True)
    university_id = db.Column(db.String(5), db.ForeignKey(University.id), primary_key=True)
    course_hedu_id = db.Column(db.Integer(2), db.ForeignKey(Course_hedu.id), primary_key=True)
    d_id = db.Column(db.String(1), primary_key=True)

    course_hedu_id_len = db.Column(db.Integer(1))

    def __repr__(self):
        return '<Yucd {}.{}.{}.{}>'.format(self.year, self.university_id, self.course_hedu_id, self.d_id)

class Ybucd(Hedu):
    __tablename__ = 'hedu_ybucd'
    year = db.Column(db.Integer(4), primary_key=True)
    bra_id = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    university_id = db.Column(db.String(5), db.ForeignKey(University.id), primary_key=True)
    course_hedu_id = db.Column(db.Integer(2), db.ForeignKey(Course_hedu.id), primary_key=True)
    d_id = db.Column(db.String(1), primary_key=True)

    bra_id_len = db.Column(db.Integer(1))
    course_hedu_id_len = db.Column(db.Integer(1))

    def __repr__(self):
        return '<Ybucd {}.{}.{}.{}.{}>'.format(self.year, self.bra_id, self.university_id, self.course_hedu_id, self.d_id)