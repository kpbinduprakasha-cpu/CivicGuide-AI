from datetime import datetime
from . import db

class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    file_path = db.Column(db.String(350), nullable=False)
    source_url = db.Column(db.String(350), nullable=True)
    authority = db.Column(db.String(150), nullable=True) # e.g. 'Department of Women & Child Development, Karnataka'
    publication_date = db.Column(db.String(50), nullable=True)
    jurisdiction = db.Column(db.String(100), default='Karnataka / Vijayanagara District', nullable=False)
    verified = db.Column(db.Boolean, default=True, nullable=False)
    chunk_count = db.Column(db.Integer, default=0, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'file_path': self.file_path,
            'source_url': self.source_url,
            'authority': self.authority,
            'publication_date': self.publication_date,
            'jurisdiction': self.jurisdiction,
            'verified': self.verified,
            'chunk_count': self.chunk_count,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }
