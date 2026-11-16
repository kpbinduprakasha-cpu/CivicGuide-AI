import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..'))

DATABASE_DIR = os.path.join(PROJECT_ROOT, 'database')
DOCUMENTS_DIR = os.path.join(PROJECT_ROOT, 'documents')
CHROMA_DIR = os.path.join(DATABASE_DIR, 'chroma_store')

# Ensure core directories exist
os.makedirs(DATABASE_DIR, exist_ok=True)
os.makedirs(DOCUMENTS_DIR, exist_ok=True)
os.makedirs(CHROMA_DIR, exist_ok=True)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secure-auth-jwt-secret-key-2026-production-ready')
    
    # SQLite Database path for local dev; supports PostgreSQL via DATABASE_URL
    DB_PATH = os.path.join(DATABASE_DIR, 'users.db').replace('\\', '/')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f'sqlite:///{DB_PATH}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Token / Session Expiration
    JWT_EXPIRATION_HOURS = int(os.environ.get('JWT_EXPIRATION_HOURS', 24))
    
    # OTP Configuration (5 minutes expiry, 60 seconds resend cooldown)
    OTP_EXPIRY_SECONDS = int(os.environ.get('OTP_EXPIRY_SECONDS', 300))
    OTP_RESEND_COOLDOWN_SECONDS = int(os.environ.get('OTP_RESEND_COOLDOWN_SECONDS', 60))
    OTP_MAX_ATTEMPTS = int(os.environ.get('OTP_MAX_ATTEMPTS', 5))
    
    # SMTP Email Configuration (Supports Gmail SMTP with App Password)
    SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
    SMTP_USERNAME = os.environ.get('SMTP_USERNAME', '')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
    SMTP_USE_TLS = os.environ.get('SMTP_USE_TLS', 'True').lower() in ['true', '1', 't']
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'Secure Auth <noreply@secureportal.com>')
    
    # In development mode, if SMTP credentials are missing, system logs OTP to console and returns in dev response
    DEV_MODE_MOCK_EMAIL = os.environ.get('DEV_MODE_MOCK_EMAIL', 'True').lower() in ['true', '1', 't']
    
    # Ollama Local AI & RAG Configuration (Retained for extended capabilities)
    OLLAMA_URL = os.environ.get('OLLAMA_URL', 'http://localhost:11434')
    OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL', 'qwen2.5:latest')
    CHROMA_PERSIST_DIR = CHROMA_DIR
    DOCUMENTS_DIR = DOCUMENTS_DIR
    
    # Max file upload size (16MB)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'pdf', 'txt', 'md'}
