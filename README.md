# CivicGuide AI – Multilingual Policy, Rights & Government Scheme Explainer
### Secure User Registration, Email OTP Verification & Citizen Identity Portal

<p align="center">
  <b>Empowering Indian Citizens with Verified Regional Language Explanations, Secure Identity, and Instant Eligibility</b><br>
  <i>Coverage: All India (Central Government, 28 States & 8 Union Territories) with Local Mapping for Vijayanagara District</i>
</p>

---

## 🏛️ Project Overview

**CivicGuide AI** is a complete, full-stack, production-grade web application built to help Indian citizens understand welfare schemes, public policies, citizen rights, and government administrative services.

It features a **bank-grade secure registration and authentication system** designed according to strict citizen verification guidelines:
1. **Welcome Page**: Modern landing page with **Create Account** and **Login** entry points in a blue, purple, and white responsive design.
2. **One-Time Registration Form**: Collects 9 personal attributes (Full Name, Age, Mobile Number, State, Sex, Languages Known, Email Address, Password, Confirm Password).
3. **Automated Unique User ID Generation**: Auto-generates a clean, unique alphanumeric User ID derived from the citizen's registered name (e.g. *Rahul Kumar* → `@rahul123`) used for all future logins.
4. **Compulsory Email OTP Verification**: Dispatches a 6-digit OTP code to the citizen's email address with a 60-second cooldown resend timer and 5-minute expiry. Accounts cannot log in before email verification.
5. **Streamlined Returning Citizen Login**: Returning citizens sign in using only their **User ID** and **Password** (no repeated OTP required on regular logins).
6. **Self-Service Password Recovery**: Secure 6-digit password reset OTP workflow to the registered email address.
7. **Personal Citizen Dashboard**: Displays complete citizen profile (User ID, Name, Email, Age, Mobile, State, Sex, Languages, Verification Status, Creation Date), Edit Profile, Change Password, and Logout.

---

## 🔐 Authentication & Identity Architecture

```
                       ┌────────────────────────┐
                       │   1. Welcome Page      │
                       │ [Create Account][Login]│
                       └───────────┬────────────┘
                                   │
              ┌────────────────────┴────────────────────┐
              ▼                                         ▼
   ┌──────────────────────┐                  ┌──────────────────────┐
   │ 2. Registration Form │                  │ 4. Returning Login   │
   │  - 9 Citizen Fields  │                  │  - User ID (@rahul123)│
   │  - Auto User ID Gen  │                  │  - Password          │
   └──────────┬───────────┘                  └──────────┬───────────┘
              │                                         │
              ▼                                         ▼
   ┌──────────────────────┐                  ┌──────────────────────┐
   │ 3. Email OTP Screen  │                  │ 6. Citizen Dashboard │
   │  - 6-Digit Code      │                  │  - Profile Details   │
   │  - 60s Resend Timer  │──────Verified───▶│  - Edit Profile      │
   │  - 5-Min Expiration  │                  │  - Change Password   │
   └──────────────────────┘                  │  - Welfare & Services│
                                             └──────────────────────┘
```

### Registration Fields (9 Required Attributes)
1. **Full Name** (e.g. Rahul Kumar)
2. **Age** (Validated 1 to 120)
3. **Mobile Number** (10-digit Indian phone number)
4. **State / UT** (Dropdown with all 36 Indian States and Union Territories)
5. **Sex** (Male / Female / Other / Prefer not to say)
6. **Languages Known** (Multi-select interactive pills: English, Kannada, Hindi, Telugu, Tamil, Marathi, Bengali, Gujarati, Malayalam, Urdu, Punjabi, Odia)
7. **Email Address** (Compulsory OTP destination)
8. **Password** (Minimum 8 characters with strength indicator)
9. **Confirm Password** (Real-time match check)

---

## 🌟 Key Application Features

1. **Multilingual AI Policy Chatbot**:
   - Integrated with local **Ollama** running a **Qwen** model (`qwen2.5:latest` / `qwen2:1.5b`).
   - High-precision offline RAG fallback using official gazettes when Ollama is offline.
   - Multilingual voice input (Speech-to-text) and speech synthesis (Text-to-speech) in Kannada, Hindi, and English.
   - Direct citations, issuing authorities, and official portal links.

2. **National & State Welfare Schemes Directory**:
   - Central schemes: PM-Kisan, Ayushman Bharat PM-JAY, PM Surya Ghar: Muft Bijli Yojana, PM Vishwakarma, Pradhan Mantri Mudra Yojana, Sukanya Samriddhi Yojana, Atal Pension Yojana, NSP, KCC.
   - State schemes: Karnataka Gruha Lakshmi, Yuva Nidhi, Gruha Jyothi, Shakti, SSP Scholarships, Majhi Ladki Bahin, etc.
   - Filter by categories: Education, Agriculture, Healthcare, Employment, Housing, Women & Child Welfare, Financial Assistance.

3. **AI Eligibility Screening Engine**:
   - Interactive screening tool evaluating age, income, ration card category (BPL/AAY/APL), occupation, gender, state, and district.
   - Detailed breakdown of satisfied vs unmet criteria, required documents, and official application portals.

4. **All India Interactive Map & Public Services Directory**:
   - Built with **React Leaflet** and **OpenStreetMap**.
   - Covers Central ministries, Apex hospitals (AIIMS), Passport Seva Kendras, State Secretariats, District Collectorates, and Common Service Centres (CSCs).
   - In-depth taluk breakdown for Vijayanagara District (Hosapete, Harapanahalli, Kudligi, Huvina Hadagali, Hagaribommanahalli, Kottur).

