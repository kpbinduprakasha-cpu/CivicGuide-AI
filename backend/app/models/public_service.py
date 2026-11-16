from datetime import datetime
from . import db

class PublicService(db.Model):
    __tablename__ = 'public_services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, index=True)
    name_kn = db.Column(db.String(250), nullable=True)
    name_hi = db.Column(db.String(250), nullable=True)
    
    category = db.Column(db.String(100), nullable=False, index=True)
    # Categories: 'Central Ministries & Offices', 'AIIMS & Central/State Hospitals', 
    # 'State Secretariat & Collectorates', 'Central/State Universities & IITs', 
    # 'Passport & Aadhaar Seva Kendras', 'Common Service Centres (CSC)', 'Welfare & Pension Offices'
    
    state = db.Column(db.String(100), default='All India', nullable=False, index=True)
    district_city = db.Column(db.String(100), default='National', nullable=False, index=True)
    taluk = db.Column(db.String(100), nullable=True, index=True)
    
    government_level = db.Column(db.String(50), default='Central Government', nullable=False, index=True)
    # 'Central Government' or 'State Government'
    
    address = db.Column(db.Text, nullable=False)
    address_kn = db.Column(db.Text, nullable=True)
    address_hi = db.Column(db.Text, nullable=True)
    
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    phone = db.Column(db.String(100), nullable=True)
    official_url = db.Column(db.String(350), nullable=True)
    verified = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self, lang='en'):
        name = self.name
        address = self.address
        if lang == 'kn':
            name = self.name_kn or self.name
            address = self.address_kn or self.address
        elif lang == 'hi':
            name = self.name_hi or self.name
            address = self.address_hi or self.address

        return {
            'id': self.id,
            'name': name,
            'name_en': self.name,
            'name_kn': self.name_kn,
            'name_hi': self.name_hi,
            'category': self.category,
            'state': self.state,
            'district_city': self.district_city,
            'taluk': self.taluk,
            'government_level': self.government_level,
            'address': address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'phone': self.phone,
            'official_url': self.official_url,
            'verified': self.verified,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
