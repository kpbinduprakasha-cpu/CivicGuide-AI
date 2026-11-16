from flask import Blueprint, request, jsonify, g
from ..models import db, Scheme
from ..auth.jwt_auth import admin_required

scheme_bp = Blueprint('schemes', __name__, url_prefix='/api/schemes')

INDIAN_STATES_LIST = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
    "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
    "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
    "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu",
    "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
]

@scheme_bp.route('/states', methods=['GET'])
def list_states():
    """Return all Indian States/UTs with their count of verified schemes."""
    # Count Central Government schemes
    central_count = Scheme.query.filter(Scheme.government_level.ilike('%Central%')).count()
    total_count = Scheme.query.count()

    state_data = []
    for state_name in INDIAN_STATES_LIST:
        # Count schemes matching this state
        st_count = Scheme.query.filter(
            (Scheme.state.ilike(f'%{state_name}%')) |
            (Scheme.government_level.ilike(f'%{state_name}%'))
        ).count()
        state_data.append({
            'name': state_name,
            'state_schemes_count': st_count,
            'total_accessible_count': st_count + central_count
        })

    return jsonify({
        'total_schemes': total_count,
        'central_schemes_count': central_count,
        'states': state_data
    }), 200

@scheme_bp.route('', methods=['GET'])
def list_schemes():
    q = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()
    level = request.args.get('level', '').strip()
    state = request.args.get('state', '').strip()
    mode = request.args.get('mode', '').strip() # 'all', 'central', 'state'
    scope = request.args.get('scope', '').strip() # 'state_only', 'central_only', or 'all'
    include_central = request.args.get('include_central', 'false').lower() in ['true', '1', 'yes']
    lang = request.args.get('lang', 'en').strip()

    query = Scheme.query

    # Category filter
    if category and category != 'All':
        query = query.filter(Scheme.category.ilike(f'%{category}%'))

    # Jurisdiction / Mode / State filtering
    if mode == 'central' or level == 'Central Government' or scope == 'central_only':
        # Show ONLY Central Government schemes
        query = query.filter(Scheme.government_level.ilike('%Central%'))
    elif mode == 'state' or level == 'State Government':
        # State Government schemes mode
        if state and state not in ['All', 'All India', 'All States', '']:
            clean_state = state.replace(' State', '').strip()
            if include_central or scope == 'all':
                query = query.filter(
                    (Scheme.state.ilike(f'%{clean_state}%')) |
                    (Scheme.government_level.ilike(f'%{clean_state}%')) |
                    (Scheme.government_level.ilike('%Central%'))
                )
            else:
                query = query.filter(
                    (Scheme.state.ilike(f'%{clean_state}%')) |
                    (Scheme.government_level.ilike(f'%{clean_state}%'))
                )
        else:
            # All state government schemes across all states
            query = query.filter(~Scheme.government_level.ilike('%Central%'))
    elif state and state not in ['All', 'All India', 'All States', '']:
        clean_state = state.replace(' State', '').strip()
        if scope == 'central_only':
            query = query.filter(Scheme.government_level.ilike('%Central%'))
        elif scope == 'all' or include_central:
            query = query.filter(
                (Scheme.state.ilike(f'%{clean_state}%')) |
                (Scheme.government_level.ilike(f'%{clean_state}%')) |
                (Scheme.government_level.ilike('%Central%'))
            )
        else:
            # When specific state is selected, show that state's schemes
            query = query.filter(
                (Scheme.state.ilike(f'%{clean_state}%')) |
                (Scheme.government_level.ilike(f'%{clean_state}%'))
            )
    elif level and level not in ['All', '']:
        if 'Central' in level:
            query = query.filter(Scheme.government_level.ilike('%Central%'))
        elif 'State' in level:
            query = query.filter(~Scheme.government_level.ilike('%Central%'))
        else:
            query = query.filter(Scheme.government_level.ilike(f'%{level}%'))

    if q:
        search_filter = (
            Scheme.name.ilike(f'%{q}%') |
            Scheme.name_kn.ilike(f'%{q}%') |
            Scheme.name_hi.ilike(f'%{q}%') |
            Scheme.description.ilike(f'%{q}%') |
            Scheme.benefits.ilike(f'%{q}%') |
            Scheme.category.ilike(f'%{q}%') |
            (Scheme.state.ilike(f'%{q}%'))
        )
        query = query.filter(search_filter)

    schemes = query.order_by(Scheme.id.asc()).all()
    
    return jsonify({
        'count': len(schemes),
        'selected_state': state or 'All India',
        'schemes': [s.to_dict(lang=lang) for s in schemes]
    }), 200

