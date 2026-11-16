import json
from datetime import datetime
from . import db

class ChatHistory(db.Model):
    __tablename__ = 'chat_histories'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(10), default='en', nullable=False)
    sources = db.Column(db.Text, nullable=True) # JSON array of citations
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def to_dict(self):
        parsed_sources = []
        if self.sources:
            try:
                parsed_sources = json.loads(self.sources)
            except Exception:
                parsed_sources = []
        return {
            'id': self.id,
            'user_id': self.user_id,
            'question': self.question,
            'answer': self.answer,
            'language': self.language,
            'sources': parsed_sources,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
