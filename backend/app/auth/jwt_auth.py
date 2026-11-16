import functools
from flask import request, jsonify, g, current_app
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from ..models import db, User

def get_serializer():
    secret_key = current_app.config['SECRET_KEY']
    return URLSafeTimedSerializer(secret_key)

def generate_auth_token(user_id, role='user', expires_in=86400):
    """Generate a tamper-proof cryptographically signed token."""
    s = get_serializer()
    return s.dumps({'user_id': user_id, 'role': role})

def verify_auth_token(token, max_age=86400):
    """Verify and decode the signed token."""
    s = get_serializer()
    try:
        data = s.loads(token, max_age=max_age)
        return data
    except (SignatureExpired, BadSignature):
        return None

def get_token_from_header():
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
        return None
    parts = auth_header.split()
    if len(parts) == 2 and parts[0].lower() == 'bearer':
        return parts[1]
    elif len(parts) == 1:
        return parts[0]
    return None

def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        token = get_token_from_header()
        if not token:
            return jsonify({'error': 'Authentication required. Missing Authorization token.'}), 401
        
        payload = verify_auth_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired session. Please log in again.'}), 401
        
        user = db.session.get(User, payload.get('user_id'))
        if not user:
            return jsonify({'error': 'User account not found.'}), 401
        
        g.current_user = user
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        token = get_token_from_header()
        if not token:
            return jsonify({'error': 'Admin authorization required.'}), 401
        
        payload = verify_auth_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired session.'}), 401
        
        if payload.get('role') != 'admin':
            return jsonify({'error': 'Access denied. Administrator privileges required.'}), 403
        
        user = db.session.get(User, payload.get('user_id'))
        if not user or user.role != 'admin':
            return jsonify({'error': 'Access denied. Administrator privileges required.'}), 403
        
        g.current_user = user
        return f(*args, **kwargs)
    return decorated_function

def optional_login(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        token = get_token_from_header()
        g.current_user = None
        if token:
            payload = verify_auth_token(token)
            if payload:
                user = db.session.get(User, payload.get('user_id'))
                if user:
                    g.current_user = user
        return f(*args, **kwargs)
    return decorated_function
