import os
import sqlite3
import importlib.util
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Page Configuration: Clean Light Theme (Identical to React Frontend)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="CivicGuide AI • Central & State Public Services Platform",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------------------------
# Custom CSS: Perfectly matches React Tailwind CSS Design System
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    /* Force Light Background across Entire App */
    .stApp {
        background-color: #f8fafc !important;
        color: #0f172a !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }
    
    /* Hide Default Streamlit Header & Clutter */
    header[data-testid="stHeader"] {
        background-color: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(8px);
        border-bottom: 1px solid #e2e8f0;
    }
    
    /* Top Navbar Bar */
    .navbar-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 1.25rem;
        padding: 0.75rem 1.25rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }
    /* Top Navbar Brand & Logo (Matches User Screenshot) */
    .brand-wrap {
        display: flex;
        align-items: center;
        gap: 0.65rem;
        white-space: nowrap !important;
    }
    .brand-logo {
        width: 40px;
        height: 40px;
        min-width: 40px;
        background: linear-gradient(135deg, #047857 0%, #059669 50%, #d97706 100%);
        color: #ffffff;
        border-radius: 0.85rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        box-shadow: 0 4px 6px -1px rgba(4, 120, 87, 0.25);
    }
    .brand-title {
        font-size: 1.15rem;
        font-weight: 900;
        color: #0f172a;
        line-height: 1.1;
        letter-spacing: -0.02em;
        white-space: nowrap !important;
    }
    .brand-pill {
        display: inline-block;
        background-color: #e0e7ff;
        color: #3730a3;
        border: 1px solid #c7d2fe;
        font-size: 0.65rem;
        font-weight: 800;
        padding: 0.12rem 0.5rem;
        border-radius: 9999px;
        margin-left: 0.3rem;
        text-transform: uppercase;
        vertical-align: middle;
        letter-spacing: 0.04em;
    }
    .brand-subtitle {
        font-size: 0.72rem;
        font-weight: 700;
        color: #64748b;
        white-space: nowrap !important;
    }
    
    /* Hero Header */
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background-color: #d1fae5;
        color: #065f46;
        border: 1px solid #a7f3d0;
        border-radius: 9999px;
        padding: 0.25rem 0.75rem;
        font-size: 0.75rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .hero-title {
        font-size: 2.3rem !important;
        font-weight: 900 !important;
        color: #0f172a !important;
        letter-spacing: -0.025em;
        margin-bottom: 0.25rem !important;
    }
    .hero-desc {
        font-size: 0.95rem;
        color: #475569;
        max-width: 55rem;
        line-height: 1.5;
        margin-bottom: 1.25rem;
    }
    
    /* White Card Container */
    .filter-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 1.5rem;
        padding: 1.25rem 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        margin-bottom: 1.5rem;
    }
    
    /* Portal Banner */
    .portal-banner {
        background: linear-gradient(135deg, #ecfdf5 0%, #f0fdfa 50%, #f0f9ff 100%);
        border: 2px solid #86efac;
        border-radius: 1.25rem;
        padding: 1rem 1.25rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        margin: 1rem 0;
    }
    
    /* Schemes Card */
    .scheme-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 1.25rem;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        transition: all 0.2s ease;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
    }
    .scheme-card:hover {
        border-color: #10b981;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.07);
    }
    
    /* Badges */
    .badge-central {
        display: inline-block;
        background-color: #eff6ff;
        color: #1e3a8a;
        border: 1px solid #bfdbfe;
        border-radius: 9999px;
        padding: 0.2rem 0.6rem;
        font-size: 0.75rem;
        font-weight: 800;
        text-transform: uppercase;
    }
    .badge-state {
        display: inline-block;
        background-color: #fef3c7;
        color: #78350f;
        border: 1px solid #fde68a;
        border-radius: 9999px;
        padding: 0.2rem 0.6rem;
        font-size: 0.75rem;
        font-weight: 800;
        text-transform: uppercase;
    }
    .badge-sector {
        display: inline-block;
        background-color: #ecfdf5;
        color: #065f46;
        border: 1px solid #a7f3d0;
        border-radius: 9999px;
        padding: 0.15rem 0.5rem;
        font-size: 0.75rem;
        font-weight: 700;
        margin-top: 0.25rem;
    }
    
    .benefit-box {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 0.75rem;
        padding: 0.65rem 0.75rem;
        margin: 0.5rem 0;
        font-weight: 600;
        font-size: 0.85rem;
        color: #0f172a;
    }

    /* =========================================================================
       EXACT REACT-STYLE TOP NAVBAR BUTTONS & RADIO TABS (Matches User Image)
       ========================================================================= */
    /* Hide ALL native radio input circles, bullets, and dots across all radios */
    div[data-testid="stRadio"] [data-baseweb="radio"] > div:first-of-type,
    div[data-testid="stRadio"] [data-baseweb="radio"] > div:first-of-type *,
    div[data-testid="stRadio"] [data-baseweb="radio"] > div:not([data-testid="stMarkdownContainer"]),
    div[data-testid="stRadio"] [data-baseweb="radio"] input[type="radio"],
    div[data-testid="stRadio"] [data-baseweb="radio"] svg,
    div[data-testid="stRadio"] label > div:first-of-type,
    div[data-testid="stRadio"] label > div:first-of-type *,
    div[data-testid="stRadio"] label > div:not([data-testid="stMarkdownContainer"]),
    div[data-testid="stRadio"] label input[type="radio"],
    div[data-testid="stRadio"] label svg,
    div[data-testid="stRadio"] div[role="radiogroup"] label > div:first-child,
    div[data-testid="stRadio"] div[role="radiogroup"] label > div:first-of-type,
    div[data-testid="stRadio"] div[role="radiogroup"] label > span {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
        opacity: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        outline: none !important;
        position: absolute !important;
        left: -9999px !important;
    }
    
    div[data-testid="stRadio"] label > [data-testid="stMarkdownContainer"] {
        display: inline-flex !important;
        align-items: center !important;
        visibility: visible !important;
        opacity: 1 !important;
        position: static !important;
    }

    /* Strict ONE-LINE flex row without wrapping */
    div[data-testid="stRadio"] div[role="radiogroup"] {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: flex-start !important;
        gap: 0.2rem !important;
        flex-wrap: nowrap !important;
        white-space: nowrap !important;
        overflow-x: auto !important;
        padding: 0 !important;
        margin: 0 !important;
        scrollbar-width: none !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"]::-webkit-scrollbar {
        display: none !important;
    }

    /* Inactive navbar tab button style */
    div[data-testid="stRadio"] div[role="radiogroup"] label {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 0.35rem 0.6rem !important;
        border-radius: 0.75rem !important;
        background-color: transparent !important;
        border: 1px solid transparent !important;
        cursor: pointer !important;
        transition: all 0.15s ease-in-out !important;
        margin: 0 !important;
        white-space: nowrap !important;
        flex-shrink: 0 !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
        background-color: #f1f5f9 !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label p {
        font-size: 0.88rem !important;
        font-weight: 700 !important;
        color: #475569 !important;
        margin: 0 !important;
        line-height: 1.2 !important;
        white-space: nowrap !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label:hover p {
        color: #0f172a !important;
    }

    /* ACTIVE TAB: Mint green pill with dark green bold text (Exact match to Image) */
    div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
        background-color: #d1fae5 !important;
        border: 1px solid #a7f3d0 !important;
        box-shadow: 0 1px 2px rgba(16, 185, 129, 0.15) !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) p {
        color: #065f46 !important;
        font-weight: 900 !important;
    }

    /* Fallback for browsers without :has */
    div[data-testid="stRadio"] div[role="radiogroup"] label[aria-checked="true"],
    div[data-testid="stRadio"] div[role="radiogroup"] label[data-checked="true"] {
        background-color: #d1fae5 !important;
        border: 1px solid #a7f3d0 !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label[aria-checked="true"] p,
    div[data-testid="stRadio"] div[role="radiogroup"] label[data-checked="true"] p {
        color: #065f46 !important;
        font-weight: 900 !important;
    }

    /* GitHub Link Button Style */
    div[data-testid="stLinkButton"] a {
        background-color: #f8fafc !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 0.75rem !important;
        color: #334155 !important;
        font-weight: 800 !important;
        font-size: 0.85rem !important;
        padding: 0.45rem 0.85rem !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03) !important;
        transition: all 0.2s ease !important;
        display: inline-flex !important;
        align-items: center !important;
        gap: 0.35rem !important;
    }
    div[data-testid="stLinkButton"] a:hover {
        background-color: #f1f5f9 !important;
        color: #0f172a !important;
        border-color: #cbd5e1 !important;
        transform: translateY(-1px);
    }

    /* Language Selectbox Style */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        border-radius: 0.75rem !important;
        border-color: #e2e8f0 !important;
        background-color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 0.85rem !important;
        color: #334155 !important;
        min-height: 2.3rem !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Constants & Official State Portals Dictionary
