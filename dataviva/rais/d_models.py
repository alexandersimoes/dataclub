from dataviva import db
from dataviva.attrs.models import Bra, Cbo, Cnae
from dataviva.rais.models import Rais, Rais_sans_growth

class Yiod(Rais_sans_growth):
    __tablename__ = 'rais_yiod'
    
    cnae_id = db.Column(db.String(6), db.ForeignKey(Cnae.id), primary_key=True)
    cbo_id = db.Column(db.String(4), db.ForeignKey(Cbo.id), primary_key=True)
    d_id = db.Column(db.String(1), primary_key=True)
    
    cnae_id_len = db.Column(db.Integer)
    cbo_id_len = db.Column(db.Integer)

    def __repr__(self):
        return '<Yiod %s.%s.%s.%s>' % (self.year, self.cnae_id, self.cbo_id, self.d_id)

class Ybid(Rais):
    __tablename__ = 'rais_ybid'
    
    bra_id = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    cnae_id = db.Column(db.String(6), db.ForeignKey(Cnae.id), primary_key=True)
    d_id = db.Column(db.String(1), primary_key=True)
    
    bra_id_len = db.Column(db.Integer)
    cnae_id_len = db.Column(db.Integer)

    def __repr__(self):
        return '<Ybid %s.%s.%s.%s>' % (self.year, self.bra_id, self.cnae_id, self.d_id)


class Ybod(Rais):
    __tablename__ = 'rais_ybod'
    
    bra_id = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    cbo_id = db.Column(db.String(4), db.ForeignKey(Cbo.id), primary_key=True)
    d_id = db.Column(db.String(1), primary_key=True)
    
    bra_id_len = db.Column(db.Integer)
    cbo_id_len = db.Column(db.Integer)

    def __repr__(self):
        return '<Ybod %s.%s.%s.%s>' % (self.year, self.bra_id, self.cbo_id, self.d_id)

class Yod(Rais):
    __tablename__ = 'rais_yod'
    
    cbo_id = db.Column(db.String(4), db.ForeignKey(Cbo.id), primary_key=True)
    d_id = db.Column(db.String(1), primary_key=True)
    
    '''specific ID length field'''
    cbo_id_len = db.Column(db.Integer)

    def __repr__(self):
        return '<Yod %s.%s.%s>' % (self.year, self.cbo_id, self.d_id)

class Yid(Rais):
    __tablename__ = 'rais_yid'
    
    cnae_id = db.Column(db.String(6), db.ForeignKey(Cnae.id), primary_key=True)
    d_id = db.Column(db.String(1), primary_key=True)
    
    '''specific ID length field'''
    cnae_id_len = db.Column(db.Integer)

    def __repr__(self):
        return '<Yid %s.%s.%s>' % (self.year, self.cnae_id, self.d_id)

class Ybd(Rais):
    __tablename__ = 'rais_ybd'
    
    bra_id = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    d_id = db.Column(db.String(1), primary_key=True)
    
    bra_id_len = db.Column(db.Integer)

    def __repr__(self):
        return '<Ybd %s.%s.%s>' % (self.year, self.bra_id, self.d_id)

class Ybiod(Rais_sans_growth):
    __tablename__ = 'rais_ybiod'
    
    bra_id = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    cnae_id = db.Column(db.String(6), db.ForeignKey(Cnae.id), primary_key=True)
    cbo_id = db.Column(db.String(4), db.ForeignKey(Cbo.id), primary_key=True)
    d_id = db.Column(db.String(1), primary_key=True)
    
    bra_id_len = db.Column(db.Integer)
    cnae_id_len = db.Column(db.Integer)
    cbo_id_len = db.Column(db.Integer)

    def __repr__(self):
        return '<Ybiod %s.%s.%s.%s.%s>' % (self.bra_id, self.year, self.cnae_id, self.cbo_id, self.d_id)