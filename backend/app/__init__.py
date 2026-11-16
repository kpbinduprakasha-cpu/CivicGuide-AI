import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from .models import db
from .utils.seed_data import seed_database

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    # Initialize database
    db.init_app(app)

    # Register API Blueprints
    from .routes.auth_routes import auth_bp
    from .routes.chat_routes import chat_bp
    from .routes.scheme_routes import scheme_bp
    from .routes.eligibility_routes import eligibility_bp
    from .routes.public_service_routes import public_service_bp
    from .routes.document_routes import document_bp
    from .routes.voice_routes import voice_bp
    from .routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(scheme_bp)
    app.register_blueprint(eligibility_bp)
    app.register_blueprint(public_service_bp)
    app.register_blueprint(document_bp)
    app.register_blueprint(voice_bp)
    app.register_blueprint(admin_bp)

    # Global JSON error handlers
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({'error': 'Bad Request', 'message': str(e)}), 400

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Not Found', 'message': 'The requested resource was not found on this server.'}), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify({'error': 'Internal Server Error', 'message': 'An unexpected server error occurred.'}), 500

    # Auto seed initial verified data
    with app.app_context():
        try:
            seed_database(app)
        except Exception as e:
            print(f"[App Init] Seed warning: {e}")

    return app
