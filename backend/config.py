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
    SECRET_KEY = os.environ.get('SECRET_KEY', 'civicguide-secret-key-2026-secure-token')
    
    # SQLite Database path in database/ folder (with forward slash formatting for SQLite URI on Windows)
    DB_PATH = os.path.join(DATABASE_DIR, 'civicguide.db').replace('\\', '/')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f'sqlite:///{DB_PATH}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Ollama Local AI Configuration
    OLLAMA_URL = os.environ.get('OLLAMA_URL', 'http://localhost:11434')
    OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL', 'qwen2.5:latest')
    
    # ChromaDB & Vector Store
    CHROMA_PERSIST_DIR = CHROMA_DIR
    DOCUMENTS_DIR = DOCUMENTS_DIR
    
    # Session / JWT expiration
    JWT_EXPIRATION_HOURS = 24
    
    # Max file upload size (16MB)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'pdf', 'txt', 'md'}
