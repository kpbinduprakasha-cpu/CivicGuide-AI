import os
from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify, current_app, g
from ..models import db, Document
from ..auth.jwt_auth import admin_required
from ..rag.rag_engine import rag_engine

document_bp = Blueprint('documents', __name__, url_prefix='/api/documents')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@document_bp.route('', methods=['GET'])
def list_documents():
    docs = Document.query.order_by(Document.uploaded_at.desc()).all()
    return jsonify({
        'count': len(docs),
        'documents': [d.to_dict() for d in docs]
    }), 200

@document_bp.route('/upload', methods=['POST'])
@admin_required
def upload_document():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request.'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading.'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Only PDF, TXT, and Markdown (.md) documents are allowed.'}), 400

    title = request.form.get('title', '').strip() or os.path.splitext(file.filename)[0].replace('_', ' ').title()
    authority = request.form.get('authority', 'Government of Karnataka / India').strip()
    source_url = request.form.get('source_url', 'https://karnataka.gov.in').strip()
    publication_date = request.form.get('publication_date', '2024-2026').strip()
    jurisdiction = request.form.get('jurisdiction', 'Karnataka / Vijayanagara District').strip()

    # Save to documents dir
    docs_dir = current_app.config['DOCUMENTS_DIR']
    os.makedirs(docs_dir, exist_ok=True)
    
    filename = secure_filename(file.filename)
    dest_path = os.path.join(docs_dir, filename)
    file.save(dest_path)

    # Create DB entry
    doc_record = Document(
        title=title,
        file_path=dest_path,
        source_url=source_url,
        authority=authority,
        publication_date=publication_date,
        jurisdiction=jurisdiction,
        verified=True
    )
    db.session.add(doc_record)
    db.session.flush()

    # Ingest into RAG vector engine
    chunk_count = rag_engine.ingest_document(
        doc_id=doc_record.id,
        title=doc_record.title,
        file_path=dest_path,
        authority=doc_record.authority,
        source_url=doc_record.source_url,
        publication_date=doc_record.publication_date,
        jurisdiction=doc_record.jurisdiction
    )
    doc_record.chunk_count = chunk_count
    db.session.commit()

    return jsonify({
        'message': f"Document '{title}' uploaded and indexed successfully into RAG.",
        'document': doc_record.to_dict(),
        'chunks_created': chunk_count
    }), 201

@document_bp.route('/<int:doc_id>', methods=['DELETE'])
@admin_required
def delete_document(doc_id):
    doc = Document.query.get(doc_id)
    if not doc:
        return jsonify({'error': 'Document record not found.'}), 404

    # Remove physical file if safe
    if os.path.exists(doc.file_path):
        try:
            os.remove(doc.file_path)
        except Exception:
            pass

    db.session.delete(doc)
    db.session.commit()

    return jsonify({
        'message': f"Document '{doc.title}' removed from database."
    }), 200
