from flask import Blueprint, request, jsonify, g
from ..models import db, User, Scheme, PublicService, Document, ChatHistory
from ..auth.jwt_auth import admin_required
from ..ai.ollama_client import ollama_client
from ..rag.rag_engine import rag_engine

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/stats', methods=['GET'])
@admin_required
def get_stats():
    total_users = User.query.count()
    total_schemes = Scheme.query.count()
    total_services = PublicService.query.count()
    total_documents = Document.query.count()
    total_chats = ChatHistory.query.count()

    ollama_info = ollama_client.check_availability()

    return jsonify({
        'users_count': total_users,
        'schemes_count': total_schemes,
        'services_count': total_services,
        'documents_count': total_documents,
        'chat_queries_count': total_chats,
        'rag_chunks_count': len(rag_engine.chunks),
        'ollama_status': ollama_info
    }), 200

@admin_bp.route('/users', methods=['GET'])
@admin_required
def list_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return jsonify({
        'count': len(users),
        'users': [u.to_dict() for u in users]
    }), 200

@admin_bp.route('/users/<int:user_id>/role', methods=['PUT'])
@admin_required
def update_user_role(user_id):
    data = request.get_json() or {}
    new_role = data.get('role')

    if new_role not in ['user', 'admin']:
        return jsonify({'error': "Role must be 'user' or 'admin'."}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found.'}), 404

    # Prevent admin from de-ranking themselves if they are the only admin
    if user.id == g.current_user.id and new_role != 'admin':
        admin_count = User.query.filter_by(role='admin').count()
        if admin_count <= 1:
            return jsonify({'error': 'Cannot change role: You are the sole administrator.'}), 400

    user.role = new_role
    db.session.commit()

    return jsonify({
        'message': f"User '{user.username}' role updated to '{new_role}'.",
        'user': user.to_dict()
    }), 200
