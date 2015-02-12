from dataviva import db
from dataviva.utils.auto_serialize import AutoSerialize
from dataviva.attrs.models import Bra, Cnae, Cbo

class Rais(db.Model, AutoSerialize):

    __abstract__ = True
    
    '''Common indicies'''
    year = db.Column(db.Integer, primary_key=True)
    
    '''Common values'''
    wage = db.Column(db.Numeric(16,2))
    num_emp = db.Column(db.Integer)
    num_jobs = db.Column(db.Integer)
    num_est = db.Column(db.Integer)
    wage_avg = db.Column(db.Numeric(16,2))
    age_avg = db.Column(db.Integer)
    '''Common growth cols'''
    wage_growth = db.Column(db.Float())
    wage_growth_5 = db.Column(db.Float())
    num_emp_growth = db.Column(db.Float())
    num_emp_growth_5 = db.Column(db.Float())

class Rais_sans_growth(db.Model, AutoSerialize):

    __abstract__ = True
    
    '''Common indicies'''
    year = db.Column(db.Integer, primary_key=True)
    
    '''Common values'''
    wage = db.Column(db.Numeric(16,2))
    num_emp = db.Column(db.Integer)
    num_jobs = db.Column(db.Integer)
    num_est = db.Column(db.Integer)
    wage_avg = db.Column(db.Numeric(16,2))
    age_avg = db.Column(db.Integer)

class Ii(db.Model):

    __tablename__ = 'rais_ii'
    cnae_id = db.Column(db.String(6), db.ForeignKey(Cnae.id), primary_key=True)
    cnae_id_t = db.Column(db.String(6), db.ForeignKey(Cnae.id), primary_key=True)
    proximity = db.Column(db.Float())

    def __repr__(self):
        return '<Ii %r-%r:%g>' % (self.cnae_id, self.cnae_id_t, self.proximity)

class Oo(db.Model):

    __tablename__ = 'rais_oo'
    cbo_id = db.Column(db.String(4), db.ForeignKey(Cbo.id), primary_key=True)
    cbo_id_t = db.Column(db.String(4), db.ForeignKey(Cbo.id), primary_key=True)
    proximity = db.Column(db.Float())

    def __repr__(self):
        return '<Oo %r-%r:%g>' % (self.cbo_id, self.cbo_id_t, self.proximity)

class Yi(Rais):

    __tablename__ = 'rais_yi'
    
    '''specific index'''
    cnae_id = db.Column(db.String(6), db.ForeignKey(Cnae.id), primary_key=True)
    
    '''specific ID length field'''
    cnae_id_len = db.Column(db.Integer)
    
    '''specific values'''
    bra_diversity = db.Column(db.Integer)
    bra_diversity_eff = db.Column(db.Float())
    cbo_diversity = db.Column(db.Integer)
    cbo_diversity_eff = db.Column(db.Float())

    def __repr__(self):
        return '<Yi %d.%s>' % (self.year, self.cnae_id)

class Yb(Rais):

    __tablename__ = 'rais_yb'
    
    '''specific index'''
    bra_id = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)

    '''specific ID length field'''
    bra_id_len = db.Column(db.Integer)

    '''specific values'''
    cnae_diversity = db.Column(db.Integer)
    cnae_diversity_eff = db.Column(db.Float())
    cbo_diversity = db.Column(db.Integer)
    cbo_diversity_eff = db.Column(db.Float())

    def __repr__(self):
        return '<Yb %d.%s>' % (self.year, self.bra_id)

class Yo(Rais):

    __tablename__ = 'rais_yo'

    '''specific index'''
    cbo_id = db.Column(db.String(6), db.ForeignKey(Cbo.id), primary_key=True)

    '''specific ID length field'''
    cbo_id_len = db.Column(db.Integer)

    '''specific values'''
    bra_diversity = db.Column(db.Integer)
    bra_diversity_eff = db.Column(db.Float())
    cnae_diversity = db.Column(db.Integer)
    cnae_diversity_eff = db.Column(db.Float())
    
    def __repr__(self):
        return '<Yo %d.%s>' % (self.year, self.cbo_id)
        
############################################################
# ----------------------------------------------------------
# 3 variable tables
# 
############################################################

class Ybi_Lg(Rais):
    
    __tablename__ = 'rais_ybi_lg'

    '''specific index'''
    bra_id = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    cnae_id = db.Column(db.String(6), db.ForeignKey(Cnae.id), primary_key=True)
    
    '''specific ID length field'''
    bra_id_len = db.Column(db.Integer)
    cnae_id_len = db.Column(db.Integer)
    
    '''specific values'''
    rca = db.Column(db.Float())
    distance = db.Column(db.Float())
    opp_gain = db.Column(db.Float())
    
    def __repr__(self):
        return '<Ybi Large %d.%s.%s>' % (self.year, self.bra_id, self.cnae_id)

class Ybi(Rais):
    
    __tablename__ = 'rais_ybi'

    '''specific index'''
    bra_id = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    cnae_id = db.Column(db.String(6), db.ForeignKey(Cnae.id), primary_key=True)
    
    '''specific ID length field'''
    bra_id_len = db.Column(db.Integer)
    cnae_id_len = db.Column(db.Integer)
    
    '''specific values'''
    rca = db.Column(db.Float())
    distance = db.Column(db.Float())
    opp_gain = db.Column(db.Float())
    
    def __repr__(self):
        return '<Ybi %d.%s.%s>' % (self.year, self.bra_id, self.cnae_id)

class Ybo(Rais):
    
    __tablename__ = 'rais_ybo'

    '''specific index'''
    bra_id = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    cbo_id = db.Column(db.String(6), db.ForeignKey(Cbo.id), primary_key=True)

    '''specific ID length field'''
    bra_id_len = db.Column(db.Integer)
    cbo_id_len = db.Column(db.Integer)
    
    def __repr__(self):
        return '<Ybo %d.%s.%s>' % (self.year, self.bra_id, self.cbo_id)
    
class Yio(Rais):
    
    __tablename__ = 'rais_yio'
    
    '''specific index'''
    cnae_id = db.Column(db.String(6), db.ForeignKey(Cnae.id), primary_key=True)
    cbo_id = db.Column(db.String(6), db.ForeignKey(Cbo.id), primary_key=True)
    
    '''specific ID length field'''
    cnae_id_len = db.Column(db.Integer)
    cbo_id_len = db.Column(db.Integer)

    '''specific YIO fields'''
    importance = db.Column(db.Float())
    mne_micro = db.Column(db.Float())
    mne_small = db.Column(db.Float())
    mne_medium = db.Column(db.Float())
    mne_large = db.Column(db.Float())
    
    def __repr__(self):
        return '<Yio %d.%s.%s>' % (self.year, self.cnae_id, self.cbo_id)

class Ybio(Rais):
    
    __tablename__ = 'rais_ybio'

    '''specific index'''
    bra_id = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    cnae_id = db.Column(db.String(6), db.ForeignKey(Cnae.id), primary_key=True)
    cbo_id = db.Column(db.String(6), db.ForeignKey(Cbo.id), primary_key=True)

    '''specific ID length field'''
    bra_id_len = db.Column(db.Integer)
    cnae_id_len = db.Column(db.Integer)
    cbo_id_len = db.Column(db.Integer)
    
    '''specific YBIO fields'''
    mne_micro = db.Column(db.Float())
    mne_small = db.Column(db.Float())
    mne_medium = db.Column(db.Float())
    mne_large = db.Column(db.Float())
    
    def __repr__(self):
        return '<Ybio %d.%s.%s.%s>' % (self.year, self.bra_id, self.cnae_id, self.cbo_id)
