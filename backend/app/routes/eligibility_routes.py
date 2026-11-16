from flask import Blueprint, request, jsonify
from ..services.eligibility_service import EligibilityService

eligibility_bp = Blueprint('eligibility', __name__, url_prefix='/api/eligibility')

@eligibility_bp.route('/check', methods=['POST'])
def check_eligibility():
    data = request.get_json() or {}
    language = data.get('language', 'en').strip().lower()
    if language not in ['en', 'kn', 'hi']:
        language = 'en'

    results = EligibilityService.evaluate(data, language=language)

    return jsonify({
        'count': len(results),
        'results': results,
        'language': language
    }), 200
