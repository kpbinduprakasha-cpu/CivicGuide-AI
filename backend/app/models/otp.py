from datetime import datetime
from . import db

class OTPVerification(db.Model):
    __tablename__ = 'otp_verifications'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False, index=True)
    user_id = db.Column(db.String(60), nullable=True, index=True)
    otp_code = db.Column(db.String(10), nullable=False) # 6 digits e.g. '482915'
    purpose = db.Column(db.String(30), default='registration', nullable=False) # 'registration' or 'reset_password'
    
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    is_used = db.Column(db.Boolean, default=False, nullable=False)
    attempts = db.Column(db.Integer, default=0, nullable=False)

    def is_expired(self):
        return datetime.utcnow() > self.expires_at

    def increment_attempt(self):
        self.attempts += 1

    def mark_used(self):
        self.is_used = True

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'user_id': self.user_id,
            'purpose': self.purpose,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_used': self.is_used,
            'attempts': self.attempts
        }
