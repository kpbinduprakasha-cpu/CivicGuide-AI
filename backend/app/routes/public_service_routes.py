import math
from flask import Blueprint, request, jsonify, g
from ..models import db, PublicService
from ..auth.jwt_auth import admin_required

public_service_bp = Blueprint('public_services', __name__, url_prefix='/api/public-services')

def haversine(lat1, lon1, lat2, lon2):
    """Calculate distance in kilometers between two lat/lon points."""
    R = 6371.0 # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@public_service_bp.route('', methods=['GET'])
def list_public_services():
    state = request.args.get('state', '').strip()
    level = request.args.get('level', '').strip() # 'Central Government' or 'State Government'
    taluk = request.args.get('taluk', '').strip()
    district = request.args.get('district', '').strip()
    category = request.args.get('category', '').strip()
    q = request.args.get('q', '').strip()
    lang = request.args.get('lang', 'en').strip()

    query = PublicService.query

    if state and state != 'All' and state != 'All India':
        query = query.filter(PublicService.state.ilike(f'%{state}%'))

    if level and level != 'All':
        query = query.filter(PublicService.government_level.ilike(f'%{level}%'))

    if taluk and taluk != 'All':
        query = query.filter(PublicService.taluk.ilike(f'%{taluk}%'))

    if district and district != 'All':
        query = query.filter(PublicService.district_city.ilike(f'%{district}%'))

    if category and category != 'All':
        query = query.filter(PublicService.category.ilike(f'%{category}%'))

    if q:
        query = query.filter(
            (PublicService.name.ilike(f'%{q}%')) |
            (PublicService.name_kn.ilike(f'%{q}%')) |
            (PublicService.name_hi.ilike(f'%{q}%')) |
            (PublicService.address.ilike(f'%{q}%')) |
            (PublicService.district_city.ilike(f'%{q}%')) |
            (PublicService.state.ilike(f'%{q}%')) |
            (PublicService.taluk.ilike(f'%{q}%'))
        )

    services = query.order_by(PublicService.state.asc(), PublicService.name.asc()).all()
    
    return jsonify({
        'count': len(services),
        'services': [s.to_dict(lang=lang) for s in services]
    }), 200

@public_service_bp.route('/nearby', methods=['GET'])
def get_nearby_services():
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    radius = request.args.get('radius', default=100.0, type=float) # in km
    category = request.args.get('category', '').strip()
    lang = request.args.get('lang', 'en').strip()

    if lat is None or lng is None:
        return jsonify({'error': 'Latitude (lat) and Longitude (lng) are required.'}), 400

    query = PublicService.query
    if category and category != 'All':
        query = query.filter(PublicService.category.ilike(f'%{category}%'))

    all_services = query.all()
    nearby = []

    for s in all_services:
        dist = haversine(lat, lng, s.latitude, s.longitude)
        if dist <= radius:
            item = s.to_dict(lang=lang)
            item['distance_km'] = round(dist, 2)
            nearby.append(item)

    # Sort by nearest first
    nearby.sort(key=lambda x: x['distance_km'])

    return jsonify({
        'user_location': {'latitude': lat, 'longitude': lng},
        'radius_km': radius,
        'count': len(nearby),
        'services': nearby
    }), 200

@public_service_bp.route('/states', methods=['GET'])
def get_states():
    """Return all states and UTs with count of registered services."""
    results = db.session.query(
        PublicService.state,
        db.func.count(PublicService.id)
    ).group_by(PublicService.state).order_by(PublicService.state.asc()).all()

    state_list = [{'state': r[0], 'count': r[1]} for r in results]
    central_count = PublicService.query.filter_by(government_level='Central Government').count()

    return jsonify({
        'country': 'India',
        'central_services_count': central_count,
        'states': state_list
    }), 200

@public_service_bp.route('/taluks', methods=['GET'])
def get_taluks():
    TALUKS = [
        'Hosapete',
        'Harapanahalli',
        'Kudligi',
        'Huvina Hadagali',
        'Hagaribommanahalli',
        'Kottur'
    ]
    
    taluk_stats = []
    for t in TALUKS:
        count = PublicService.query.filter_by(taluk=t).count()
        taluk_stats.append({
            'name': t,
            'service_count': count
        })
        
    return jsonify({
        'district': 'Vijayanagara',
        'state': 'Karnataka',
        'taluks': taluk_stats
    }), 200

@public_service_bp.route('', methods=['POST'])
@admin_required
def create_public_service():
    data = request.get_json() or {}
    
    required = ['name', 'category', 'address', 'latitude', 'longitude']
    for req in required:
        if req not in data:
            return jsonify({'error': f"'{req}' is required."}), 400

    try:
        lat = float(data['latitude'])
        lon = float(data['longitude'])
    except ValueError:
        return jsonify({'error': 'Latitude and longitude must be valid floating numbers.'}), 400

    service = PublicService(
        name=data['name'].strip(),
        name_kn=data.get('name_kn', '').strip() or None,
        name_hi=data.get('name_hi', '').strip() or None,
        category=data['category'].strip(),
        state=data.get('state', 'Central / All India').strip(),
        district_city=data.get('district_city', 'National').strip(),
        taluk=data.get('taluk', '').strip() or None,
        government_level=data.get('government_level', 'Central Government').strip(),
        address=data['address'].strip(),
        latitude=lat,
        longitude=lon,
        phone=data.get('phone', '').strip() or None,
        official_url=data.get('official_url', '').strip() or None,
        verified=bool(data.get('verified', True))
    )

    db.session.add(service)
    db.session.commit()

    return jsonify({
        'message': 'Public service location added successfully.',
        'service': service.to_dict()
    }), 201

@public_service_bp.route('/<int:service_id>', methods=['PUT'])
@admin_required
def update_public_service(service_id):
    service = PublicService.query.get(service_id)
    if not service:
        return jsonify({'error': 'Public service location not found.'}), 404

    data = request.get_json() or {}
    
    fields = ['name', 'name_kn', 'name_hi', 'category', 'state', 'district_city', 'taluk', 'government_level', 'address', 'phone', 'official_url', 'verified']
    for f in fields:
        if f in data:
            setattr(service, f, data[f])

    if 'latitude' in data:
        try:
            service.latitude = float(data['latitude'])
        except ValueError:
            pass

    if 'longitude' in data:
        try:
            service.longitude = float(data['longitude'])
        except ValueError:
            pass

    db.session.commit()
    return jsonify({
        'message': 'Public service record updated successfully.',
        'service': service.to_dict()
    }), 200

@public_service_bp.route('/<int:service_id>', methods=['DELETE'])
@admin_required
def delete_public_service(service_id):
    service = PublicService.query.get(service_id)
    if not service:
        return jsonify({'error': 'Public service record not found.'}), 404

    db.session.delete(service)
    db.session.commit()
    return jsonify({
        'message': f"Service '{service.name}' removed successfully."
    }), 200
