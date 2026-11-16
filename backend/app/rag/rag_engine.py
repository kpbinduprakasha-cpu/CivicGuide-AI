import os
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .document_processor import extract_text_from_file, chunk_text

class RAGEngine:
    def __init__(self, persist_dir=None):
        self.persist_dir = persist_dir or os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'chroma_store')
        os.makedirs(self.persist_dir, exist_ok=True)
        
        self.chunks = [] # List of dicts: {'id': ..., 'text': ..., 'metadata': ...}
        self.chroma_client = None
        self.chroma_collection = None
        self.vectorizer = None
        self.tfidf_matrix = None
        
        self._init_chroma()
        self._load_cached_chunks()

    def _init_chroma(self):
        try:
            import chromadb
            from chromadb.config import Settings
            self.chroma_client = chromadb.PersistentClient(path=self.persist_dir)
            self.chroma_collection = self.chroma_client.get_or_create_collection(
                name="civic_documents",
                metadata={"description": "CivicGuide AI verified government policy and services knowledge base"}
            )
            print("[RAG] ChromaDB initialized successfully.")
        except Exception as e:
            print(f"[RAG] ChromaDB initialization note: {e}. Using resilient TF-IDF Vector Engine.")
            self.chroma_client = None
            self.chroma_collection = None

    def _load_cached_chunks(self):
        cache_path = os.path.join(self.persist_dir, 'chunks_cache.json')
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    self.chunks = json.load(f)
                self._update_tfidf_index()
                print(f"[RAG] Loaded {len(self.chunks)} verified chunks from cache.")
            except Exception as e:
                print(f"[RAG] Error loading chunks cache: {e}")

    def _save_cached_chunks(self):
        cache_path = os.path.join(self.persist_dir, 'chunks_cache.json')
        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(self.chunks, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[RAG] Error saving chunks cache: {e}")

    def _update_tfidf_index(self):
        if not self.chunks:
            self.vectorizer = None
            self.tfidf_matrix = None
            return
        
        corpus = [c['text'] for c in self.chunks]
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english')
        try:
            self.tfidf_matrix = self.vectorizer.fit_transform(corpus)
        except Exception as e:
            print(f"[RAG] Error fitting TF-IDF: {e}")

    def ingest_document(self, doc_id, title, file_path, authority="", source_url="", publication_date="", jurisdiction="Karnataka / Vijayanagara District"):
        """Extract, chunk, embed, and store document in vector stores."""
        text = extract_text_from_file(file_path)
        if not text:
            return 0
        
        raw_chunks = chunk_text(text)
        new_chunks = []
        
        for idx, chunk in enumerate(raw_chunks):
            chunk_id = f"doc_{doc_id}_chunk_{idx}"
            metadata = {
                'doc_id': str(doc_id),
                'title': title,
                'authority': authority,
                'source_url': source_url,
                'publication_date': publication_date,
                'jurisdiction': jurisdiction,
                'chunk_index': idx
            }
            
            chunk_obj = {
                'id': chunk_id,
                'text': chunk,
                'metadata': metadata
            }
            new_chunks.append(chunk_obj)
            
            # Store into ChromaDB if available
            if self.chroma_collection:
                try:
                    self.chroma_collection.upsert(
                        ids=[chunk_id],
                        documents=[chunk],
                        metadatas=[metadata]
                    )
                except Exception as e:
                    print(f"[RAG] ChromaDB upsert error: {e}")
                    
        # Add to local index and save
        self.chunks.extend(new_chunks)
        self._save_cached_chunks()
        self._update_tfidf_index()
        return len(new_chunks)

    def retrieve(self, query, top_k=4):
        """Retrieve the most relevant verified document passages for a user query."""
        if not self.chunks:
            return []
        
        results = []
        
        # Try ChromaDB query first
        if self.chroma_collection:
            try:
                chroma_results = self.chroma_collection.query(
                    query_texts=[query],
                    n_results=min(top_k, len(self.chunks))
                )
                if chroma_results and chroma_results.get('documents') and chroma_results['documents'][0]:
                    docs = chroma_results['documents'][0]
                    metas = chroma_results['metadatas'][0]
                    distances = chroma_results.get('distances', [[0]*len(docs)])[0]
                    
                    for doc_text, meta, dist in zip(docs, metas, distances):
                        results.append({
                            'text': doc_text,
                            'title': meta.get('title', 'Official Government Document'),
                            'authority': meta.get('authority', 'Government of Karnataka / India'),
                            'source_url': meta.get('source_url', 'https://karnataka.gov.in'),
                            'publication_date': meta.get('publication_date', '2024-2026'),
                            'jurisdiction': meta.get('jurisdiction', 'Karnataka / Vijayanagara'),
                            'score': float(1.0 / (1.0 + dist)) if dist is not None else 0.85
                        })
                    return results
            except Exception as e:
                print(f"[RAG] ChromaDB query fallback to TF-IDF: {e}")

        # Resilient TF-IDF retrieval fallback
        if self.vectorizer and self.tfidf_matrix is not None:
            try:
                query_vec = self.vectorizer.transform([query])
                similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
                
                # Top k indices
                top_indices = np.argsort(similarities)[::-1][:top_k]
                for idx in top_indices:
                    score = float(similarities[idx])
                    if score > 0.05 or len(results) == 0: # Threshold or best match
                        chunk = self.chunks[idx]
                        meta = chunk['metadata']
                        results.append({
                            'text': chunk['text'],
                            'title': meta.get('title', 'Official Government Document'),
                            'authority': meta.get('authority', 'Government of Karnataka / India'),
                            'source_url': meta.get('source_url', 'https://karnataka.gov.in'),
                            'publication_date': meta.get('publication_date', '2024-2026'),
                            'jurisdiction': meta.get('jurisdiction', 'Karnataka / Vijayanagara'),
                            'score': round(score, 4)
                        })
            except Exception as e:
                print(f"[RAG] TF-IDF query error: {e}")

        return results

    def clear(self):
        self.chunks = []
        if self.chroma_collection:
            try:
                self.chroma_client.delete_collection("civic_documents")
                self.chroma_collection = self.chroma_client.create_collection("civic_documents")
            except Exception:
                pass
        self._save_cached_chunks()
        self._update_tfidf_index()

# Singleton instance
rag_engine = RAGEngine()
