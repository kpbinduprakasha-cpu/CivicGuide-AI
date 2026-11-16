from flask import Blueprint, request, jsonify

voice_bp = Blueprint('voice', __name__, url_prefix='/api/voice')

@voice_bp.route('/transcribe', methods=['POST'])
def transcribe():
    """
    Multilingual voice transcription endpoint.
    Complements client-side Web Speech API recognition.
    """
    data = request.get_json() or {}
    text = data.get('text', '').strip()
    language = data.get('language', 'en')

    if not text:
        return jsonify({
            'status': 'ready',
            'message': 'Send audio or recognized speech transcript.',
            'supported_languages': ['en-IN', 'kn-IN', 'hi-IN']
        }), 200

    return jsonify({
        'status': 'success',
        'transcribed_text': text,
        'language': language
    }), 200

@voice_bp.route('/speak', methods=['POST'])
def speak():
    """
    Multilingual text-to-speech configuration endpoint.
    Guides client-side speech synthesis parameters for regional pronunciation.
    """
    data = request.get_json() or {}
    text = data.get('text', '').strip()
    language = data.get('language', 'en')

    lang_map = {
        'kn': {'lang_code': 'kn-IN', 'pitch': 1.0, 'rate': 0.9, 'name': 'Kannada Voice'},
        'hi': {'lang_code': 'hi-IN', 'pitch': 1.0, 'rate': 0.95, 'name': 'Hindi Voice'},
        'en': {'lang_code': 'en-IN', 'pitch': 1.0, 'rate': 1.0, 'name': 'Indian English Voice'}
    }

    voice_profile = lang_map.get(language, lang_map['en'])

    return jsonify({
        'status': 'ready',
        'text': text,
        'voice_profile': voice_profile
    }), 200
