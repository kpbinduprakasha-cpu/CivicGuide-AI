import re
import random
import json
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, g, current_app
from ..models import db, User, OTPVerification
from ..auth.jwt_auth import generate_auth_token, login_required
from ..utils.user_id_generator import generate_unique_user_id
from ..services.email_service import EmailService

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
PHONE_REGEX = r'^[6-9]\d{9}$'

INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
    "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
    "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
    "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu",
    "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
]

@auth_bp.route('/states', methods=['GET'])
def get_indian_states():
    """Return list of Indian states & UTs for registration dropdown."""
    return jsonify({'states': INDIAN_STATES}), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Step 1: One-time account registration.
    Validates all personal details, auto-generates a unique User ID, creates unverified user,
    and sends a 6-digit OTP to the registered email address.
    """
    data = request.get_json() or {}
    
    full_name = data.get('full_name', '').strip()
    age = data.get('age')
    mobile_number = data.get('mobile_number', '').strip()
    state = data.get('state', '').strip()
    sex = data.get('sex', '').strip()
    languages = data.get('languages', [])
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    confirm_password = data.get('confirm_password', '')

    # 1. Field Validations
    if not full_name or len(full_name) < 2:
        return jsonify({'error': 'Full Name is required (minimum 2 characters).'}), 400

    try:
        age_int = int(age)
        if age_int < 1 or age_int > 120:
            return jsonify({'error': 'Please enter a valid age between 1 and 120.'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Age must be a valid number.'}), 400

    # Mobile validation (10 digits starting with 6-9 for India, or 10 digits clean)
    clean_phone = re.sub(r'[^0-9]', '', mobile_number)
    if len(clean_phone) == 12 and clean_phone.startswith('91'):
        clean_phone = clean_phone[2:]
    if len(clean_phone) != 10:
        return jsonify({'error': 'Please enter a valid 10-digit mobile number.'}), 400

    if not state:
        return jsonify({'error': 'State is required. Please select your State.'}), 400

    valid_sex = ['Male', 'Female', 'Other', 'Prefer not to say']
    if sex not in valid_sex:
        return jsonify({'error': f'Sex must be one of: {", ".join(valid_sex)}.'}), 400

    # Languages list validation
    if isinstance(languages, str):
        languages = [l.strip() for l in languages.split(',') if l.strip()]
    if not isinstance(languages, list) or len(languages) == 0:
        languages = ['English']

    if not email or not re.match(EMAIL_REGEX, email):
        return jsonify({'error': 'A valid email address is required.'}), 400

    if not password or len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters long.'}), 400

    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match.'}), 400

    # 2. Check if email is already registered and verified
    existing_user = User.query.filter_by(email=email).first()
    if existing_user and existing_user.is_verified:
        return jsonify({
            'error': f'An account is already registered with this email. Please log in using your User ID (@{existing_user.user_id}).'
        }), 409

    # 3. Generate or reuse User ID
    if existing_user and not existing_user.is_verified:
        user = existing_user
        user_id = existing_user.user_id
    else:
        user_id = generate_unique_user_id(full_name)
        user = User(
            user_id=user_id,
            email=email
        )
        db.session.add(user)

    # Update personal fields
    user.full_name = full_name
    user.age = age_int
    user.mobile_number = clean_phone
    user.state = state
    user.sex = sex
    user.set_languages_list(languages)
    user.set_password(password)
    user.is_verified = False # Must verify OTP to activate!
    user.role = 'user'

    # 4. Generate 6-Digit OTP (5 minutes expiration)
    otp_code = str(random.randint(100000, 999999))
    expires_at = datetime.utcnow() + timedelta(seconds=current_app.config['OTP_EXPIRY_SECONDS'])

    # Invalidate prior unused registration OTPs for this email
    OTPVerification.query.filter_by(email=email, purpose='registration', is_used=False).update({'is_used': True})

    otp_record = OTPVerification(
        email=email,
        user_id=user_id,
        otp_code=otp_code,
        purpose='registration',
        expires_at=expires_at,
        is_used=False,
        attempts=0
    )
    db.session.add(otp_record)
    db.session.commit()

    # 5. Send OTP via Email
    dispatch_result = EmailService.send_otp_email(
        recipient_email=email,
        otp_code=otp_code,
        purpose='registration',
        user_name=full_name
    )

    return jsonify({
        'message': f'Account registration initiated. A 6-digit verification code has been sent to {email}.',
        'email': email,
        'user_id': user_id,
        'cooldown_seconds': current_app.config['OTP_RESEND_COOLDOWN_SECONDS'],
        'expires_in_seconds': current_app.config['OTP_EXPIRY_SECONDS'],
        'dev_otp': dispatch_result.get('dev_otp')
    }), 201

@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    """
    Step 2: Compulsory OTP verification.
    Verifies 6-digit OTP, activates the user account, and returns the assigned User ID and auth token.
    """
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    otp_input = data.get('otp', '').strip()

    if not email or not otp_input:
        return jsonify({'error': 'Email and 6-digit OTP are required.'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'No registration record found for this email.'}), 404

    # Fetch latest unused OTP for registration
    otp_record = OTPVerification.query.filter_by(
        email=email,
        purpose='registration',
        is_used=False
    ).order_by(OTPVerification.created_at.desc()).first()

    if not otp_record:
        return jsonify({'error': 'No active verification code found. Please request a new OTP.'}), 400

    # Expiration check (5 minutes)
    if otp_record.is_expired():
        return jsonify({'error': 'Verification code has expired. Please request a new OTP.'}), 400

    # Rate limiting on failed attempts (max 5)
    if otp_record.attempts >= current_app.config.get('OTP_MAX_ATTEMPTS', 5):
        return jsonify({'error': 'Too many incorrect attempts. Please request a new verification code.'}), 429

    # Verify code match
    if otp_record.otp_code != otp_input:
        otp_record.increment_attempt()
        db.session.commit()
        remaining = current_app.config.get('OTP_MAX_ATTEMPTS', 5) - otp_record.attempts
        return jsonify({
            'error': f'Incorrect verification code. {remaining} attempt(s) remaining.'
        }), 400

    # Mark OTP as used and activate account
    otp_record.mark_used()
    user.is_verified = True
    db.session.commit()

    token = generate_auth_token(user.id, user.role)

    return jsonify({
        'message': 'Registration Successful! Your account has been verified and activated.',
        'user_id': user.user_id,
        'user': user.to_dict(),
        'token': token
    }), 200

@auth_bp.route('/resend-otp', methods=['POST'])
def resend_otp():
    """
    Resend 6-digit OTP with a strict 60-second cooldown period.
    """
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    purpose = data.get('purpose', 'registration').strip()

    if not email or not re.match(EMAIL_REGEX, email):
        return jsonify({'error': 'Valid email address is required.'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'No account associated with this email.'}), 404

    # Enforce 60-second cooldown from the most recent OTP creation
    recent_otp = OTPVerification.query.filter_by(
        email=email,
        purpose=purpose
    ).order_by(OTPVerification.created_at.desc()).first()

    cooldown = current_app.config['OTP_RESEND_COOLDOWN_SECONDS']
    if recent_otp:
        elapsed = (datetime.utcnow() - recent_otp.created_at).total_seconds()
        if elapsed < cooldown:
            wait_seconds = int(cooldown - elapsed)
            return jsonify({
                'error': f'Please wait {wait_seconds} seconds before requesting another code.',
                'wait_seconds': wait_seconds
            }), 429

    # Generate fresh 6-digit OTP
    otp_code = str(random.randint(100000, 999999))
    expires_at = datetime.utcnow() + timedelta(seconds=current_app.config['OTP_EXPIRY_SECONDS'])

    # Invalidate previous unused OTPs
    OTPVerification.query.filter_by(email=email, purpose=purpose, is_used=False).update({'is_used': True})

    new_otp = OTPVerification(
        email=email,
        user_id=user.user_id,
        otp_code=otp_code,
        purpose=purpose,
        expires_at=expires_at,
        is_used=False,
        attempts=0
    )
    db.session.add(new_otp)
    db.session.commit()

    dispatch_result = EmailService.send_otp_email(
        recipient_email=email,
        otp_code=otp_code,
        purpose=purpose,
        user_name=user.full_name
    )

    return jsonify({
        'message': f'A new 6-digit verification code has been sent to {email}.',
        'cooldown_seconds': cooldown,
        'expires_in_seconds': current_app.config['OTP_EXPIRY_SECONDS'],
        'dev_otp': dispatch_result.get('dev_otp')
    }), 200

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login endpoint.
    Users log in with their registered User ID (e.g. rahul123) and Password.
    OTP is NOT required for regular returning logins.
    """
    data = request.get_json() or {}
    user_id_input = data.get('user_id', '').strip() or data.get('identifier', '').strip()
    password = data.get('password', '')

    if not user_id_input or not password:
        return jsonify({'error': 'Please enter your User ID and Password.'}), 400

    # Look up by user_id or email
    user = User.query.filter(
        (User.user_id.ilike(user_id_input)) | (User.email.ilike(user_id_input))
    ).first()

    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid User ID or Password. Please check your credentials.'}), 401

    # Check email verification status: compulsory before login!
    if not user.is_verified:
        return jsonify({
            'error': 'Your email address has not been verified yet. Please complete OTP verification to activate your account.',
            'needs_verification': True,
            'email': user.email,
            'user_id': user.user_id
        }), 403

    token = generate_auth_token(user.id, user.role)

    return jsonify({
        'message': f'Welcome back, {user.full_name}!',
        'user_id': user.user_id,
        'user': user.to_dict(),
        'token': token
    }), 200

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """
    Initiate password reset by sending a 6-digit reset OTP to the registered email.
    """
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()

    if not email or not re.match(EMAIL_REGEX, email):
        return jsonify({'error': 'Please provide a valid registered email address.'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.is_verified:
        return jsonify({'error': 'No active account found with this email address.'}), 404

    # Cooldown check
    recent_otp = OTPVerification.query.filter_by(
        email=email,
        purpose='reset_password'
    ).order_by(OTPVerification.created_at.desc()).first()

    cooldown = current_app.config['OTP_RESEND_COOLDOWN_SECONDS']
    if recent_otp:
        elapsed = (datetime.utcnow() - recent_otp.created_at).total_seconds()
        if elapsed < cooldown:
            wait_seconds = int(cooldown - elapsed)
            return jsonify({
                'error': f'Please wait {wait_seconds} seconds before requesting another reset code.',
                'wait_seconds': wait_seconds
            }), 429

    otp_code = str(random.randint(100000, 999999))
    expires_at = datetime.utcnow() + timedelta(seconds=current_app.config['OTP_EXPIRY_SECONDS'])

    OTPVerification.query.filter_by(email=email, purpose='reset_password', is_used=False).update({'is_used': True})

    otp_record = OTPVerification(
        email=email,
        user_id=user.user_id,
        otp_code=otp_code,
        purpose='reset_password',
        expires_at=expires_at,
        is_used=False,
        attempts=0
    )
    db.session.add(otp_record)
    db.session.commit()

    dispatch_result = EmailService.send_otp_email(
        recipient_email=email,
        otp_code=otp_code,
        purpose='reset_password',
        user_name=user.full_name
    )

    return jsonify({
        'message': f'Password reset code sent to {email}.',
        'email': email,
        'cooldown_seconds': cooldown,
        'expires_in_seconds': current_app.config['OTP_EXPIRY_SECONDS'],
        'dev_otp': dispatch_result.get('dev_otp')
    }), 200

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """
    Verify reset OTP and set new password.
    """
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    otp_input = data.get('otp', '').strip()
    new_password = data.get('new_password', '')
    confirm_password = data.get('confirm_password', '')

    if not email or not otp_input:
        return jsonify({'error': 'Email and 6-digit OTP code are required.'}), 400

    if not new_password or len(new_password) < 8:
        return jsonify({'error': 'New password must be at least 8 characters long.'}), 400

    if new_password != confirm_password:
        return jsonify({'error': 'Passwords do not match.'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'No account found with this email.'}), 404

    otp_record = OTPVerification.query.filter_by(
        email=email,
        purpose='reset_password',
        is_used=False
    ).order_by(OTPVerification.created_at.desc()).first()

    if not otp_record:
        return jsonify({'error': 'No active reset request found. Please request a new OTP.'}), 400

    if otp_record.is_expired():
        return jsonify({'error': 'Reset code has expired. Please request a new OTP.'}), 400

    if otp_record.attempts >= current_app.config.get('OTP_MAX_ATTEMPTS', 5):
        return jsonify({'error': 'Too many failed attempts. Please request a new code.'}), 429

    if otp_record.otp_code != otp_input:
        otp_record.increment_attempt()
        db.session.commit()
        remaining = current_app.config.get('OTP_MAX_ATTEMPTS', 5) - otp_record.attempts
        return jsonify({'error': f'Invalid reset code. {remaining} attempt(s) remaining.'}), 400

    # Mark OTP used and update password
    otp_record.mark_used()
    user.set_password(new_password)
    db.session.commit()

    return jsonify({
        'message': f'Password updated successfully! You can now log in with your User ID (@{user.user_id}).',
        'user_id': user.user_id
    }), 200

@auth_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    """Return authenticated citizen profile."""
    return jsonify({
        'user': g.current_user.to_dict()
    }), 200

@auth_bp.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    """
    Update profile details: Name, Age, Mobile, State, Sex, Languages.
    """
    user = g.current_user
    data = request.get_json() or {}

    if 'full_name' in data and len(data['full_name'].strip()) >= 2:
        user.full_name = data['full_name'].strip()

    if 'age' in data:
        try:
            age_int = int(data['age'])
            if 1 <= age_int <= 120:
                user.age = age_int
        except (ValueError, TypeError):
            pass

    if 'mobile_number' in data:
        clean_phone = re.sub(r'[^0-9]', '', str(data['mobile_number']))
        if len(clean_phone) == 12 and clean_phone.startswith('91'):
            clean_phone = clean_phone[2:]
        if len(clean_phone) == 10:
            user.mobile_number = clean_phone

    if 'state' in data and data['state'].strip():
        user.state = data['state'].strip()

    if 'sex' in data and data['sex'].strip() in ['Male', 'Female', 'Other', 'Prefer not to say']:
        user.sex = data['sex'].strip()

    if 'languages' in data:
        user.set_languages_list(data['languages'])

    db.session.commit()

    return jsonify({
        'message': 'Profile updated successfully.',
        'user': user.to_dict()
    }), 200

@auth_bp.route('/change-password', methods=['PUT'])
@login_required
def change_password():
    """Change password for authenticated user."""
    user = g.current_user
    data = request.get_json() or {}
    
    current_password = data.get('current_password', '')
    new_password = data.get('new_password', '')
    confirm_password = data.get('confirm_password', '')

    if not user.check_password(current_password):
        return jsonify({'error': 'Current password is incorrect.'}), 400

    if not new_password or len(new_password) < 8:
        return jsonify({'error': 'New password must be at least 8 characters long.'}), 400

    if new_password != confirm_password:
        return jsonify({'error': 'New passwords do not match.'}), 400

    user.set_password(new_password)
    db.session.commit()

    return jsonify({
        'message': 'Password changed successfully.'
    }), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'Logged out successfully.'}), 200