@scheme_bp.route('/<int:scheme_id>', methods=['GET'])
def get_scheme(scheme_id):
    lang = request.args.get('lang', 'en').strip()
    scheme = Scheme.query.get(scheme_id)
    if not scheme:
        return jsonify({'error': 'Scheme not found.'}), 404
    return jsonify({
        'scheme': scheme.to_dict(lang=lang)
    }), 200

@scheme_bp.route('', methods=['POST'])
@admin_required
def create_scheme():
    data = request.get_json() or {}
    
    required_fields = ['name', 'description', 'category', 'eligibility', 'benefits', 'required_documents', 'application_process', 'official_url']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f"'{field}' is required."}), 400

    scheme = Scheme(
        name=data['name'].strip(),
        name_kn=data.get('name_kn', '').strip() or None,
        name_hi=data.get('name_hi', '').strip() or None,
        description=data['description'].strip(),
        description_kn=data.get('description_kn', '').strip() or None,
        description_hi=data.get('description_hi', '').strip() or None,
        category=data['category'].strip(),
        eligibility=data['eligibility'].strip(),
        eligibility_kn=data.get('eligibility_kn', '').strip() or None,
        eligibility_hi=data.get('eligibility_hi', '').strip() or None,
        benefits=data['benefits'].strip(),
        benefits_kn=data.get('benefits_kn', '').strip() or None,
        benefits_hi=data.get('benefits_hi', '').strip() or None,
        required_documents=data['required_documents'].strip(),
        application_process=data['application_process'].strip(),
        official_url=data['official_url'].strip(),
        government_level=data.get('government_level', 'Karnataka State'),
        state=data.get('state', 'All India' if 'Central' in data.get('government_level', '') else 'Karnataka'),
        source_date=data.get('source_date', '2024-2026'),
        verified=bool(data.get('verified', True))
    )
    
    db.session.add(scheme)
    db.session.commit()

    return jsonify({
        'message': 'Government scheme added successfully.',
        'scheme': scheme.to_dict()
    }), 201

@scheme_bp.route('/<int:scheme_id>', methods=['PUT'])
@admin_required
def update_scheme(scheme_id):
    scheme = Scheme.query.get(scheme_id)
    if not scheme:
        return jsonify({'error': 'Scheme not found.'}), 404

    data = request.get_json() or {}
    
    updatable_fields = [
        'name', 'name_kn', 'name_hi',
        'description', 'description_kn', 'description_hi',
        'category',
        'eligibility', 'eligibility_kn', 'eligibility_hi',
        'benefits', 'benefits_kn', 'benefits_hi',
        'required_documents', 'application_process',
        'official_url', 'government_level', 'state', 'source_date', 'verified'
    ]

    for field in updatable_fields:
        if field in data:
            setattr(scheme, field, data[field])

    db.session.commit()
    return jsonify({
        'message': 'Government scheme updated successfully.',
        'scheme': scheme.to_dict()
    }), 200

@scheme_bp.route('/<int:scheme_id>', methods=['DELETE'])
@admin_required
def delete_scheme(scheme_id):
    scheme = Scheme.query.get(scheme_id)
    if not scheme:
        return jsonify({'error': 'Scheme not found.'}), 404

    db.session.delete(scheme)
    db.session.commit()
    return jsonify({
        'message': f"Scheme '{scheme.name}' has been deleted."
    }), 200
