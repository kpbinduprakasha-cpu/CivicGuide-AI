from flask import Blueprint, request, jsonify, g
from ..models import db, Scheme
from ..auth.jwt_auth import admin_required

scheme_bp = Blueprint('schemes', __name__, url_prefix='/api/schemes')

@scheme_bp.route('', methods=['GET'])
def list_schemes():
    q = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()
    level = request.args.get('level', '').strip()
    lang = request.args.get('lang', 'en').strip()

    query = Scheme.query

    if category and category != 'All':
        query = query.filter(Scheme.category.ilike(f'%{category}%'))

    if level and level != 'All':
        query = query.filter(Scheme.government_level.ilike(f'%{level}%'))

    if q:
        search_filter = (
            Scheme.name.ilike(f'%{q}%') |
            Scheme.name_kn.ilike(f'%{q}%') |
            Scheme.name_hi.ilike(f'%{q}%') |
            Scheme.description.ilike(f'%{q}%') |
            Scheme.benefits.ilike(f'%{q}%') |
            Scheme.category.ilike(f'%{q}%')
        )
        query = query.filter(search_filter)

    schemes = query.order_by(Scheme.id.asc()).all()
    
    return jsonify({
        'count': len(schemes),
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
        'official_url', 'government_level', 'source_date', 'verified'
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