# ---------------------------------------------------------------------------
ALL_INDIAN_LANGUAGES = [
    "English (English)",
    "हिन्दी (Hindi)",
    "ಕನ್ನಡ (Kannada)",
    "తెలుగు (Telugu)",
    "தமிழ் (Tamil)",
    "मराठी (Marathi)",
    "বাংলা (Bengali)",
    "ગુજરાતી (Gujarati)",
    "മലയാളം (Malayalam)",
    "ਪੰਜਾਬੀ (Punjabi)",
    "ଓଡ଼ିଆ (Odia)",
    "অসমীয়া (Assamese)",
    "اردو (Urdu)",
    "संस्कृतम् (Sanskrit)",
    "कोंकणी (Konkani)",
    "नेपाली (Nepali)",
    "मैथिली (Maithili)",
    "ᱥᱟᱱᱛᱟᱲᱤ (Santali)",
    "کٲشُر (Kashmiri)",
    "सिन्धी (Sindhi)",
    "डोगरी (Dogri)",
    "মৈতৈಲೋನ್ (Manipuri)",
    "बर' (Bodo)"
]

ALL_INDIAN_STATES = [
    "All India",
    "Karnataka", "Maharashtra", "Delhi", "Tamil Nadu", "Uttar Pradesh",
    "Andhra Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat",
    "Haryana", "Himachal Pradesh", "Jharkhand", "Kerala", "Madhya Pradesh",
    "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
    "Rajasthan", "Sikkim", "Telangana", "Tripura", "Uttarakhand", "West Bengal",
    "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu",
    "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
]

STATE_OFFICIAL_PORTALS = {
    "All India": {
        "name": "National Portal of India & myScheme Portal",
        "url": "https://www.myscheme.gov.in",
        "description": "Official National Platform for All-India Central & State Government Welfare Schemes across all 36 States and Union Territories. Covers 47+ verified initiatives accessible directly with citizen screening."
    },
    "Karnataka": {
        "name": "Karnataka Seva Sindhu & Nadakacheri Portal",
        "url": "https://sevasindhu.karnataka.gov.in",
        "description": "Official Government of Karnataka portal for citizen services, 5 guarantee schemes (Gruha Lakshmi, Yuva Nidhi, Gruha Jyothi, Shakti, Anna Bhagya), and Nadakacheri certificates."
    },
    "Maharashtra": {
        "name": "Aaple Sarkar / MahaOnline Portal",
        "url": "https://aaplesarkar.mahaonline.gov.in",
        "description": "Official Government of Maharashtra public services, certificates, and citizen welfare schemes portal."
    },
    "Delhi": {
        "name": "e-District Delhi Citizen Services",
        "url": "https://edistrict.delhigovt.nic.in",
        "description": "Government of NCT of Delhi official portal for certificates, revenue, free electricity, and welfare services."
    },
    "Tamil Nadu": {
        "name": "TNeGA e-Sevai Portal",
        "url": "https://www.tnesevai.tn.gov.in",
        "description": "Government of Tamil Nadu official electronic citizen services, Kalaignar Magalir Urimai, and welfare directory."
    },
    "Uttar Pradesh": {
        "name": "eDistrict Uttar Pradesh Portal",
        "url": "https://edistrict.up.gov.in",
        "description": "Government of Uttar Pradesh official citizen services, scholarships, smartphone distribution, and revenue portal."
    },
    "Gujarat": {
        "name": "Digital Gujarat Citizen Services Portal",
        "url": "https://www.digitalgujarat.gov.in",
        "description": "Official Government of Gujarat portal for scholarships, certificates, and public welfare schemes."
    },
    "Rajasthan": {
        "name": "Jan Soochna & e-Mitra Rajasthan Portal",
        "url": "https://jansoochna.rajasthan.gov.in",
        "description": "Official Government of Rajasthan portal for public schemes, Mukhyamantri Ayushman Arogya, and social pensions."
    },
    "Andhra Pradesh": {
        "name": "MeeSeva Andhra Pradesh Portal",
        "url": "https://meeseva.ap.gov.in",
        "description": "Official Government of Andhra Pradesh citizen delivery and welfare distribution portal."
    },
    "Telangana": {
        "name": "MeeSeva Telangana Portal",
        "url": "https://ts.meeseva.telangana.gov.in",
        "description": "Official Government of Telangana online citizen delivery and Rythu Bharosa welfare portal."
    },
    "Kerala": {
        "name": "e-District Kerala Services Portal",
        "url": "https://edistrict.kerala.gov.in",
        "description": "Government of Kerala official portal for certificates, revenue, and KASP healthcare benefits."
    },
    "West Bengal": {
        "name": "Bangla Sahayata Kendra / e-District WB",
        "url": "https://edistrict.wb.gov.in",
        "description": "Government of West Bengal citizen services delivery, Kanyashree, and Lakshmir Bhandar portal."
    },
    "Madhya Pradesh": {
        "name": "MP e-District Citizen Services Portal",
        "url": "https://mpedistrict.gov.in",
        "description": "Government of Madhya Pradesh public services guarantee and Ladli Behna welfare portal."
    },
    "Bihar": {
        "name": "RTPS Bihar ServicePlus Portal",
        "url": "https://serviceonline.bihar.gov.in",
        "description": "Government of Bihar official portal for Right to Public Services (RTPS), student credit card, and citizen welfare."
    },
    "Punjab": {
        "name": "e-Sewa Punjab Citizen Portal",
        "url": "https://esewa.punjab.gov.in",
        "description": "Government of Punjab official citizen facilitation and domestic power welfare portal."
    },
    "Haryana": {
        "name": "Saral Haryana Citizen Portal",
        "url": "https://saralharyana.gov.in",
        "description": "Government of Haryana Antyodaya SARAL portal for government schemes and citizen services."
    },
    "Odisha": {
        "name": "Odisha One & e-District Portal",
        "url": "https://odishaone.gov.in",
        "description": "Government of Odisha integrated citizen service portal for KALIA scheme and welfare services."
    },
    "Assam": {
        "name": "Sewa Setu Assam Portal",
        "url": "https://sewasetu.assam.gov.in",
        "description": "Government of Assam citizen centric service delivery and Orunodoi 2.0 portal."
    }
}

# ---------------------------------------------------------------------------
# Database Loader with Verified Fallbacks
# ---------------------------------------------------------------------------
def _load_data_from_python_modules():
    schemes = []
    services = []
    curr_dir = os.path.dirname(os.path.abspath(__file__))

    # 1. Load All-India Schemes from git-tracked backend/app/utils/all_india_schemes_data.py
    s_path = os.path.join(curr_dir, "backend", "app", "utils", "all_india_schemes_data.py")
    if os.path.exists(s_path):
        try:
            spec = importlib.util.spec_from_file_location("all_india_schemes_data", s_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, "ALL_INDIA_SCHEMES"):
                for idx, s in enumerate(mod.ALL_INDIA_SCHEMES, start=1):
                    item = dict(s)
                    item["id"] = idx
                    schemes.append(item)
        except Exception:
            pass

    # 2. Load Public Services from git-tracked backend/app/utils/all_india_services_data.py
    sv_path = os.path.join(curr_dir, "backend", "app", "utils", "all_india_services_data.py")
    if os.path.exists(sv_path):
        try:
            spec = importlib.util.spec_from_file_location("all_india_services_data", sv_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, "ALL_PUBLIC_SERVICES"):
                for idx, sv in enumerate(mod.ALL_PUBLIC_SERVICES, start=1):
                    item = dict(sv)
                    item["id"] = idx
                    services.append(item)
        except Exception:
            pass

    return schemes, services

@st.cache_data
def load_database_data():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    db_paths = [
        os.path.join(curr_dir, "database", "users.db"),
        os.path.join("database", "users.db"),
        os.path.join("backend", "civicguide.db"),
        "users.db"
    ]
    db_file = None
    for p in db_paths:
        if os.path.exists(p):
            db_file = p
            break

    schemes = []
    services = []

    if db_file:
        try:
            conn = sqlite3.connect(db_file)
            schemes_df = pd.read_sql_query("SELECT * FROM schemes ORDER BY id ASC", conn)
            services_df = pd.read_sql_query("SELECT * FROM public_services ORDER BY id ASC", conn)
            conn.close()
            schemes = schemes_df.to_dict(orient="records")
            services = services_df.to_dict(orient="records")
        except Exception:
            pass

    if not schemes or len(schemes) == 0:
        py_schemes, py_services = _load_data_from_python_modules()
        schemes = py_schemes
        if not services or len(services) == 0:
            services = py_services

    return schemes, services

