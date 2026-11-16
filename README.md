# CivicGuide AI – Multilingual Policy, Rights & Government Scheme Explainer

<p align="center">
  <b>Empowering Indian Citizens with Simple, Verified Regional Language Explanations</b><br>
  <i>Coverage: All India (Central Government, States & Union Territories)</i>
</p>

---

## 🏛️ Project Overview
**CivicGuide AI** is a full-stack, production-ready AI web application built to help Indian citizens across all 28 States, 8 Union Territories, and the Central Government understand welfare schemes, public policies, citizen rights, and public administrative services. It includes specialized local taluk-level mapping for Karnataka (covering all 6 taluks of Vijayanagara District).

The application supports three languages:
1. **English**
2. **Kannada (ಕನ್ನಡ)**
3. **Hindi (हिन्दी)**

---

## 🌟 Key Features

1. **Authentication & User Privacy**:
   - Opening login page with logo, show/hide password, remember me, forgot password, and registration links.
   - Separate accounts for every citizen with encrypted password storage (`werkzeug.security`).
   - Guest browsing access to public government schemes.
   - Private conversation history per user; users cannot access another user's data.
   - Option to clear private chat history at any time.

2. **AI Chatbot with Local Ollama & RAG**:
   - Connects to local **Ollama** running a **Qwen** model (`qwen2.5:latest` / `qwen2:1.5b`).
   - Graceful offline fallback: If Ollama is offline or model is missing, the system utilizes a high-accuracy, verified **RAG Knowledge Engine** powered by official government documents.
   - Displays citations, issuing authorities, publication dates, and official government portal links.
   - Multilingual voice input (Microphone speech-to-text) and voice output (Text-to-speech read aloud).

3. **Government Schemes Directory (Central & State Initiatives)**:
   - Comprehensive directory of Central Government initiatives (PM-Kisan, Ayushman Bharat PM-JAY, PM Surya Ghar: Muft Bijli Yojana, PM Vishwakarma, Pradhan Mantri Mudra Yojana, Sukanya Samriddhi Yojana, Atal Pension Yojana, National Scholarship Portal, Kisan Credit Card) and State schemes (Gruha Lakshmi, Yuva Nidhi, Gruha Jyothi, Shakti, SSP Scholarships, Majhi Ladki Bahin Yojana, Delhi Lifeline Water & Electricity).
   - Filter by categories: Education, Agriculture, Healthcare, Employment, Housing, Women & Child Welfare, Financial Assistance, Social Welfare.
   - Filter by State or Central government level.

4. **AI Eligibility Checker**:
   - Interactive screening tool evaluating age, income, ration card category (BPL/AAY/APL), occupation, gender, state, and district.
   - Evaluates across Central and State schemes.
   - Provides broken-down satisfied vs unmet conditions, required documents, and official application portals.
   - Explicit disclaimer explaining that final approval belongs to the competent government department.

5. **All India Interactive Map & Public Services Directory**:
   - Built with **React Leaflet** and **OpenStreetMap**.
   - Covers Central Government ministries & offices (New Delhi, North Block, NITI Aayog), AIIMS & Apex Hospitals, Passport Seva Kendras, State Secretariats, District Collectorates, and Common Service Centres (CSCs).
   - In-depth taluk breakdown for Karnataka (Hosapete, Harapanahalli, Kudligi, Huvina Hadagali, Hagaribommanahalli, Kottur).
   - Filter by State/UT, Jurisdiction Level (`Central Government` vs `State Government`), Service Category, and Taluk.
   - Popups with addresses, verified phone numbers, and one-click OpenStreetMap directions.

6. **Admin Dashboard (RBAC)**:
   - Dedicated administrator portal.
   - Manage government schemes (Add, edit, delete).
   - Manage public service locations with GPS coordinates.
   - Upload government PDF/text documents; automatically vectorized and indexed into ChromaDB.
   - View registered users and audit system analytics.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React 19, Vite, Tailwind CSS v4, React Router v7, Axios, Lucide React icons |
| **Map** | React Leaflet, Leaflet, OpenStreetMap |
| **Voice** | Web Speech API (SpeechRecognition & SpeechSynthesis for Kannada, Hindi, English) |
| **Backend** | Python 3.14, Flask, Flask-CORS, SQLAlchemy, itsdangerous, Werkzeug |
| **Database** | SQLite (`database/civicguide.db`) |
| **AI / RAG** | Ollama local AI (Qwen model), ChromaDB, scikit-learn TF-IDF, pypdf |

---

## 🚀 Quick Start Guide (Windows)

