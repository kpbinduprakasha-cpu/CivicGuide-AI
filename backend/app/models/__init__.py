from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .otp import OTPVerification
from .scheme import Scheme
from .public_service import PublicService
from .chat import ChatHistory
from .document import Document

__all__ = ['db', 'User', 'OTPVerification', 'Scheme', 'PublicService', 'ChatHistory', 'Document']
