from flask import Blueprint, request, jsonify, g
from ..models import db, Scheme
from ..auth.jwt_auth import admin_required
from ..services.eligibility_service import EligibilityService

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

    # Jurisdiction / Mode / State filtering:
    # 1. Central Government: shows central government schemes
    # 2. State Government: only when selecting a state, show that particular state's schemes; otherwise no show
    # 3. All: combines both Central and State government schemes together
    if mode == 'central' or level == 'Central Government' or scope == 'central_only':
        query = query.filter(Scheme.government_level.ilike('%Central%'))
    elif mode == 'state' or level == 'State Government' or scope == 'state_only':
        if state and state not in ['All', 'All India', 'All States', '']:
            clean_state = state.replace(' State', '').strip()
            query = query.filter(
                (Scheme.state.ilike(f'%{clean_state}%')) |
                (Scheme.government_level.ilike(f'%{clean_state}%'))
            )
        else:
            # When State Government is selected without a particular state: otherwise no show
            query = query.filter(Scheme.id == -1)
    # All / default queries return all verified schemes combining Central & State Government

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

@scheme_bp.route('/recommendations', methods=['POST'])
def recommend_schemes():
    """
    Evaluates citizen demographics and returns personalized scheme recommendations
    with criteria match badges and eligibility confidence scores.
    """
    data = request.get_json() or {}
    lang = data.get('lang', 'en').strip().lower()
    if lang not in ['en', 'kn', 'hi']:
        lang = 'en'

    eval_results = EligibilityService.evaluate(data, language=lang)
    lookup = {res['scheme_id']: res for res in eval_results}

    schemes = Scheme.query.order_by(Scheme.id.asc()).all()
    results = []
    
    for s in schemes:
        eval_data = lookup.get(s.id)
        s_dict = s.to_dict(lang=lang)
        if eval_data:
            s_dict['match_status'] = eval_data['status']
            s_dict['satisfied_criteria'] = eval_data['satisfied_criteria']
            s_dict['unmet_criteria'] = eval_data['unmet_criteria']
            s_dict['explanation'] = eval_data['explanation']
            # Match score: count satisfied conditions
            s_dict['match_score'] = len(eval_data['satisfied_criteria'])
        else:
            s_dict['match_status'] = 'Possibly Eligible'
            s_dict['satisfied_criteria'] = []
            s_dict['unmet_criteria'] = []
            s_dict['match_score'] = 1

        results.append(s_dict)

    # Sort: Eligible/Possibly Eligible first, then descending match_score
    results.sort(key=lambda x: (
        1 if x['match_status'] in ['Eligible', 'Possibly Eligible'] else (
            0.5 if 'Partially' in x['match_status'] else 0
        ),
        x['match_score']
    ), reverse=True)

    return jsonify({
        'count': len(results),
        'recommended_count': len([r for r in results if r['match_status'] in ['Eligible', 'Possibly Eligible']]),
        'schemes': results
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