### 1. Prerequisites
Ensure you have the following installed on Windows:
- **Node.js** (v18 or higher)
- **Python** (3.10 to 3.14)
- **Ollama** (Optional for live LLM; download from [ollama.com](https://ollama.com))

---

### 2. Run the Backend (Flask & SQLite)

Open a PowerShell or Command Prompt terminal in the project root:

```powershell
# Navigate to project directory
cd "c:\Users\Lenovo\OneDrive\Desktop\CivicGuide AI"

# Install backend dependencies (if not already installed)
python -m pip install -r backend/requirements.txt

# Start the Flask backend server
python backend/run.py
```

*The backend starts at `http://127.0.0.1:5000` and automatically initializes the SQLite database and seeds verified schemes, public services, and RAG document vectors.*

---

### 3. Run the Frontend (React + Vite)

Open a second terminal window:

```powershell
cd "c:\Users\Lenovo\OneDrive\Desktop\CivicGuide AI\frontend"

# Install npm dependencies (if not already installed)
npm install

# Start Vite development server
npm run dev
```

*The frontend starts at `http://localhost:5173`.*

Open your web browser and navigate to:
👉 **`http://localhost:5173`**

---

### 4. Optional: Run Local Ollama with Qwen

To activate live local Qwen LLM responses:

```powershell
# In a separate terminal or background
ollama run qwen2.5:latest
# or lightweight version:
ollama run qwen2:1.5b
```

> **Note**: If Ollama is not running, CivicGuide AI automatically detects this and seamlessly answers using its verified RAG knowledge base from official government gazettes, ensuring zero downtime!

---

## 🔑 Pre-Seeded Demonstration Accounts

For college project evaluation and testing, the application includes pre-seeded accounts:

| Role | Username | Password | Email | Description |
|---|---|---|---|---|
| **Citizen (User)** | `citizen` | `Citizen@2026` | `citizen@civicguide.gov.in` | Standard citizen account with private chat history |
| **Administrator** | `admin` | `Admin@CivicGuide2026` | `admin@civicguide.gov.in` | Full access to Admin Console, Scheme & Service management |

---

## 🧪 Running Automated Tests

A comprehensive unit test suite is included in `tests/test_backend.py`. Run it with:

```powershell
python tests/test_backend.py
```

Tests cover:
- Citizen registration, field validation, duplicate detection, and login
- Government scheme directory and category filters
- Vijayanagara 6 taluks public services verification
- Scheme eligibility screening engine (e.g., Gruha Lakshmi, Yuva Nidhi)
- AI Chatbot RAG context retrieval
- Role-based access control (RBAC) security

---

## 📂 Project Directory Structure

```
CivicGuide-AI/
├── backend/
│   ├── app/
│   │   ├── ai/               # Ollama client and RAG synthesis
│   │   ├── auth/             # Token generator and @login_required decorators
│   │   ├── models/           # SQLAlchemy User, Scheme, Service, Chat, Document
│   │   ├── rag/              # Document processor & ChromaDB vector store
│   │   ├── routes/           # REST API endpoints (auth, chat, schemes, services, etc.)
│   │   ├── services/         # Eligibility criteria engine
│   │   └── utils/            # Database seeder (Vijayanagara data & schemes)
│   ├── config.py             # Environment configurations
│   ├── requirements.txt      # Python dependencies
│   └── run.py                # Flask server entry point
├── database/                 # SQLite database & ChromaDB store
├── documents/                # Verified government policy documents for RAG
├── frontend/
│   ├── src/
│   │   ├── components/       # Navbar, Footer, LanguageSelector, VoiceButton
│   │   ├── context/          # AuthContext, LanguageContext (en, kn, hi)
│   │   ├── pages/            # 14 distinct pages (Home, Login, Schemes, Chat, Map, etc.)
│   │   ├── services/         # Axios API service
│   │   ├── App.jsx           # React Router and layout
│   │   └── main.jsx          # React DOM entry
│   ├── package.json
│   └── vite.config.js
├── tests/                    # Automated test suite
├── .env.example              # Environment variables template
├── .gitignore
├── README.md                 # Full documentation
└── SPEC.md                   # Technical specification
```

---

## 📜 Official Citations & Data Sources
- **Karnataka State Portals**: [Seva Sindhu](https://sevasindhugs.karnataka.gov.in), [Nadakacheri](https://nadakacheri.karnataka.gov.in), [SSP Karnataka](https://ssp.postmatric.karnataka.gov.in).
- **Central Government Portals**: [PM-Kisan](https://pmkisan.gov.in), [Ayushman Bharat PM-JAY](https://pmjay.gov.in), [PMAY-Gramin](https://pmayg.nic.in).
- **District Administration**: [Vijayanagara District Administration, Hosapete](https://vijayanagara.nic.in).
- **Cartography**: OpenStreetMap contributors.

---

## 🎓 Academic Project Credit
Developed as a B.Tech Artificial Intelligence & Data Science capstone project demonstration.
