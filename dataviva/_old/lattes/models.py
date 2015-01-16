from dataviva import db
from dataviva.utils.auto_serialize import AutoSerialize
from dataviva.attrs.models import Bra

############################################################
# ----------------------------------------------------------
# People
#
############################################################

class Bri(db.Model, AutoSerialize):

    __tablename__ = 'lattes_bri'
    bra_id = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    research_id = db.Column(db.String(8), db.ForeignKey(Research.id), primary_key=True)
    inst_id = db.Column(db.Integer(11), db.ForeignKey(Institution.id), primary_key=True)
    people = db.Column(db.Integer(11))

    def __repr__(self):
        return '<Bri %s.%s.%d>' % (self.bra_id, self.research_id, self.inst_id)

############################################################
# ----------------------------------------------------------
# Papers
#
############################################################

class Ybr(db.Model, AutoSerialize):

    __tablename__ = 'lattes_ybr'
    year = db.Column(db.Integer(4), primary_key=True)
    bra_id = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    research_id = db.Column(db.String(8), db.ForeignKey(Research.id), primary_key=True)
    papers_rca = db.Column(db.Float())

    def __repr__(self):
        return '<Ybr %d.%s.%s>' % (self.year, self.bra_id, self.research_id)

class Ybri(db.Model, AutoSerialize):

    __tablename__ = 'lattes_ybri'
    year = db.Column(db.Integer(4), primary_key=True)
    bra_id = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    research_id = db.Column(db.String(8), db.ForeignKey(Research.id), primary_key=True)
    inst_id = db.Column(db.Integer(11), db.ForeignKey(Institution.id), primary_key=True)
    papers = db.Column(db.Integer(11))

    def __repr__(self):
        return '<Ybri %d.%s.%s.%d>' % (self.year, self.bra_id, self.research_id, self.inst_id)
