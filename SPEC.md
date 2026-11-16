# CivicGuide AI — Architectural Specification (SPEC.md)

## 1. System Overview
**CivicGuide AI** is an intelligent, multilingual web application built to explain Indian government schemes, policies, citizen rights, and public services in simple regional languages (**Kannada, English, and Hindi**).
The application covers **All India** (Central Government initiatives across all 28 States and 8 Union Territories) alongside comprehensive district and taluk mapping for Karnataka (including all 6 taluks of Vijayanagara District: Hosapete, Harapanahalli, Kudligi, Huvina Hadagali, Hagaribommanahalli, and Kottur).

---

## 2. Technology Stack
- **Frontend**: React 19, Vite, Tailwind CSS v4, React Router v7, Axios, Lucide React icons, React Leaflet, OpenStreetMap.
- **Backend**: Python 3.14, Flask, Flask-CORS, SQLAlchemy, itsdangerous cryptographic token serializer, Werkzeug security.
- **Database**: SQLite (ACID compliant, relational schema, zero external database installation needed).
- **AI & RAG Engine**: 
  - Local Ollama AI client interfacing `http://localhost:11434/api/generate` with configurable Qwen models (`qwen2.5:latest` / `qwen2:1.5b`).
  - ChromaDB persistent vector database with ONNX embeddings + fallback TF-IDF vectorizer.
  - PDF & document extractor using `pypdf`.
  - Zero-hallucination RAG workflow: Retrieves verified policy documents and cites official portals.
- **Voice Interactivity**: Web Speech API (`SpeechRecognition` with `kn-IN`, `hi-IN`, `en-IN` support and `SpeechSynthesis` for audio answers).

---

## 3. Database Schema

### `users` Table
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY | Unique citizen ID |
| `full_name` | VARCHAR(150) | NOT NULL | Citizen full name |
| `email` | VARCHAR(150) | UNIQUE, NOT NULL | Unique contact email |
| `username` | VARCHAR(100) | UNIQUE, NOT NULL | Login handle |
| `password_hash` | VARCHAR(255) | NOT NULL | Werkzeug scrypt/pbkdf2 hash |
| `role` | VARCHAR(20) | DEFAULT 'user' | Access role: 'user' or 'admin' |
| `preferred_language` | VARCHAR(10) | DEFAULT 'en' | 'en', 'kn', 'hi' |
| `created_at` | DATETIME | DEFAULT utcnow | Account registration date |
| `reset_token` | VARCHAR(100) | NULLABLE | Secure password reset token |
| `reset_token_expiry`| DATETIME | NULLABLE | Token expiration timestamp |

### `schemes` Table
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY | Unique scheme ID |
| `name` | VARCHAR(250) | NOT NULL | Scheme name in English |
| `name_kn` | VARCHAR(250) | NULLABLE | Scheme name in Kannada |
| `name_hi` | VARCHAR(250) | NULLABLE | Scheme name in Hindi |
| `description` | TEXT | NOT NULL | Comprehensive overview |
| `category` | VARCHAR(100) | NOT NULL | Category (e.g. Women and child welfare, Agriculture, etc.) |
| `eligibility` | TEXT | NOT NULL | Criteria and norms |
| `benefits` | TEXT | NOT NULL | Direct cash or material benefits |
| `required_documents`| TEXT | NOT NULL | Documents checklist |
| `application_process`| TEXT | NOT NULL | Step-by-step application procedure |
| `official_url` | VARCHAR(350) | NOT NULL | Verified government URL |
| `government_level` | VARCHAR(50) | NOT NULL | 'Central Government', 'Karnataka State', 'State Government' |
| `source_date` | VARCHAR(50) | NULLABLE | Gazette/Order validity date |
| `verified` | BOOLEAN | DEFAULT TRUE | Official verification badge |

