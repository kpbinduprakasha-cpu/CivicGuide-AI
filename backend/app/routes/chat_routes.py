import json
from flask import Blueprint, request, jsonify, g
from ..models import db, ChatHistory
from ..auth.jwt_auth import login_required, optional_login
from ..ai.ollama_client import ollama_client
from ..rag.rag_engine import rag_engine

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')

@chat_bp.route('', methods=['POST'])
@optional_login
def chat():
    data = request.get_json() or {}
    question = data.get('question', '').strip()
    language = data.get('language', 'en').strip().lower()

    if not question:
        return jsonify({'error': 'Please provide a question.'}), 400

    if g.current_user and not language:
        language = 'en'
    if not language:
        language = 'en'

    # Generate answer with RAG + Ollama Qwen
    result = ollama_client.generate_response(user_question=question, language=language)
    
    chat_record = None
    # If user is authenticated, securely save history for this user
    if g.current_user:
        chat_record = ChatHistory(
            user_id=g.current_user.id,
            question=question,
            answer=result['answer'],
            language=language,
            sources=json.dumps(result['sources'], ensure_ascii=False)
        )
        db.session.add(chat_record)
        db.session.commit()

    return jsonify({
        'question': question,
        'answer': result['answer'],
        'sources': result['sources'],
        'ai_provider': result.get('ai_provider'),
        'model_status': result.get('model_status'),
        'ollama_notice': result.get('ollama_notice'),
        'language': language,
        'saved': bool(g.current_user),
        'chat_id': chat_record.id if chat_record else None
    }), 200

@chat_bp.route('/history', methods=['GET'])
@login_required
def get_chat_history():
    # Only return chat history belonging strictly to current logged in user
    history = ChatHistory.query.filter_by(user_id=g.current_user.id)\
                               .order_by(ChatHistory.created_at.desc())\
                               .limit(50)\
                               .all()
    return jsonify({
        'history': [item.to_dict() for item in history]
    }), 200

@chat_bp.route('/history', methods=['DELETE'])
@login_required
def clear_chat_history():
    # Delete only current user's history
    deleted_count = ChatHistory.query.filter_by(user_id=g.current_user.id).delete()
    db.session.commit()
    return jsonify({
        'message': 'Your conversation history has been cleared securely.',
        'deleted_count': deleted_count
    }), 200

@chat_bp.route('/status', methods=['GET'])
def get_ai_status():
    ollama_info = ollama_client.check_availability()
    rag_count = len(rag_engine.chunks)
    return jsonify({
        'ollama': ollama_info,
        'rag_indexed_chunks': rag_count,
        'vector_store': 'ChromaDB' if rag_engine.chroma_collection else 'TF-IDF Hybrid'
    }), 200
