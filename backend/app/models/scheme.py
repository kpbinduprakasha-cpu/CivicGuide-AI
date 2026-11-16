from datetime import datetime
from . import db

class Scheme(db.Model):
    __tablename__ = 'schemes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, index=True)
    name_kn = db.Column(db.String(250), nullable=True)
    name_hi = db.Column(db.String(250), nullable=True)
    
    description = db.Column(db.Text, nullable=False)
    description_kn = db.Column(db.Text, nullable=True)
    description_hi = db.Column(db.Text, nullable=True)
    
    category = db.Column(db.String(100), nullable=False, index=True) 
    # Categories: Education, Agriculture, Healthcare, Employment, Housing, 
    # Women and child welfare, Social welfare, Financial assistance
    
    eligibility = db.Column(db.Text, nullable=False)
    eligibility_kn = db.Column(db.Text, nullable=True)
    eligibility_hi = db.Column(db.Text, nullable=True)
    
    benefits = db.Column(db.Text, nullable=False)
    benefits_kn = db.Column(db.Text, nullable=True)
    benefits_hi = db.Column(db.Text, nullable=True)
    
    required_documents = db.Column(db.Text, nullable=False)
    application_process = db.Column(db.Text, nullable=False)
    official_url = db.Column(db.String(350), nullable=False)
    
    government_level = db.Column(db.String(50), default='Karnataka State', nullable=False) # 'Karnataka State' or 'Central Government'
    state = db.Column(db.String(100), default='All India', nullable=True) # e.g. 'Karnataka', 'Maharashtra', 'Delhi', 'All India'
    source_date = db.Column(db.String(50), nullable=True)
    verified = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self, lang='en'):
        name = self.name
        description = self.description
        eligibility = self.eligibility
        benefits = self.benefits
        
        if lang == 'kn':
            name = self.name_kn or self.name
            description = self.description_kn or self.description
            eligibility = self.eligibility_kn or self.eligibility
            benefits = self.benefits_kn or self.benefits
        elif lang == 'hi':
            name = self.name_hi or self.name
            description = self.description_hi or self.description
            eligibility = self.eligibility_hi or self.eligibility
            benefits = self.benefits_hi or self.benefits

        state_val = self.state
        if not state_val:
            if 'Central' in (self.government_level or ''):
                state_val = 'All India'
            elif 'Karnataka' in (self.government_level or ''):
                state_val = 'Karnataka'
            elif 'Maharashtra' in (self.government_level or ''):
                state_val = 'Maharashtra'
            elif 'Delhi' in (self.government_level or ''):
                state_val = 'Delhi'
            else:
                state_val = (self.government_level or '').replace(' State', '').strip()

        return {
            'id': self.id,
            'name': name,
            'name_en': self.name,
            'name_kn': self.name_kn,
            'name_hi': self.name_hi,
            'description': description,
            'description_en': self.description,
            'description_kn': self.description_kn,
            'description_hi': self.description_hi,
            'category': self.category,
            'eligibility': eligibility,
            'eligibility_en': self.eligibility,
            'eligibility_kn': self.eligibility_kn,
            'eligibility_hi': self.eligibility_hi,
            'benefits': benefits,
            'benefits_en': self.benefits,
            'benefits_kn': self.benefits_kn,
            'benefits_hi': self.benefits_hi,
            'required_documents': self.required_documents,
            'application_process': self.application_process,
            'official_url': self.official_url,
            'government_level': self.government_level,
            'state': state_val,
            'source_date': self.source_date,
            'verified': self.verified,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
