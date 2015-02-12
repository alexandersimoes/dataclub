from dataviva import db
from dataviva.utils.auto_serialize import AutoSerialize
from dataviva.attrs.models import Wld, Hs, Bra, Cnae
import json

class EiBaseModel(db.Model, AutoSerialize):

    __abstract__ = True
    
    '''Common indicies'''
    year = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Integer, primary_key=True)

    '''Common values'''
    tax = db.Column(db.Float())
    icms_tax = db.Column(db.Float())
    transportation_cost = db.Column(db.Float())
    purchase_value = db.Column(db.Float())
    transfer_value = db.Column(db.Float())
    devolution_value = db.Column(db.Float())
    icms_credit_value = db.Column(db.Float())
    remit_value = db.Column(db.Float())


class Ymsrp(EiBaseModel):
    __tablename__ = 'ei_ymsrp'

    bra_id_s = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    bra_id_s3 = db.Column(db.String(3))
    bra_id_s1 = db.Column(db.String(1))
    cnae_id_s1 = db.Column(db.String(1))

    bra_id_r3 = db.Column(db.String(3))
    bra_id_r1 = db.Column(db.String(1))
    cnae_id_r1 = db.Column(db.String(1))

    cnae_id_s = db.Column(db.String(3), db.ForeignKey(Cnae.id), primary_key=True)
    bra_id_r = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)

    cnae_id_r = db.Column(db.String(3), db.ForeignKey(Cnae.id), primary_key=True)
    hs_id = db.Column(db.String(6), db.ForeignKey(Hs.id), primary_key=True)
    hs_id2 = db.Column(db.String(2))


    def __repr__(self):
        return '<Ymsrp %s.%s>' % (self.year, self.month)

class Ymsr(EiBaseModel):
    __tablename__ = 'ei_ymsr'

    bra_id_s = db.Column(db.String(8), db.ForeignKey(Bra.id), primary_key=True)
    cnae_id_s = db.Column(db.String(5), db.ForeignKey(Cnae.id), primary_key=True)
    bra_id_r = db.Column(db.String(8), db.ForeignKey(Bra.id), primary_key=True)
    cnae_id_r = db.Column(db.String(5), db.ForeignKey(Cnae.id), primary_key=True)


    bra_id_s3 = db.Column(db.String(3))
    bra_id_s1 = db.Column(db.String(1))
    cnae_id_s1 = db.Column(db.String(1))

    bra_id_r3 = db.Column(db.String(3))
    bra_id_r1 = db.Column(db.String(1))
    cnae_id_r1 = db.Column(db.String(1))

    def __repr__(self):
        return '<Ymsr %s.%s>' % (self.year, self.month)


class Ymsp(EiBaseModel):
    __tablename__ = 'ei_ymsp'

    bra_id_s = db.Column(db.String(8), db.ForeignKey(Bra.id), primary_key=True)
    cnae_id_s = db.Column(db.String(5), db.ForeignKey(Cnae.id), primary_key=True)
    hs_id = db.Column(db.String(6), db.ForeignKey(Hs.id), primary_key=True)

    bra_id_s3 = db.Column(db.String(3))
    bra_id_s1 = db.Column(db.String(1))
    cnae_id_s1 = db.Column(db.String(1))
    hs_id2 = db.Column(db.String(2))

    def __repr__(self):
        return '<Ymsp %s.%s>' % (self.year, self.month)

class Ymrp(EiBaseModel):
    __tablename__ = 'ei_ymrp'

    bra_id_r = db.Column(db.String(8), db.ForeignKey(Bra.id), primary_key=True)
    cnae_id_r = db.Column(db.String(5), db.ForeignKey(Cnae.id), primary_key=True)
    hs_id = db.Column(db.String(6), db.ForeignKey(Hs.id), primary_key=True)

    bra_id_r3 = db.Column(db.String(3))
    bra_id_r1 = db.Column(db.String(1))
    cnae_id_r1 = db.Column(db.String(1))
    hs_id2 = db.Column(db.String(2))

    def __repr__(self):
        return '<Ymrp %s.%s>' % (self.year, self.month)

class Ymr(EiBaseModel):
    __tablename__ = 'ei_ymr'

    bra_id_r = db.Column(db.String(8), db.ForeignKey(Bra.id), primary_key=True)
    cnae_id_r = db.Column(db.String(5), db.ForeignKey(Cnae.id), primary_key=True)

    bra_id_r3 = db.Column(db.String(3))
    bra_id_r1 = db.Column(db.String(1))
    cnae_id_r1 = db.Column(db.String(1))

    def __repr__(self):
        return '<Ymr %s.%s>' % (self.year, self.month)

class Yms(EiBaseModel):
    __tablename__ = 'ei_yms'

    bra_id_s = db.Column(db.String(8), db.ForeignKey(Bra.id), primary_key=True)
    cnae_id_s = db.Column(db.String(5), db.ForeignKey(Cnae.id), primary_key=True)
    bra_id_s3 = db.Column(db.String(3))
    bra_id_s1 = db.Column(db.String(1))

    def __repr__(self):
        return '<Yms %s.%s>' % (self.year, self.month)

class Ymp(EiBaseModel):
    __tablename__ = 'ei_ymp'

    hs_id = db.Column(db.String(6), db.ForeignKey(Hs.id), primary_key=True)
    hs_id2 = db.Column(db.String(2))

    def __repr__(self):
        return '<Ymp_ei %s.%s>' % (self.year, self.month)
