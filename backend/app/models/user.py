import json
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(60), unique=True, nullable=False, index=True) # e.g. rahul123
    full_name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False, default=25)
    mobile_number = db.Column(db.String(20), nullable=False, default='')
    state = db.Column(db.String(100), nullable=False, default='Karnataka')
    sex = db.Column(db.String(30), nullable=False, default='Prefer not to say') # Male, Female, Other, Prefer not to say
    languages = db.Column(db.Text, nullable=False, default='["English"]') # JSON list of languages
    
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False) # 'user' or 'admin'
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Legacy support aliases
    @property
    def username(self):
        return self.user_id

    @username.setter
    def username(self, val):
        self.user_id = val

    @property
    def preferred_language(self):
        try:
            langs = json.loads(self.languages) if self.languages else []
            return langs[0] if langs else 'English'
        except Exception:
            return 'English'

    def get_languages_list(self):
        try:
            return json.loads(self.languages) if self.languages else []
        except Exception:
            return [self.languages] if self.languages else []

    def set_languages_list(self, langs_list):
        if isinstance(langs_list, list):
            self.languages = json.dumps(langs_list)
        else:
            self.languages = json.dumps([str(langs_list)])

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user_id,
            'full_name': self.full_name,
            'age': self.age,
            'mobile_number': self.mobile_number,
            'state': self.state,
            'sex': self.sex,
            'languages': self.get_languages_list(),
            'email': self.email,
            'is_verified': self.is_verified,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
