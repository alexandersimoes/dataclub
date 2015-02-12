from dataviva import db
from dataviva.utils.auto_serialize import AutoSerialize
from dataviva.attrs.models import Wld, Hs, Bra

class Secex(db.Model, AutoSerialize):

    __abstract__ = True
    
    '''Common indicies'''
    year = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Integer, primary_key=True)
    
    '''Common values'''
    export_val = db.Column(db.Numeric(16,2))
    import_val = db.Column(db.Numeric(16,2))
    export_val_growth = db.Column(db.Float())
    export_val_growth_5 = db.Column(db.Float())

class Pp(db.Model):

    __tablename__ = 'secex_pp'
    hs_id = db.Column(db.String(6), db.ForeignKey(Hs.id), primary_key=True)
    hs_id_t = db.Column(db.String(6), db.ForeignKey(Hs.id), primary_key=True)
    proximity = db.Column(db.Float())

    def __repr__(self):
        return '<Pp {}-{}:{:.2f}>'.format(self.hs_id, self.hs_id_t, self.proximity)

class Ymw(Secex):

    __tablename__ = 'secex_ymw'
    
    '''specific index'''
    wld_id = db.Column(db.String(5), db.ForeignKey(Wld.id), primary_key=True)
    
    '''specific values'''
    eci = db.Column(db.Float())
    bra_diversity = db.Column(db.Integer)
    bra_diversity_eff = db.Column(db.Float())
    hs_diversity = db.Column(db.Integer)
    hs_diversity_eff = db.Column(db.Float())
    
    '''specific ID length fields'''
    wld_id_len = db.Column(db.Integer)

    def __repr__(self):
        return '<Ymw {}.{}.{}>'.format(self.year, self.month, self.wld_id)

class Ymp(Secex):

    __tablename__ = 'secex_ymp'
    
    '''specific index'''
    hs_id = db.Column(db.String(6), db.ForeignKey(Hs.id), primary_key=True)
    
    '''specific values'''
    pci = db.Column(db.Float())
    bra_diversity = db.Column(db.Integer)
    bra_diversity_eff = db.Column(db.Float())
    wld_diversity = db.Column(db.Integer)
    wld_diversity_eff = db.Column(db.Float())
    rca_wld = db.Column(db.Float())
    
    '''specific ID length fields'''
    hs_id_len = db.Column(db.Integer)
    
    def __repr__(self):
        return '<Ymp {0}.{1}.{2}>'.format(self.year, self.month, self.hs_id)

class Ymb(Secex):

    __tablename__ = 'secex_ymb'
    
    '''specific index'''
    bra_id = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    
    '''specific values'''
    eci = db.Column(db.Float())
    hs_diversity = db.Column(db.Integer)
    hs_diversity_eff = db.Column(db.Float())
    wld_diversity = db.Column(db.Integer)
    wld_diversity_eff = db.Column(db.Float())
    
    '''specific ID length fields'''
    bra_id_len = db.Column(db.Integer)

    def __repr__(self):
        return '<Ymb {0}.{1}.{2}>'.format(self.year, self.month, self.bra_id)

############################################################
# ----------------------------------------------------------
# 3 variable tables
# 
############################################################

class Ympw(Secex):

    __tablename__ = 'secex_ympw'
    
    '''specific index'''
    hs_id = db.Column(db.String(6), db.ForeignKey(Hs.id), primary_key=True)
    wld_id = db.Column(db.String(5), db.ForeignKey(Wld.id), primary_key=True)
    
    '''specific ID length fields'''
    hs_id_len = db.Column(db.Integer)
    wld_id_len = db.Column(db.Integer)

    def __repr__(self):
        return '<Ympw {0}.{1}.{2}.{3}>'.format(self.year, self.month, self.hs_id, self.wld_id)

class Ymbp(Secex):

    __tablename__ = 'secex_ymbp'
    
    '''specific index'''
    bra_id = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    hs_id = db.Column(db.String(6), db.ForeignKey(Hs.id), primary_key=True)
    
    '''specific values'''
    rca = db.Column(db.Float())
    rca_wld = db.Column(db.Float())
    rcd = db.Column(db.Float())
    distance = db.Column(db.Float())
    distance_wld = db.Column(db.Float())
    opp_gain = db.Column(db.Float())
    opp_gain_wld = db.Column(db.Float())
    
    '''specific ID length fields'''
    bra_id_len = db.Column(db.Integer)
    hs_id_len = db.Column(db.Integer)

    def __repr__(self):
        return '<Ymbp {0}.{1}.{2}.{3}>'.format(self.year, self.month, self.bra_id, self.hs_id)

class Ymbw(Secex):

    __tablename__ = 'secex_ymbw'
    
    '''specific index'''
    bra_id = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    wld_id = db.Column(db.String(5), db.ForeignKey(Wld.id), primary_key=True)
    
    '''specific ID length fields'''
    bra_id_len = db.Column(db.Integer)
    wld_id_len = db.Column(db.Integer)

    def __repr__(self):
        return '<Ymbw {0}.{1}.{2}.{3}>'.format(self.year, self.month, self.bra_id, self.wld_id)

############################################################
# ----------------------------------------------------------
# 4 variable tables
# 
############################################################

class Ymbpw(Secex):

    __tablename__ = 'secex_ymbpw'
    
    '''specific index'''
    bra_id = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    hs_id = db.Column(db.String(6), db.ForeignKey(Hs.id), primary_key=True)
    wld_id = db.Column(db.String(5), db.ForeignKey(Wld.id), primary_key=True)
    
    '''specific ID length fields'''
    bra_id_len = db.Column(db.Integer)
    hs_id_len = db.Column(db.Integer)
    wld_id_len = db.Column(db.Integer)

    def __repr__(self):
        return '<Ymbpw {0}.{1}.{2}.{3}.{4}>'.format(self.year, self.month, self.bra_id, self.hs_id, self.wld_id)