5. **Administrator Console (RBAC)**:
   - Dedicated admin portal at `/admin/login` and `/admin`.
   - Manage government schemes (Add, edit, delete).
   - Manage public service coordinates with GPS verification.
   - Upload government PDF/text documents for automated vectorization into ChromaDB.
   - Audit registered citizen profiles.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React 19, Vite, Tailwind CSS v4, React Router v7, Axios, Lucide React icons |
| **Backend** | Python 3.14 / 3.11, Flask, Flask-CORS, SQLAlchemy, itsdangerous, Werkzeug |
| **Authentication** | Werkzeug secure password hashing, JWT Bearer tokens, 6-digit OTP verification |
| **Email Service** | SMTP (Gmail SMTP with App Password) + Dev fallback logging to `database/dev_otp_inbox.json` |
| **Database** | SQLite (`database/civicguide.db`) for development, PostgreSQL-ready for production |
| **AI / RAG** | Ollama local AI (Qwen model), ChromaDB, scikit-learn TF-IDF, pypdf |
| **Interactive Map** | React Leaflet, Leaflet, OpenStreetMap |
| **Voice** | Web Speech API (SpeechRecognition & SpeechSynthesis for Kannada, Hindi, English) |

---

## 🚀 Quick Start Guide (Windows / VS Code)

### 1. Prerequisites
- **Node.js** (v18 or higher)
- **Python** (v3.10 to 3.14)
- **Git**

---

### 2. Configure Environment (`.env`)

Copy the template file:
```powershell
cp .env.example .env
```

*In `.env`, configure live Gmail SMTP credentials (optional) or leave empty to use built-in Dev Mode logging.*

```ini
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-16-char-app-password
DEV_MODE_MOCK_EMAIL=True
```

> **Dev Mode Note**: When running locally without SMTP credentials, OTP codes are logged prominently to the backend terminal and stored in `database/dev_otp_inbox.json`. The frontend verification screen also displays a convenient **Auto Fill** badge during testing.

---

### 3. Run the Backend (Flask REST API)

In a PowerShell terminal:

```powershell
# Navigate to project directory
cd "c:\Users\Lenovo\OneDrive\Desktop\CivicGuide AI"

# Install backend dependencies
python -m pip install -r backend/requirements.txt

# Start the Flask backend server
python backend/run.py
```

*The backend server runs on `http://127.0.0.1:5000` and initializes the database automatically.*

---

### 4. Run the Frontend (React + Vite)

In a second terminal window:

```powershell
cd "c:\Users\Lenovo\OneDrive\Desktop\CivicGuide AI\frontend"

# Install npm dependencies
npm install

# Start Vite development server
npm run dev
```

*The frontend opens at `http://localhost:5173`.*

Open your web browser and navigate to:
👉 **`http://localhost:5173`**

---

### 5. Running Automated Tests

Run the comprehensive test suite verifying registration, OTP verification, User ID generation, login, profile updates, and RAG services:

```powershell
$env:PYTHONIOENCODING="utf-8"
python tests/test_backend.py
```

---

## 🔑 Pre-Seeded Demonstration Accounts

| Role | User ID / Handle | Password | Verification Status | Description |
|---|---|---|---|---|
| **Citizen (Demo)** | `citizen` | `Citizen@2026` | Verified | Standard citizen profile with sample queries |
| **Administrator** | `admin` | `Admin@CivicGuide2026` | Verified | Full access to Admin Console, Scheme & Document management |

---

## 📂 Project Directory Structure

```
CivicGuide-AI/
├── backend/
│   ├── app/
│   │   ├── ai/               # Ollama client and RAG synthesis
│   │   ├── auth/             # Token generator and @login_required decorators
│   │   ├── models/           # User, OTPVerification, Scheme, Service, Chat, Document
│   │   ├── rag/              # Document processor & ChromaDB vector store
│   │   ├── routes/           # REST API routes (auth, chat, schemes, services, admin)
│   │   ├── services/         # EmailService (SMTP + Dev Mode) & Eligibility Engine
│   │   └── utils/            # User ID generator & Database seeder
│   ├── config.py             # App & SMTP configuration
│   ├── requirements.txt      # Python dependencies
│   └── run.py                # Flask server entry point
├── database/                 # SQLite database (`civicguide.db`) & Dev OTP inbox
├── documents/                # Government policy documents for RAG indexing
├── frontend/
│   ├── src/
│   │   ├── components/       # Navbar, Footer, LanguageSelector
│   │   ├── context/          # AuthContext (login, register, verifyOTP, logout), LanguageContext
│   │   ├── pages/            # Welcome, Register, VerifyOTP, Login, ForgotPassword, UserDashboard, etc.
│   │   ├── services/         # Axios API client
│   │   ├── App.jsx           # React Router v7 configuration
│   │   └── main.jsx          # React DOM entry
│   ├── package.json
│   └── vite.config.js
├── tests/                    # Automated backend test suite (`test_backend.py`)
├── .env.example              # Environment variables template
├── .gitignore
└── README.md                 # Project documentation
```

---

## 📜 Official Citations & Data Sources
- **Central Government Portals**: [PM-Kisan](https://pmkisan.gov.in), [Ayushman Bharat PM-JAY](https://pmjay.gov.in), [PMAY-Gramin](https://pmayg.nic.in), [National Portal of India](https://india.gov.in).
- **Karnataka State Portals**: [Seva Sindhu](https://sevasindhugs.karnataka.gov.in), [Nadakacheri](https://nadakacheri.karnataka.gov.in), [SSP Karnataka](https://ssp.postmatric.karnataka.gov.in).
- **District Administration**: [Vijayanagara District Administration, Hosapete](https://vijayanagara.nic.in).
- **Cartography**: OpenStreetMap contributors.

---

## 🎓 Academic Capstone Project
Developed as an advanced full-stack AI and Citizen Identity System capstone project demonstration.
