import re
import secrets
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, g
from ..models import db, User
from ..auth.jwt_auth import generate_auth_token, login_required

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    
    full_name = data.get('full_name', '').strip()
    email = data.get('email', '').strip().lower()
    username = data.get('username', '').strip().lower()
    password = data.get('password', '')
    confirm_password = data.get('confirm_password', '')
    preferred_language = data.get('preferred_language', 'en').strip().lower()

    # Field validations
    if not full_name:
        return jsonify({'error': 'Full name is required.'}), 400
    if not email or not re.match(EMAIL_REGEX, email):
        return jsonify({'error': 'A valid email address is required.'}), 400
    if not username or len(username) < 3:
        return jsonify({'error': 'Username must be at least 3 characters long.'}), 400
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return jsonify({'error': 'Username can only contain letters, numbers, and underscores.'}), 400
    if not password or len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters long.'}), 400
    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match.'}), 400
    if preferred_language not in ['en', 'kn', 'hi']:
        preferred_language = 'en'

    # Check uniqueness
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'An account with this email address already exists.'}), 409
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'This username is already taken. Please choose another.'}), 409

    # Create user with secure password hash
    user = User(
        full_name=full_name,
        email=email,
        username=username,
        role='user',
        preferred_language=preferred_language
    )
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()

    token = generate_auth_token(user.id, user.role)

    return jsonify({
        'message': 'Account created successfully! Welcome to CivicGuide AI.',
        'user': user.to_dict(),
        'token': token
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    identifier = data.get('identifier', '').strip().lower() # email or username
    password = data.get('password', '')

    if not identifier or not password:
        return jsonify({'error': 'Please provide email/username and password.'}), 400

    # Find by email or username
    user = User.query.filter(
        (User.email == identifier) | (User.username == identifier)
    ).first()

    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials. Please verify your username/email and password.'}), 401

    token = generate_auth_token(user.id, user.role)

    return jsonify({
        'message': f'Welcome back, {user.full_name}!',
        'user': user.to_dict(),
        'token': token
    }), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'Logged out successfully.'}), 200

@auth_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    return jsonify({
        'user': g.current_user.to_dict()
    }), 200

@auth_bp.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    data = request.get_json() or {}
    user = g.current_user

    if 'full_name' in data and data['full_name'].strip():
        user.full_name = data['full_name'].strip()
    
    if 'preferred_language' in data and data['preferred_language'] in ['en', 'kn', 'hi']:
        user.preferred_language = data['preferred_language']

    db.session.commit()
    return jsonify({
        'message': 'Profile updated successfully.',
        'user': user.to_dict()
    }), 200

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json() or {}
    identifier = data.get('identifier', '').strip().lower()

    if not identifier:
        return jsonify({'error': 'Please enter your registered email or username.'}), 400

    user = User.query.filter(
        (User.email == identifier) | (User.username == identifier)
    ).first()

    if not user:
        # Avoid user enumeration by returning a standard courteous response
        return jsonify({
            'message': 'If an account exists with this email or username, password reset instructions have been generated.'
        }), 200

    # Generate secure reset token
    reset_token = secrets.token_urlsafe(32)
    user.reset_token = reset_token
    user.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
    db.session.commit()

    # In local/demo environment, return the token directly for seamless testing
    return jsonify({
        'message': 'Password reset token generated successfully.',
        'reset_token': reset_token,
        'info': f'For demonstration purposes, your reset token is: {reset_token}'
    }), 200

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json() or {}
    token = data.get('token', '').strip()
    new_password = data.get('password', '')
    confirm_password = data.get('confirm_password', '')

    if not token:
        return jsonify({'error': 'Reset token is required.'}), 400
    if not new_password or len(new_password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters long.'}), 400
    if new_password != confirm_password:
        return jsonify({'error': 'Passwords do not match.'}), 400

    user = User.query.filter_by(reset_token=token).first()
    if not user or not user.reset_token_expiry or user.reset_token_expiry < datetime.utcnow():
        return jsonify({'error': 'Invalid or expired password reset token. Please request a new one.'}), 400

    user.set_password(new_password)
    user.reset_token = None
    user.reset_token_expiry = None
    db.session.commit()

    return jsonify({
        'message': 'Password reset successful! You can now log in with your new password.'
    }), 200