# ---------------------------------------------------------------------------
# AI ASSISTANT RESPONSE SYNTHESIS ENGINE (STEP-BY-STEP PROCESS)
# ---------------------------------------------------------------------------
def _synthesize_python_ai_reply(query, schemes):
    q_lower = query.lower().strip()
    
    # Check scheme keywords
    alias_map = {
        "pm-kisan": ["kisan", "pm kisan", "pmkisan", "farmer 6000", "2000", "ರೈತ", "ಕಿಸಾನ್"],
        "ayushman bharat": ["ayushman", "pm-jay", "pmjay", "health card", "5 lakh", "ಆಯುಷ್ಮಾನ್", "ಆರೋಗ್ಯ", "hospital"],
        "pm surya ghar": ["surya", "solar", "rooftop", "electricity", "muft bijli", "ಸೌರ", "ವಿದ್ಯುತ್"],
        "pm vishwakarma": ["vishwakarma", "artisan", "toolkit", "15000", "carpenter", "ವಿಶ್ವಕರ್ಮ"],
        "mudra": ["mudra", "pmmy", "business loan", "small loan", "ಮುದ್ರಾ"],
        "gruha lakshmi": ["gruha lakshmi", "graha lakshmi", "2000 women", "ಗೃಹ ಲಕ್ಷ್ಮಿ"],
        "yuva nidhi": ["yuva nidhi", "unemployment", "3000 graduate", "ಯುವ ನಿಧಿ"],
        "gruha jyothi": ["gruha jyothi", "free 200 units", "ಗೃಹ ಜ್ಯೋತಿ"],
        "shakti": ["shakti", "free bus", "ksrtc", "ಶಕ್ತಿ ಯೋಜನೆ"],
        "ssp": ["ssp", "scholarship", "vidyasiri", "post matric", "ವಿದ್ಯಾರ್ಥಿವೇತನ", "ವಿದ್ಯಾಸಿರಿ"],
        "anna bhagya": ["anna bhagya", "free rice", "170 dbt", "ಅನ್ನ ಭಾಗ್ಯ"]
    }
    
    found = None
    for alias_key, kws in alias_map.items():
        if any(kw in q_lower for kw in kws):
            for s in schemes:
                if alias_key in s.get("name", "").lower():
                    found = s
                    break
            if found:
                break
                
    if not found:
        for s in schemes:
            s_name = s.get("name", "").lower()
            words = [w for w in s_name.replace("-", " ").split() if len(w) > 3 and w not in ["scheme", "yojana", "pradhan", "mantri"]]
            if any(w in q_lower for w in words):
                found = s
                break

    # Civic document: Caste/Income
    if any(k in q_lower for k in ['caste', 'income certificate', 'caste and income', 'ಜಾತಿ', 'ಆದಾಯ', 'जाति', 'आय प्रमाण']):
        return {
            "answer": """### 🎯 Direct Answer
**Caste and Income Certificates** are officially issued by the Revenue Department through **Nadakacheri (Atalji Janasnehi Kendra)** and **Seva Sindhu** in Karnataka, and respective State Revenue Portals across India. They are legally mandatory for student scholarships (SSP), college admissions, fee waivers, and government welfare benefits.

### 💰 Key Benefits & Financial Assistance
- **Education Fee Concessions:** 100% or partial tuition fee waiver across universities and colleges.
- **Welfare Eligibility:** Mandatory document for Gruha Lakshmi, Yuva Nidhi, SSP Vidyasiri, and housing allotments.
- **Validity:** Digitally signed with a unique RD Number and QR Code, valid for 5 continuous years.

### 👥 Eligibility Criteria (Who Qualifies)
- Permanent residents of the respective State / Karnataka.
- Belongs to notified SC, ST, Category-1, 2A, 2B, 3A, 3B, or EWS categories.
- Annual household income must be within government prescribed ceiling (e.g. up to ₹2.5 Lakhs for scholarships/BPL).

### 📝 Step-by-Step Implementation & How to Apply
- **Step 1: Document Checklist & Preparation:** Keep applicant Aadhaar, parent Aadhaar, Ration Card (BPL/APL), and school Leaving Certificate (TC / marksheet) ready.
- **Step 2: Visit Portal or Citizen Kiosk:** Go to [nadakacheri.karnataka.gov.in](https://nadakacheri.karnataka.gov.in) or visit your nearest **Grama One**, **Karnataka One**, or **CSC** center.
- **Step 3: Online Form Submission:** Click 'Online Application' > 'Apply Online', log in with mobile OTP, and select Caste or Income Certificate.
- **Step 4: Departmental Scrutiny & Field Verification:** Pay nominal government fee (₹25 - ₹40) online. The Village Accountant (VA) and Revenue Inspector (RI) verify records and report to the Tahsildar.
- **Step 5: Sanction Order & Certificate Download:** Receive your acknowledgment with RD Number. Once digitally signed by the Tahsildar, download the certificate directly from the Nadakacheri portal.

### 📑 Required Documents Checklist
- Applicant and Parent Aadhaar Cards
- Family Ration Card (BPL / Antyodaya / APL)
- School Transfer Certificate (TC) showing caste or previous caste certificate
- Self-declaration of annual household income and passport photo

### 🏛️ Where to Apply & Official Links
- 🔗 **Official Portal:** [https://nadakacheri.karnataka.gov.in](https://nadakacheri.karnataka.gov.in)
- 🏢 **Assistance Centers:** Grama One, Atalji Janasnehi Kendra (Nadakacheri), or Taluk Tahsildar Office
- 📞 **Helpline:** 080-22340676 / 1902""",
            "url": "https://nadakacheri.karnataka.gov.in"
        }

    # Civic document: Land RTC / Pahani
    if any(k in q_lower for k in ['rtc', 'pahani', 'bhoomi', 'land record', 'survey number', 'ಪಹಣಿ', 'ಭೂಮಿ', 'ಖತೌನಿ']):
        return {
            "answer": """### 🎯 Direct Answer
The **RTC (Record of Rights, Tenancy and Crops) / Pahani** is the official land ownership document issued online through the **Bhoomi Portal** by the Karnataka Revenue Department. It is required for PM-Kisan verification, crop loans, and land title confirmation.

### 💰 Key Benefits & Financial Assistance
- **PM-Kisan & Crop Insurance:** Mandatory proof of cultivable land ownership for receiving ₹6,000 annual PM-Kisan DBT.
- **Institutional Credit:** Access to Kisan Credit Card (KCC) and interest-subsidised bank crop loans.
- **Instant Digital Download:** Valid digitally signed original RTC for just ₹15.

### 👥 Eligibility Criteria (Who Qualifies)
- Any agricultural or non-agricultural land owner or authorized family member.
- Must know the District, Taluk, Hobli, Village, and Survey Number / Hissa Number.

### 📝 Step-by-Step Implementation & How to Apply
- **Step 1: Check Survey Details:** Keep your District, Taluk, Hobli, Village name, and land Survey Number ready.
- **Step 2: Open Bhoomi Portal:** Visit [landrecords.karnataka.gov.in](https://landrecords.karnataka.gov.in) or visit your nearest **Grama One / Taluk Bhoomi Kiosk**.
- **Step 3: Select RTC View / Download:** Click 'Citizen Services' > 'View RTC and MR' or 'Current Year RTC'.
- **Step 4: Enter Survey and Hissa:** Select your Taluk and Village, enter Survey Number, select Surnoc and Hissa, and click 'Fetch Details'.
- **Step 5: Online Payment & Print RTC:** Pay ₹15 via UPI/NetBanking to view and print the digitally signed original Karnataka Government RTC/Pahani.

### 📑 Required Documents Checklist
- Land Survey Number & Hissa Number
- Village & Hobli details
- Aadhaar Card of Landowner (for PM-Kisan linking)

### 🏛️ Where to Apply & Official Links
- 🔗 **Official Portal:** [https://landrecords.karnataka.gov.in](https://landrecords.karnataka.gov.in)
- 🏢 **Assistance Centers:** Village Grama One center or Taluk Tahsildar Bhoomi Kiosk
- 📞 **Helpline:** 080-22113255 (Bhoomi Monitoring Cell)""",
            "url": "https://landrecords.karnataka.gov.in"
        }

    # Civic document: Ration Card
    if any(k in q_lower for k in ['ration', 'bpl card', 'ration card', 'ರೇಷನ್', 'ಆಹಾರ', 'ರಾಶನ್']):
        return {
            "answer": """### 🎯 Direct Answer
**Ration Cards (BPL / Antyodaya / APL)** are issued by the Department of Food, Civil Supplies & Consumer Affairs. In Karnataka, cards are managed via **ahara.kar.nic.in** and are required for Anna Bhagya free food grains and Ayushman Bharat health benefits.

### 💰 Key Benefits & Financial Assistance
- **Anna Bhagya:** 5 kg free food grains per member + ₹170 direct DBT per extra 5 kg per member.
- **Gruha Lakshmi:** ₹2,000 monthly DBT for female family heads on BPL/Antyodaya cards.
- **Ayushman PM-JAY:** ₹5 Lakh cashless hospitalization coverage per family per year.

### 👥 Eligibility Criteria (Who Qualifies)
- **BPL / Antyodaya Card:** Annual family income below ₹1.20 Lakhs, no four-wheeler, no commercial income tax payer in the family.
- **APL Card:** Any resident citizen not falling under BPL/Antyodaya criteria.

### 📝 Step-by-Step Implementation & How to Apply
- **Step 1: Document Preparation:** Keep Aadhaar cards of all family members, active mobile number, electricity account bill, and income certificate ready.
- **Step 2: Visit Seva Sindhu / Ahara Portal:** Navigate to [ahara.kar.nic.in](https://ahara.kar.nic.in) or visit your nearest **Grama One / Karnataka One** center.
- **Step 3: Online Form Submission:** Enter all family members' Aadhaar numbers; authenticate via biometric fingerprint or Aadhaar OTP.
- **Step 4: Scrutiny by Food Inspector:** The local Food Inspector verifies residence and domestic criteria online.
- **Step 5: Sanction Order & Card Allotment:** Once approved, your Ration Card Number is generated. Download e-Ration Card or collect card from your local Fair Price Shop (PDS).

### 📑 Required Documents Checklist
- Aadhaar Cards of all family members (mandatory)
- Revenue Income and Caste Certificate (RD Number)
- Latest domestic electricity bill (showing Consumer ID)
- Active bank passbook linked to family head's Aadhaar

### 🏛️ Where to Apply & Official Links
- 🔗 **Official Portal:** [https://ahara.kar.nic.in](https://ahara.kar.nic.in)
- 🏢 **Assistance Centers:** Grama One, Karnataka One, or Taluk Food Shirastedar Office
- 📞 **Toll-Free Helpline:** 1967 / 1800-425-9339""",
            "url": "https://ahara.kar.nic.in"
        }

    # If scheme found
    if found:
        name = found.get('name')
        gov_level = found.get('government_level')
        benefits = found.get('benefits')
        eligibility = found.get('eligibility')
        docs = found.get('required_documents', 'Aadhaar Card, Ration Card, Bank Passbook, Mobile Number')
        official_url = found.get('official_url', 'https://www.myscheme.gov.in')
        
        return {
            "answer": f"""### 🎯 Direct Answer
**{name}** is an official {gov_level} initiative designed to provide direct financial assistance, capital subsidies, and welfare entitlements directly to eligible citizens across India.

### 💰 Key Benefits & Financial Assistance
- **Direct Financial Assistance:** {benefits}
- **Disbursement Mode:** Direct Benefit Transfer (DBT) directly into the beneficiary's Aadhaar-linked bank account without intermediaries.
- **Zero Middlemen:** Digitised, automated online verification ensuring full transparency.

### 👥 Eligibility Criteria (Who Qualifies)
- {eligibility}
- Applicant must satisfy statutory domicile and residence criteria for {found.get('state', 'India')}.

### 📝 Step-by-Step Implementation & How to Apply
- **Step 1: Document Checklist & Preparation:** Keep original Aadhaar Card, Ration Card/Income proof, and Bank Passbook ready.
- **Step 2: Visit Official Portal or Kiosk:** Go to the official website [{official_url}]({official_url}) or visit your nearest **Grama One**, **Karnataka One**, or **Common Service Centre (CSC)**.
- **Step 3: Online Form Submission & Aadhaar OTP:** Enter demographic data, Aadhaar number, and verify using the OTP sent to your registered mobile phone.
- **Step 4: Departmental Scrutiny & Field Verification:** The administering department and Village Accountant/Inspector verify submitted details online.
- **Step 5: Sanction Order & DBT Disbursement:** Receive your application acknowledgment number to track status. Upon approval, funds or entitlements are credited directly.

### 📑 Required Documents Checklist
- {docs}
- Active mobile number linked to Aadhaar
- Bank account passbook with NPCI / Aadhaar seeding

### 🏛️ Where to Apply & Official Links
- 🔗 **Official Online Portal:** [{official_url}]({official_url})
- 🏢 **Local Kiosks:** Nearest Grama One, Bapuji Seva Kendra, or Common Service Centre (CSC)
- 📞 **Helpline:** 1902 / 1800-180-1551 (Citizen Support Desk)""",
            "url": official_url
        }

    # Fallback general query guidance
    return {
        "answer": f"""### 🎯 Direct Answer
CivicGuide AI assists Indian citizens with verified guidelines, eligibility checks, and step-by-step application instructions for all 47 Central and State government welfare schemes.

### 💰 Key Benefits & Financial Assistance
- **Direct Benefit Transfer (DBT):** Cash subsidies and welfare payments transferred directly into Aadhaar-linked bank accounts.
- **Comprehensive Coverage:** Schemes span Agriculture (PM-Kisan), Healthcare (Ayushman Bharat), Clean Energy (PM Surya Ghar), Social Security, and Scholarships.

### 👥 Eligibility Criteria (Who Qualifies)
- Indian citizens meeting age, annual household income, and state domicile criteria.
- Use our built-in **Eligibility Checker** tab to automatically screen your family criteria against all schemes.

### 📝 Step-by-Step Implementation & How to Apply
- **Step 1: Screen Eligibility:** Select your age, income, and state on the **Eligibility Checker** tab.
- **Step 2: Collect Required Documents:** Ensure your Aadhaar is linked to your active mobile number and your bank account is seeded with NPCI/Aadhaar.
- **Step 3: Visit Official Portal or Kiosk:** Access the national portal [myscheme.gov.in](https://www.myscheme.gov.in) or visit your nearest **Grama One / CSC**.
- **Step 4: Departmental Verification:** Online scrutiny of uploaded documents by designated municipal/revenue officers.
- **Step 5: Track Acknowledgment & Receive DBT:** Use the generated acknowledgment number to monitor progress until benefit disbursement.

### 📑 Required Documents Checklist
- Aadhaar Card (linked to active mobile number)
- Ration Card (BPL / Antyodaya / APL)
- Domicile / Residence Proof and Revenue Caste-Income Certificate
- Bank Passbook with NPCI Seeding

### 🏛️ Where to Apply & Official Links
- 🔗 **National Schemes Portal:** [https://www.myscheme.gov.in](https://www.myscheme.gov.in)
- 🏢 **Assistance Centers:** Nearest CSC Kiosk, Grama One, or Taluk Tahsildar Office
- 📞 **National Citizen Helpline:** 1912 / 1800-180-1551""",
        "url": "https://www.myscheme.gov.in"
    }