### `public_services` Table
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY | Unique location ID |
| `name` | VARCHAR(250) | NOT NULL | Office / Hospital / College name |
| `name_kn` | VARCHAR(250) | NULLABLE | Service name in Kannada |
| `name_hi` | VARCHAR(250) | NULLABLE | Service name in Hindi |
| `category` | VARCHAR(100) | NOT NULL | Ministries, AIIMS, PSK, Collectorates, CSCs, etc. |
| `state` | VARCHAR(100) | NOT NULL | Delhi, Karnataka, Maharashtra, Tamil Nadu, etc. |
| `district_city` | VARCHAR(100) | NOT NULL | New Delhi, Bengaluru, Mumbai, Vijayanagara, etc. |
| `taluk` | VARCHAR(100) | NULLABLE | Hosapete, Harapanahalli, Kudligi, Hadagali, etc. |
| `government_level` | VARCHAR(50) | NOT NULL | 'Central Government' or 'State Government' |
| `address` | TEXT | NOT NULL | Verified postal address |
| `latitude` | FLOAT | NOT NULL | GPS Latitude |
| `longitude` | FLOAT | NOT NULL | GPS Longitude |
| `phone` | VARCHAR(100) | NULLABLE | Office helpline / phone |
| `official_url` | VARCHAR(350) | NULLABLE | Portal link |
| `verified` | BOOLEAN | DEFAULT TRUE | Confirmed location status |

### `chat_histories` Table
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY | Interaction ID |
| `user_id` | INTEGER | FOREIGN KEY (users.id) | Private to specific citizen |
| `question` | TEXT | NOT NULL | Citizen question |
| `answer` | TEXT | NOT NULL | AI response |
| `language` | VARCHAR(10) | NOT NULL | 'en', 'kn', 'hi' |
| `sources` | TEXT | JSON | Cited official document references |
| `created_at` | DATETIME | DEFAULT utcnow | Timestamp |

### `documents` Table
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY | Document ID |
| `title` | VARCHAR(250) | NOT NULL | Policy title |
| `file_path` | VARCHAR(350) | NOT NULL | Physical disk path |
| `source_url` | VARCHAR(350) | NULLABLE | Official portal reference |
| `authority` | VARCHAR(150) | NULLABLE | Issuing department / Ministry |
| `publication_date` | VARCHAR(50) | NULLABLE | Publication year / date |
| `jurisdiction` | VARCHAR(100) | NOT NULL | Jurisdiction level |
| `chunk_count` | INTEGER | DEFAULT 0 | Vector chunks in RAG |

---

## 4. API Endpoints Reference

### Authentication
- `POST /api/auth/register` — Independent citizen account registration with field validation.
- `POST /api/auth/login` — Authentication with secure token return.
- `POST /api/auth/logout` — Invalidate session.
- `GET /api/auth/me` — Protected profile retrieval.
- `PUT /api/auth/profile` — Update name or preferred language.
- `POST /api/auth/forgot-password` — Password reset token generator.
- `POST /api/auth/reset-password` — Password update using verified token.

### AI Chatbot & RAG
- `POST /api/chat` — Question answering with RAG retrieval from verified documents and local Ollama Qwen integration.
- `GET /api/chat/history` — Get user's private history (authenticated).
- `DELETE /api/chat/history` — Securely clear user's history.
- `GET /api/chat/status` — Returns Ollama availability and RAG index health.

### Government Schemes
- `GET /api/schemes` — Filterable by search keyword, category, jurisdiction, and language.
- `GET /api/schemes/:id` — Full scheme details with documents and procedure.
- `POST /api/schemes` — [Admin] Add new scheme.
- `PUT /api/schemes/:id` — [Admin] Update scheme.
- `DELETE /api/schemes/:id` — [Admin] Remove scheme.

### Scheme Eligibility Screener
- `POST /api/eligibility/check` — Evaluates age, income, ration card, gender, occupation, and state/district against Central & State criteria.

### Public Services & Map
- `GET /api/public-services` — List verified services filtered by `state`, `level` ('Central Government' / 'State Government'), `category`, `taluk`, or search query.
- `GET /api/public-services/states` — Return counts for Central Government and all States/UTs across India.
- `GET /api/public-services/nearby` — Haversine nearest service lookup based on GPS coordinates.
- `GET /api/public-services/taluks` — Returns Karnataka taluks and counts.
- `POST /api/public-services` — [Admin] Add new service location.
- `PUT /api/public-services/:id` — [Admin] Update service.
- `DELETE /api/public-services/:id` — [Admin] Delete service.

### Administration & RAG Ingestion
- `GET /api/admin/stats` — [Admin] System-wide analytics.
- `GET /api/admin/users` — [Admin] User audit list.
- `PUT /api/admin/users/:id/role` — [Admin] Role modification.
- `POST /api/documents/upload` — [Admin] Upload PDF/TXT, extracts text, chunks, and indexes into ChromaDB.
- `GET /api/documents` — List indexed RAG documents.
- `DELETE /api/documents/:id` — [Admin] Remove document from RAG index.