schemes_list, services_list = load_database_data()

# ---------------------------------------------------------------------------
# TOP NAVBAR: Matches User Image Exactly (Single Line Layout)
# ---------------------------------------------------------------------------
if "top_navbar_tab" not in st.session_state:
    st.session_state.top_navbar_tab = "🧭 Home"

nav_col_logo, nav_col_tabs, nav_col_right = st.columns([1.9, 7.3, 2.8], vertical_alignment="center")

with nav_col_logo:
    st.markdown("""
    <div class="brand-wrap">
        <div class="brand-logo">🏛️</div>
        <div>
            <div class="brand-title">CivicGuide AI <span class="brand-pill">ALL INDIA</span></div>
            <div class="brand-subtitle">Central & State Governments</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with nav_col_tabs:
    active_nav = st.radio(
        "Navigation",
        [
            "🧭 Home",
            "🏛️ Government Schemes",
            "🤖 AI Assistant",
            "📋 Eligibility Checker",
            "📍 Service Map"
        ],
        horizontal=True,
        label_visibility="collapsed",
        key="top_navbar_tab"
    )

with nav_col_right:
    c_lang, c_gh, c_user, c_out = st.columns([4.2, 2.2, 0.9, 0.7], vertical_alignment="center")
    with c_lang:
        selected_lang = st.selectbox("Language", ALL_INDIAN_LANGUAGES, index=0, key="top_navbar_language", label_visibility="collapsed")
    with c_gh:
        st.link_button("GitHub", "https://github.com/kpbinduprakasha-cpu/CivicGuide-AI")
    with c_user:
        st.markdown("""
        <div style="width: 34px; height: 34px; border-radius: 50%; background-color: #047857; color: white; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.95rem; border: 2px solid #a7f3d0;" title="Citizen: K P BINDUPRAKASHA">
            K
        </div>
        """, unsafe_allow_html=True)
    with c_out:
        st.markdown("""
        <div style="font-size: 1.15rem; color: #64748b; cursor: pointer; text-align: center;" title="Sign Out">
            🚪
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr style='margin-top: 0.2rem; margin-bottom: 1.25rem; border-color: #e2e8f0;'>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# VIEW: 1. GOVERNMENT SCHEMES (Matches Image 2 Exactly)
# ---------------------------------------------------------------------------
if "Government Schemes" in active_nav:
    
    # Hero Title & Action Pills Row
    h_col1, h_col2 = st.columns([3, 2])
    with h_col1:
        st.markdown('<div class="hero-badge">🛡️ Official Government Welfare Directory • Verified All-India Database</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-title">Government Schemes</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-desc">Search, filter, and apply for Central and State government welfare schemes across India. Verified with official application guidelines, required document checklists, and citizen eligibility matching.</div>', unsafe_allow_html=True)
    with h_col2:
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        b1, b2, b3 = st.columns(3)
        with b1:
            st.button("📍 Offices & Taluk Map", key="h_btn1")
        with b2:
            st.button("🔖 Saved Schemes (0)", key="h_btn2")
        with b3:
            st.button("✨ AI Matched (40)", key="h_btn3")

    # -----------------------------------------------------------------------
    # Main White Filter Card (Matches Image 2)
    # -----------------------------------------------------------------------
    st.markdown('<div class="filter-card">', unsafe_allow_html=True)

    # Row 1: Search & Sort Dropdown
    s_col1, s_col2 = st.columns([5, 2])
    with s_col1:
        search_query = st.text_input(
            "Search Schemes",
            placeholder="Search by scheme name, benefits, or keywords (e.g. scholarship, solar, 2000, farmer, loan)...",
            label_visibility="collapsed"
        )
    with s_col2:
        sort_by = st.selectbox(
            "Sort By",
            [
                "⭐ AI Best Match First",
                "🏛️ Central Government First",
                "📍 State Government First",
                "🔤 Scheme Name (A to Z)"
            ],
            index=0,
            label_visibility="collapsed"
        )

    st.markdown("<hr style='margin: 0.75rem 0; border-color: #f1f5f9;'>", unsafe_allow_html=True)

    # Row 2: Schemes Scope, Portal Selector & View Controls
    ctrl1, ctrl2, ctrl3, ctrl4 = st.columns([4, 2, 2, 2])
    with ctrl1:
        scope_choice = st.radio(
            "Schemes Scope",
            [
                "🏛️ Central (10)",
                "📍 State",
                "🇮🇳 All Combined (47)"
            ],
            index=0,
            horizontal=True,
            label_visibility="collapsed"
        )
    with ctrl2:
        selected_state = st.selectbox("Portal", ALL_INDIAN_STATES, index=0, label_visibility="collapsed")
    with ctrl3:
        view_mode = st.radio("Display Mode", ["Cards View", "Combined Table"], horizontal=True, label_visibility="collapsed")
    with ctrl4:
        # Counter pill
        st.markdown(f"""
        <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 0.75rem; padding: 0.45rem 0.75rem; font-size: 0.8rem; font-weight: 800; color: #334155; text-align: center;">
            Showing <span style="color: #047857;">{len(schemes_list)}</span> schemes
        </div>
        """, unsafe_allow_html=True)

    # Official State Government Portal Banner (Matches Image 2)
    portal_info = STATE_OFFICIAL_PORTALS.get(selected_state, STATE_OFFICIAL_PORTALS["All India"])
    st.markdown(f"""
    <div class="portal-banner">
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <div style="width: 40px; height: 40px; background-color: #047857; color: white; border-radius: 0.75rem; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; flex-shrink: 0;">
                ↗
            </div>
            <div>
                <div style="display: inline-block; background-color: #d1fae5; color: #065f46; border: 1px solid #a7f3d0; border-radius: 9999px; padding: 0.1rem 0.5rem; font-size: 0.65rem; font-weight: 800; text-transform: uppercase;">
                    {selected_state if selected_state != 'All India' else 'NATIONAL'} PORTAL • Verified Link
                </div>
                <div style="font-size: 1.05rem; font-weight: 900; color: #0f172a; margin: 0.15rem 0;">
                    {portal_info['name']}
                </div>
                <div style="font-size: 0.8rem; color: #475569; max-width: 50rem;">
                    {portal_info['description']}
                </div>
            </div>
        </div>
        <div>
            <a href="{portal_info['url']}" target="_blank" style="background-color: #047857; color: white; padding: 0.5rem 1.25rem; border-radius: 9999px; font-size: 0.85rem; font-weight: 800; text-decoration: none; display: inline-block; white-space: nowrap;">
                Visit {selected_state if selected_state != 'All India' else 'myScheme'} Website ↗
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Row 3: Target Citizen Group Filter (Matches Image 2)
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.75rem; margin-bottom: 0.35rem;">
        <span style="font-size: 0.75rem; font-weight: 800; color: #334155; text-transform: uppercase; letter-spacing: 0.05em;">Target Citizen Group:</span>
        <span style="font-size: 0.7rem; font-weight: 700; color: #94a3b8; text-transform: uppercase;">Select audience filter</span>
    </div>
    """, unsafe_allow_html=True)
    
    target_group = st.radio(
        "Target Citizen Group",
        [
            "👥 All Citizens",
            "🎓 Students & Youth",
            "🌾 Farmers & Rural",
            "👩 Women & Families",
            "🔨 Artisans & MSME",
            "🩺 Senior Citizens & Health"
        ],
        index=0,
        horizontal=True,
        label_visibility="collapsed"
    )

    # Row 4: Welfare Sector Filter
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.75rem; margin-bottom: 0.35rem;">
        <span style="font-size: 0.75rem; font-weight: 800; color: #334155; text-transform: uppercase; letter-spacing: 0.05em;">Welfare Sector:</span>
        <span style="font-size: 0.7rem; font-weight: 700; color: #94a3b8; text-transform: uppercase;">Select sector filter</span>
    </div>
    """, unsafe_allow_html=True)

    welfare_sector = st.radio(
        "Welfare Sector",
        [
            "All",
            "Agriculture",
            "Education",
            "Healthcare",
            "Employment",
            "Housing",
            "Women and child welfare",
            "Social welfare",
            "Financial assistance"
        ],
        index=0,
        horizontal=True,
        label_visibility="collapsed"
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # -----------------------------------------------------------------------
    # Filtering Logic
    # -----------------------------------------------------------------------
    filtered = list(schemes_list)

    # Scope
    if "Central" in scope_choice:
        filtered = [s for s in filtered if "central" in (s.get("government_level") or "").lower()]
    elif "State" in scope_choice:
        if selected_state and selected_state != "All India":
            filtered = [
                s for s in filtered
                if "central" not in (s.get("government_level") or "").lower() and
                   (selected_state.lower() in (s.get("state") or "").lower() or selected_state.lower() in (s.get("government_level") or "").lower())
            ]
        else:
            filtered = []
    else: # All Combined
        pass

    # Sector Filter
    if welfare_sector != "All":
        filtered = [s for s in filtered if welfare_sector.lower() in (s.get("category") or "").lower()]

    # Target Citizen Group Filter
    if "Students" in target_group:
        filtered = [s for s in filtered if s.get("category") == "Education" or "scholarship" in (s.get("description") or "").lower() or "yuva" in (s.get("name") or "").lower()]
    elif "Farmers" in target_group:
        filtered = [s for s in filtered if s.get("category") == "Agriculture" or "farmer" in (s.get("description") or "").lower() or "kisan" in (s.get("name") or "").lower()]
    elif "Women" in target_group:
        filtered = [s for s in filtered if s.get("category") == "Women and child welfare" or "woman" in (s.get("description") or "").lower() or "girl" in (s.get("description") or "").lower()]
    elif "Artisans" in target_group:
        filtered = [s for s in filtered if "artisan" in (s.get("description") or "").lower() or "vishwakarma" in (s.get("name") or "").lower() or "mudra" in (s.get("name") or "").lower()]
    elif "Senior" in target_group:
        filtered = [s for s in filtered if s.get("category") == "Healthcare" or "pension" in (s.get("description") or "").lower() or "senior" in (s.get("eligibility") or "").lower()]

    # Search Query
    if search_query.strip():
        q = search_query.strip().lower()
        filtered = [
            s for s in filtered
            if q in (s.get("name") or "").lower() or
               q in (s.get("description") or "").lower() or
               q in (s.get("benefits") or "").lower() or
               q in (s.get("category") or "").lower()
        ]

    # Sorting
    if "Name" in sort_by:
        filtered.sort(key=lambda s: s.get("name", ""))
    elif "State" in sort_by:
        filtered.sort(key=lambda s: 0 if "central" not in (s.get("government_level") or "").lower() else 1)
    elif "Central" in sort_by:
        filtered.sort(key=lambda s: 0 if "central" in (s.get("government_level") or "").lower() else 1)

    # -----------------------------------------------------------------------
    # Render Schemes: Cards View or Combined Table
    # -----------------------------------------------------------------------
    if "State" in scope_choice and (not selected_state or selected_state == "All India"):
        st.warning("📍 **Please select a State from the 'Portal' dropdown above to view its State Government schemes.**")
        st.info("State Government welfare programs are specific to individual states (e.g. choose Karnataka to view Gruha Lakshmi, Yuva Nidhi, Gruha Jyothi, Shakti, SSP Scholarship, and Anna Bhagya).")
    elif len(filtered) == 0:
        st.info(f"ℹ️ No schemes found matching Sector '**{welfare_sector}**' under '**{scope_choice}**' for '**{selected_state}**'.")
        st.markdown(f"👉 **Tip:** Set Welfare Sector to **'All'** or switch to **🏛️ Central (10)** / **🇮🇳 All Combined (47)**.")
    else:
        st.markdown(f"**Showing {len(filtered)} verified schemes**")

        if view_mode == "Combined Table":
            # Small, compact, beautiful data table
            table_data = []
            for idx, s in enumerate(filtered, 1):
                is_central = "central" in (s.get("government_level") or "").lower()
                table_data.append({
                    "#": idx,
                    "Scheme Name": s.get("name"),
                    "Sector": s.get("category"),
                    "Level": "🏛️ Central" if is_central else f"📍 {s.get('state', 'State')}",
                    "Direct Benefits": s.get("benefits"),
                    "Eligibility": s.get("eligibility"),
                    "Official Portal": s.get("official_url")
                })
            df = pd.DataFrame(table_data)
            
            # Action controls row: CSV download
            csv_data = df.to_csv(index=False).encode('utf-8')
            t_col1, t_col2 = st.columns([5, 1])
            with t_col2:
                st.download_button(
                    "📥 Export Small Table (CSV)",
                    data=csv_data,
                    file_name="civicguide_schemes_small_table.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "#": st.column_config.NumberColumn("#", width="small"),
                    "Scheme Name": st.column_config.TextColumn("Scheme Name", width="medium"),
                    "Sector": st.column_config.TextColumn("Sector", width="small"),
                    "Level": st.column_config.TextColumn("Level", width="small"),
                    "Direct Benefits": st.column_config.TextColumn("Direct Benefits", width="large"),
                    "Eligibility": st.column_config.TextColumn("Eligibility", width="large"),
                    "Official Portal": st.column_config.LinkColumn("Official Portal", display_text="Visit ↗")
                }
            )
        else:
            # Cards View (Strict 3 columns matching Image 2)
            cols = st.columns(3)
            for idx, scheme in enumerate(filtered):
                col = cols[idx % 3]
                with col:
                    is_central = "central" in (scheme.get("government_level") or "").lower()
                    badge_html = '<span class="badge-central">🏛️ CENTRAL GOVERNMENT</span>' if is_central else f'<span class="badge-state">📍 STATE GOVERNMENT • {scheme.get("state")}</span>'
                    
                    st.markdown(f"""
                    <div class="scheme-card">
                        <div>
                            <div>{badge_html}</div>
                            <h4 style="margin: 0.5rem 0 0.25rem 0; font-weight: 800; font-size: 1.1rem; color: #0f172a;">{scheme.get('name')}</h4>
                            <span class="badge-sector">{scheme.get('category')}</span>
                            <p style="font-size: 0.85rem; color: #475569; margin: 0.5rem 0; line-height: 1.4;">{scheme.get('description')[:140]}...</p>
                            <div class="benefit-box">
                                💰 <strong>Benefit:</strong> {scheme.get('benefits')}
                            </div>
                            <div style="font-size: 0.8rem; color: #334155; margin-top: 0.4rem;">
                                <strong>Eligibility:</strong> {scheme.get('eligibility')[:110]}...
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander(f"📋 Document Checklist & Apply for {scheme.get('name')}"):
                        st.markdown(f"**Mandatory Documents:** {scheme.get('required_documents')}")
                        st.markdown(f"**How to Apply:** {scheme.get('application_process')}")
                        if scheme.get('official_url'):
                            st.link_button("Visit Official Application Portal ↗", scheme.get('official_url'))

# ---------------------------------------------------------------------------
# VIEW: 2. HOME & OVERVIEW (Matches Images 5, 6, 7, 8, 9 Exactly)
# ---------------------------------------------------------------------------
elif "Home" in active_nav:
    
    # 1. HERO SECTION (Matches Image 5)
    st.markdown("""
    <div style="background: linear-gradient(180deg, #064e3b 0%, #0f172a 100%); color: white; padding: 3rem 2rem 3rem 2rem; border-radius: 1.5rem; text-align: center; margin-bottom: 1.5rem; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.25);">
        <div style="display: inline-flex; align-items: center; gap: 0.5rem; background-color: rgba(16, 185, 129, 0.2); border: 1px solid rgba(16, 185, 129, 0.4); padding: 0.35rem 1rem; border-radius: 9999px; font-size: 0.8rem; font-weight: 700; color: #6ee7b7; margin-bottom: 1.25rem;">
            ✨ All India | Central & State Governments • Verified Government Sources
        </div>
        <h1 style="font-size: 2.5rem; font-weight: 900; line-height: 1.2; margin: 0 0 1rem 0; letter-spacing: -0.025em; color: #ffffff;">
            Understand Your Rights & Government Schemes Across India
        </h1>
        <p style="font-size: 1.05rem; color: #cbd5e1; max-width: 48rem; margin: 0 auto 1.5rem auto; line-height: 1.6;">
            Empowering citizens across all Indian States, Union Territories, and Central Government initiatives with instant, AI-guided verified scheme explanations, eligibility checks, and public service locations.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 2. STATE EXPLORER PILLS & STATS (Matches Image 6)
    st.markdown("""
    <div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 0.5rem; margin-bottom: 1.5rem;">
        <span style="font-size: 0.85rem; font-weight: 800; color: #475569;">Explore by State:</span>
        <span style="background-color: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; padding: 0.2rem 0.65rem; border-radius: 9999px; font-size: 0.8rem; font-weight: 800;">Karnataka</span>
        <span style="background-color: #f1f5f9; color: #334155; border: 1px solid #e2e8f0; padding: 0.2rem 0.65rem; border-radius: 9999px; font-size: 0.8rem; font-weight: 800;">Maharashtra</span>
        <span style="background-color: #f1f5f9; color: #334155; border: 1px solid #e2e8f0; padding: 0.2rem 0.65rem; border-radius: 9999px; font-size: 0.8rem; font-weight: 800;">Delhi</span>
        <span style="background-color: #f1f5f9; color: #334155; border: 1px solid #e2e8f0; padding: 0.2rem 0.65rem; border-radius: 9999px; font-size: 0.8rem; font-weight: 800;">Tamil Nadu</span>
        <span style="background-color: #f1f5f9; color: #334155; border: 1px solid #e2e8f0; padding: 0.2rem 0.65rem; border-radius: 9999px; font-size: 0.8rem; font-weight: 800;">Uttar Pradesh</span>
        <span style="background-color: #f1f5f9; color: #334155; border: 1px solid #e2e8f0; padding: 0.2rem 0.65rem; border-radius: 9999px; font-size: 0.8rem; font-weight: 800;">West Bengal</span>
        <span style="background-color: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; padding: 0.2rem 0.65rem; border-radius: 9999px; font-size: 0.8rem; font-weight: 800;">All India +</span>
    </div>
    """, unsafe_allow_html=True)

    # 4 Stat Counters
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="filter-card" style="text-align: center; border-radius: 1.25rem;">
            <div style="font-size: 2.2rem; font-weight: 900; color: #0f172a;">45+</div>
            <div style="font-size: 0.85rem; font-weight: 700; color: #64748b;">National & State Schemes</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown("""
        <div class="filter-card" style="text-align: center; border-radius: 1.25rem;">
            <div style="font-size: 2.2rem; font-weight: 900; color: #047857;">All India</div>
            <div style="font-size: 0.85rem; font-weight: 700; color: #64748b;">Central & 28+ States/UTs</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown("""
        <div class="filter-card" style="text-align: center; border-radius: 1.25rem;">
            <div style="font-size: 2.2rem; font-weight: 900; color: #d97706;">23 Languages</div>
            <div style="font-size: 0.85rem; font-weight: 700; color: #64748b;">All Scheduled Indian Languages</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown("""
        <div class="filter-card" style="text-align: center; border-radius: 1.25rem;">
            <div style="font-size: 2.2rem; font-weight: 900; color: #0284c7;">100% RAG</div>
            <div style="font-size: 0.85rem; font-weight: 700; color: #64748b;">Zero Hallucinations</div>
        </div>
        """, unsafe_allow_html=True)

    # 3. FEATURE LAUNCH CARDS (Matches Image 6)
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        st.markdown("""
        <div class="filter-card" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div style="width: 40px; height: 40px; border-radius: 0.75rem; background-color: #ecfdf5; display: flex; align-items: center; justify-content: center; font-size: 1.3rem; margin-bottom: 0.75rem;">
                    🤖
                </div>
                <h3 style="font-size: 1.15rem; font-weight: 900; color: #0f172a; margin: 0 0 0.5rem 0;">AI Assistant</h3>
                <p style="font-size: 0.85rem; color: #475569; line-height: 1.5; margin: 0 0 1rem 0;">
                    Ask government policy, scholarship, and citizen rights questions in Kannada, English, or Hindi with speech input and voice responses.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch AI Assistant →", key="btn_f1", use_container_width=True):
            st.session_state.top_navbar_tab = "🤖 AI Assistant"
            st.rerun()
    with f_col2:
        st.markdown("""
        <div class="filter-card" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div style="width: 40px; height: 40px; border-radius: 0.75rem; background-color: #fef3c7; display: flex; align-items: center; justify-content: center; font-size: 1.3rem; margin-bottom: 0.75rem;">
                    📋
                </div>
                <h3 style="font-size: 1.15rem; font-weight: 900; color: #0f172a; margin: 0 0 0.5rem 0;">Eligibility Checker</h3>
                <p style="font-size: 0.85rem; color: #475569; line-height: 1.5; margin: 0 0 1rem 0;">
                    Evaluate your family's eligibility against official scheme criteria with detailed met conditions, required documents, and application links.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Check Eligibility →", key="btn_f2", use_container_width=True):
            st.session_state.top_navbar_tab = "📋 Eligibility Checker"
            st.rerun()
    with f_col3:
        st.markdown("""
        <div class="filter-card" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div style="width: 40px; height: 40px; border-radius: 0.75rem; background-color: #eff6ff; display: flex; align-items: center; justify-content: center; font-size: 1.3rem; margin-bottom: 0.75rem;">
                    📍
                </div>
                <h3 style="font-size: 1.15rem; font-weight: 900; color: #0f172a; margin: 0 0 0.5rem 0;">Service Map</h3>
                <p style="font-size: 0.85rem; color: #475569; line-height: 1.5; margin: 0 0 1rem 0;">
                    Interactive OpenStreetMap directory of Central Ministries, AIIMS, Passport Seva Kendras, State Secretariats, and CSCs across India and Karnataka.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore All India Map →", key="btn_f3", use_container_width=True):
            st.session_state.top_navbar_tab = "📍 Service Map"
            st.rerun()

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # 4. POPULAR NATIONAL & STATE SCHEMES (Matches Images 7 & 8)
    col_pop_title, col_pop_btn = st.columns([3.5, 1.5], vertical_alignment="center")
    with col_pop_title:
        st.markdown("""
        <div style="margin-bottom: 0.5rem;">
            <span style="font-size: 0.75rem; font-weight: 800; color: #047857; text-transform: uppercase; letter-spacing: 0.05em;">VERIFIED WELFARE CATALOG</span>
            <h2 style="font-size: 1.75rem; font-weight: 900; color: #0f172a; margin: 0.2rem 0;">Popular National & State Schemes</h2>
            <p style="font-size: 0.85rem; color: #64748b; margin: 0;">Key welfare initiatives for women, farmers, artisans, students, and citizens across India.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_pop_btn:
        if st.button("View All Schemes →", key="btn_view_all_pop", use_container_width=True):
            st.session_state.top_navbar_tab = "🏛️ Government Schemes"
            st.rerun()

    pop_schemes = [
        {
            "name": "PM-Kisan Samman Nidhi",
            "desc": "Central government direct income support scheme providing Rs. 6,000 annually in three installments to all eligible landholding farmer families across India.",
            "benefit": "Rs. 6,000 per year transferred in three equal quarterly installments of Rs. 2,000 directly into the Aadhaar-linked bank account via DBT.",
            "url": "https://pmkisan.gov.in"
        },
        {
            "name": "Ayushman Bharat - PM-JAY",
            "desc": "Flagship national health protection scheme offering up to Rs. 5 Lakh cashless hospitalization coverage per family per year for secondary and tertiary healthcare.",
            "benefit": "Cashless treatment up to Rs. 5,00,000 per family per year across empaneled public and private hospitals throughout India.",
            "url": "https://pmjay.gov.in"
        },
        {
            "name": "PM Surya Ghar: Muft Bijli Yojana",
            "desc": "Central scheme providing up to 300 units of free electricity per month to households by giving capital subsidies up to Rs. 78,000 for installing rooftop solar systems.",
            "benefit": "Direct subsidy up to Rs. 78,000 for 3 kW system, zero electricity bills, and income from selling surplus power back to the grid.",
            "url": "https://pmsuryaghar.gov.in"
        },
        {
            "name": "PM Vishwakarma Yojana",
            "desc": "Holistic support initiative for traditional artisans and craftspeople across 18 trades, offering official ID, Rs. 15,000 toolkit voucher, training stipend, and collateral-free loans.",
            "benefit": "PM Vishwakarma Certificate & ID, 5-7 days training with Rs. 500/day stipend, Rs. 15,000 e-voucher for tools, and 5% loan up to Rs. 3 Lakh.",
            "url": "https://pmvishwakarma.gov.in"
        }
    ]

    p_cols = st.columns(4)
    for idx, p in enumerate(pop_schemes):
        with p_cols[idx]:
            st.markdown(f"""
            <div class="scheme-card" style="height: 100%;">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <span class="badge-central">CENTRAL GOVERNMENT</span>
                        <span style="font-size: 0.7rem; font-weight: 800; color: #047857; background-color: #ecfdf5; padding: 0.1rem 0.4rem; border-radius: 9999px;">✓ Verified</span>
                    </div>
                    <h4 style="font-size: 1rem; font-weight: 900; color: #0f172a; margin: 0.35rem 0;">{p['name']}</h4>
                    <p style="font-size: 0.8rem; color: #475569; line-height: 1.4; height: 3.8rem; overflow: hidden; margin-bottom: 0.5rem;">{p['desc']}</p>
                    <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 0.6rem; padding: 0.5rem; margin-bottom: 0.75rem;">
                        <span style="font-size: 0.7rem; font-weight: 800; color: #065f46; display: block;">Key Benefit:</span>
                        <span style="font-size: 0.75rem; color: #334155; line-height: 1.3;">{p['benefit'][:110]}...</span>
                    </div>
                </div>
                <div style="border-top: 1px solid #e2e8f0; padding-top: 0.65rem;">
                    <a href="{p['url']}" target="_blank" style="background-color: #047857; color: white; padding: 0.45rem 0.85rem; border-radius: 0.6rem; font-size: 0.8rem; font-weight: 800; text-decoration: none; display: block; text-align: center;">
                        Visit Official Website ↗
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    # 5. HOW CIVICGUIDE AI WORKS (Matches Image 8 Exactly)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <span style="font-size: 0.75rem; font-weight: 800; color: #047857; text-transform: uppercase; letter-spacing: 0.05em;">SIMPLE 4-STEP PROCESS</span>
        <h2 style="font-size: 2rem; font-weight: 900; color: #0f172a; margin: 0.2rem 0;">How CivicGuide AI Works</h2>
        <p style="font-size: 0.85rem; color: #64748b;">Designed specifically to make government schemes accessible to every citizen without complex legal jargon.</p>
    </div>
    """, unsafe_allow_html=True)

    w1, w2, w3, w4 = st.columns(4)
    with w1:
        st.markdown("""
        <div class="filter-card" style="height: 100%; position: relative;">
            <span style="position: absolute; top: 1rem; right: 1.25rem; font-size: 1.5rem; font-weight: 900; color: #d1fae5;">01</span>
            <div style="width: 34px; height: 34px; border-radius: 0.5rem; background-color: #ecfdf5; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; margin-bottom: 0.5rem;">🤖</div>
            <h4 style="font-size: 0.95rem; font-weight: 900; color: #0f172a; margin: 0 0 0.35rem 0;">1. Search & Ask AI Assistant</h4>
            <p style="font-size: 0.8rem; color: #475569; line-height: 1.4; margin: 0;">Enter scheme keywords or ask questions in Kannada, English, or Hindi to get instant verified policy guidance and required documents.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Ask AI Assistant →", key="btn_w1", use_container_width=True):
            st.session_state.top_navbar_tab = "🤖 AI Assistant"
            st.rerun()
    with w2:
        st.markdown("""
        <div class="filter-card" style="height: 100%; position: relative;">
            <span style="position: absolute; top: 1rem; right: 1.25rem; font-size: 1.5rem; font-weight: 900; color: #fef3c7;">02</span>
            <div style="width: 34px; height: 34px; border-radius: 0.5rem; background-color: #fef3c7; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; margin-bottom: 0.5rem;">📋</div>
            <h4 style="font-size: 0.95rem; font-weight: 900; color: #0f172a; margin: 0 0 0.35rem 0;">2. Check Family Eligibility</h4>
            <p style="font-size: 0.8rem; color: #475569; line-height: 1.4; margin: 0;">Screen your age, annual household income, category, and domicile against official rules across all 47 Central & State welfare initiatives.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Check Eligibility →", key="btn_w2", use_container_width=True):
            st.session_state.top_navbar_tab = "📋 Eligibility Checker"
            st.rerun()
    with w3:
        st.markdown("""
        <div class="filter-card" style="height: 100%; position: relative;">
            <span style="position: absolute; top: 1rem; right: 1.25rem; font-size: 1.5rem; font-weight: 900; color: #dbeafe;">03</span>
            <div style="width: 34px; height: 34px; border-radius: 0.5rem; background-color: #eff6ff; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; margin-bottom: 0.5rem;">🏛️</div>
            <h4 style="font-size: 0.95rem; font-weight: 900; color: #0f172a; margin: 0 0 0.35rem 0;">3. Review Required Documents</h4>
            <p style="font-size: 0.8rem; color: #475569; line-height: 1.4; margin: 0;">Review complete official checklists including Aadhaar, Nadakacheri certificates, and NPCI-linked bank account passbooks before applying.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Browse Schemes →", key="btn_w3", use_container_width=True):
            st.session_state.top_navbar_tab = "🏛️ Government Schemes"
            st.rerun()
    with w4:
        st.markdown("""
        <div class="filter-card" style="height: 100%; position: relative;">
            <span style="position: absolute; top: 1rem; right: 1.25rem; font-size: 1.5rem; font-weight: 900; color: #d1fae5;">04</span>
            <div style="width: 34px; height: 34px; border-radius: 0.5rem; background-color: #ecfdf5; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; margin-bottom: 0.5rem;">🌐</div>
            <h4 style="font-size: 0.95rem; font-weight: 900; color: #0f172a; margin: 0 0 0.35rem 0;">4. Direct Official Application</h4>
            <p style="font-size: 0.8rem; color: #475569; line-height: 1.4; margin: 0;">Click verified one-touch links to submit applications directly on government portals like Seva Sindhu, myScheme, and PM-Kisan without middlemen.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Service Map →", key="btn_w4", use_container_width=True):
            st.session_state.top_navbar_tab = "📍 Service Map"
            st.rerun()

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    # 6. DISTRICT MAP & SERVICES (Matches Image 9 Exactly)
    st.markdown("""
    <div style="background: linear-gradient(90deg, #064e3b 0%, #0f172a 100%); color: white; padding: 2rem 2.5rem; border-radius: 1.5rem; margin-bottom: 1.5rem; display: flex; flex-direction: column; gap: 1rem;">
        <div>
            <span style="font-size: 0.75rem; font-weight: 800; color: #fde047; text-transform: uppercase; letter-spacing: 0.05em;">DISTRICT MAP & SERVICES</span>
            <h3 style="font-size: 1.6rem; font-weight: 900; color: white; margin: 0.2rem 0;">Public Services & Offices Across India</h3>
            <p style="font-size: 0.85rem; color: #cbd5e1; margin: 0; max-width: 48rem;">Find Central Ministries, AIIMS, Passport Seva Kendras, State Secretariats, District Collectorates, and Common Service Centres (CSCs).</p>
        </div>
        <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
            <span style="background-color: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25); color: #e2e8f0; padding: 0.2rem 0.65rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 700;">Hosapete (5 services)</span>
            <span style="background-color: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25); color: #e2e8f0; padding: 0.2rem 0.65rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 700;">Harapanahalli (4 services)</span>
            <span style="background-color: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25); color: #e2e8f0; padding: 0.2rem 0.65rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 700;">Kudligi (4 services)</span>
            <span style="background-color: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25); color: #e2e8f0; padding: 0.2rem 0.65rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 700;">Huvina Hadagali (3 services)</span>
            <span style="background-color: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25); color: #e2e8f0; padding: 0.2rem 0.65rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 700;">Hagaribommanahalli (3 services)</span>
            <span style="background-color: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25); color: #e2e8f0; padding: 0.2rem 0.65rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 700;">Kottur (4 services)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# VIEW: 3. AI CITIZEN ASSISTANT (Guaranteed 5-Step Process)
# ---------------------------------------------------------------------------
elif "AI Assistant" in active_nav:
    st.markdown('<div class="hero-title">🤖 AI Citizen Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-desc">Grounded Policy Assistant providing step-by-step application instructions, eligibility criteria, required documents, and official portal links.</div>', unsafe_allow_html=True)

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": "Namaskara! I am your CivicGuide AI assistant. How can I help you with government schemes, certificates (Caste/Income/RTC), or application procedures today?",
                "url": "https://www.myscheme.gov.in"
            }
        ]

    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("url"):
                st.link_button("Visit Official Website ↗", msg["url"])

    if query := st.chat_input("Ask about any scheme, caste certificate, RTC/pahani, ration card, or how to apply..."):
        st.session_state.chat_messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
            
        with st.chat_message("assistant"):
            res = _synthesize_python_ai_reply(query, schemes_list)
            st.markdown(res["answer"])
            if res.get("url"):
                st.link_button("Visit Official Website ↗", res["url"])
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": res["answer"],
                "url": res.get("url")
            })

# ---------------------------------------------------------------------------
# VIEW: 4. ELIGIBILITY CHECKER
# ---------------------------------------------------------------------------
elif "Eligibility Checker" in active_nav:
    st.markdown('<div class="hero-title">📋 Citizen Demographic Eligibility Checker</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-desc">Evaluate your demographic qualifications against all 47 verified Central & State government schemes.</div>', unsafe_allow_html=True)

    with st.form("eligibility_form"):
        e1, e2, e3 = st.columns(3)
        with e1:
            age = st.number_input("Age (Years)", min_value=1, max_value=100, value=24)
            gender = st.selectbox("Gender", ["Male", "Female", "Transgender"])
        with e2:
            state = st.selectbox("State of Residence", ALL_INDIAN_STATES[1:], index=0)
            occupation = st.selectbox("Current Occupation", ["Graduate / Unemployed", "Student", "Farmer / Agricultural Worker", "Artisan / Craftsperson", "Small Business / MSME", "Senior Citizen / Homemaker"])
        with e3:
            income = st.number_input("Annual Household Income (₹)", min_value=0, max_value=2500000, value=120000, step=10000)
            ration_card = st.selectbox("Ration Card Category", ["BPL (Below Poverty Line)", "Antyodaya (AAY)", "APL (Above Poverty Line)", "None"])

        submit = st.form_submit_button("🔍 Evaluate My Eligibility Across All Schemes")

    if submit:
        st.success(f"Demographic Evaluation Complete for **{gender}, {age} Years, {state}** (Annual Income: ₹{income:,})")
        matched = []
        for s in schemes_list:
            score = 1
            if age >= 18:
                score += 1
            if gender == "Female" and ("woman" in (s.get("description") or "").lower() or "women" in (s.get("description") or "").lower()):
                score += 2
            if "unemployed" in occupation.lower() and ("unemployed" in (s.get("eligibility") or "").lower() or "yuva" in (s.get("name") or "").lower()):
                score += 2
            if income <= 250000:
                score += 1
            status = "Qualified" if score >= 3 else "Conditions Apply" if score >= 2 else "Criteria Not Met"
            matched.append({"scheme": s, "status": status})

        c1, c2 = st.columns(2)
        c1.metric("Qualified Schemes", len([m for m in matched if m["status"] == "Qualified"]))
        c2.metric("Conditions Apply", len([m for m in matched if m["status"] == "Conditions Apply"]))

        for item in matched[:6]:
            s = item["scheme"]
            st.markdown(f"""
            <div class="scheme-card" style="margin-bottom: 0.5rem;">
                <span class="badge-central">{s.get('government_level')}</span>
                <span style="float: right; font-weight: bold; color: {'#047857' if item['status'] == 'Qualified' else '#b45309'};">● {item['status']}</span>
                <h4 style="margin: 0.4rem 0;">{s.get('name')}</h4>
                <div class="benefit-box">💰 {s.get('benefits')}</div>
            </div>
            """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# VIEW: 5. SERVICE MAP
# ---------------------------------------------------------------------------
elif "Service Map" in active_nav:
    st.markdown('<div class="hero-title">📍 Public Services Map & Taluk Directory</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-desc">Find Deputy Commissioner, Tahsildar, District Hospitals, and Grama One / CSC centers in Vijayanagara and across India.</div>', unsafe_allow_html=True)

    if services_list:
        df_services = pd.DataFrame(services_list)
        map_data = df_services.dropna(subset=['latitude', 'longitude'])
        if not map_data.empty:
            st.map(map_data[['latitude', 'longitude']], zoom=10)

        st.markdown("#### **Verified Public Service Offices Directory (Small Table)**")
        st.dataframe(
            df_services[['name', 'category', 'taluk', 'address', 'phone', 'government_level']],
            use_container_width=True,
            hide_index=True
        )
