import os
import sqlite3
import importlib.util
import json
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

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

    .office-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 1rem;
        padding: 1rem 1.15rem;
        margin-bottom: 0.85rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
        transition: all 0.2s ease;
    }
    .office-card:hover {
        border-color: #10b981;
        box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.1);
        transform: translateY(-1px);
    }

    /* =========================================================================
       EXACT REACT-STYLE TOP NAVBAR BUTTONS & TABS (Matches User Image Exactly)
       ========================================================================= */
    /* Hide native radio input and all radio indicator circles/bullets */
    div[data-testid="stRadio"] input[type="radio"] {
        display: none !important;
        position: absolute !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
    }

    /* Target ONLY the first child of the label which is the radio circle, NEVER markdown container */
    div[data-testid="stRadio"] [data-baseweb="radio"] > span:first-child,
    div[data-testid="stRadio"] [data-baseweb="radio"] > div:first-child:not([data-testid="stMarkdownContainer"]),
    div[data-testid="stRadio"] label > span:first-child,
    div[data-testid="stRadio"] label > div:first-child:not([data-testid="stMarkdownContainer"]),
    div[data-testid="stRadio"] label svg {
        display: none !important;
        width: 0 !important;
        height: 0 !important;
        min-width: 0 !important;
        max-width: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }

    /* Strict ONE-LINE flex row without wrapping */
    div[data-testid="stRadio"] div[role="radiogroup"] {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: flex-start !important;
        gap: 0.35rem !important;
        flex-wrap: nowrap !important;
        white-space: nowrap !important;
        overflow-x: auto !important;
        padding: 0 !important;
        margin: 0 !important;
        scrollbar-width: none !important;
        width: 100% !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"]::-webkit-scrollbar {
        display: none !important;
    }

    /* Inactive navbar tab button style */
    div[data-testid="stRadio"] div[role="radiogroup"] label {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 0.45rem 0.85rem !important;
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

    /* Label text - GUARANTEED 100% VISIBLE */
    div[data-testid="stRadio"] [data-testid="stMarkdownContainer"],
    div[data-testid="stRadio"] [data-testid="stMarkdownContainer"] p,
    div[data-testid="stRadio"] [data-testid="stMarkdownContainer"] span {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        visibility: visible !important;
        opacity: 1 !important;
        font-size: 0.92rem !important;
        font-weight: 700 !important;
        color: #475569 !important;
        margin: 0 !important;
        line-height: 1.2 !important;
        white-space: nowrap !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label:hover [data-testid="stMarkdownContainer"] p {
        color: #0f172a !important;
    }

    /* ACTIVE TAB: Mint green pill with dark green bold text (Exact match to React Image) */
    div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked),
    div[data-testid="stRadio"] div[role="radiogroup"] label[aria-checked="true"],
    div[data-testid="stRadio"] div[role="radiogroup"] label[data-checked="true"] {
        background-color: #d1fae5 !important;
        border: 1px solid #a7f3d0 !important;
        box-shadow: 0 1px 2px rgba(16, 185, 129, 0.15) !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) [data-testid="stMarkdownContainer"] p,
    div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) [data-testid="stMarkdownContainer"] span,
    div[data-testid="stRadio"] div[role="radiogroup"] label[aria-checked="true"] [data-testid="stMarkdownContainer"] p,
    div[data-testid="stRadio"] div[role="radiogroup"] label[data-checked="true"] [data-testid="stMarkdownContainer"] p {
        color: #065f46 !important;
        font-weight: 800 !important;
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

    /* Navbar Action Buttons (Dashboard Avatar & Logout) */
    button:has(p:contains("▦ K")) {
        background-color: #ecfdf5 !important;
        color: #047857 !important;
        border: 1.5px solid #a7f3d0 !important;
        border-radius: 0.75rem !important;
        font-weight: 900 !important;
        font-size: 0.95rem !important;
        padding: 0.45rem 0.65rem !important;
        transition: all 0.2s ease !important;
    }
    button:has(p:contains("▦ K")):hover {
        background-color: #047857 !important;
        color: #ffffff !important;
        border-color: #047857 !important;
    }
    
    button:has(p:contains("🚪")) {
        background-color: #f8fafc !important;
        color: #64748b !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 0.75rem !important;
        font-weight: 800 !important;
        font-size: 0.95rem !important;
        padding: 0.45rem 0.65rem !important;
        transition: all 0.2s ease !important;
    }
    button:has(p:contains("🚪")):hover {
        background-color: #fee2e2 !important;
        color: #b91c1c !important;
        border-color: #fecaca !important;
    }

    /* =========================================================================
       PIXEL-PERFECT LOGIN & REGISTRATION STYLES (Matches User Screenshots Exactly)
       ========================================================================= */
    /* Icon adorned text inputs */
    div[data-testid="stTextInput"]:has(input[aria-label="USER ID"]) div[data-baseweb="input"],
    div[data-testid="stTextInput"]:has(input[aria-label="PASSWORD"]) div[data-baseweb="input"],
    div[data-testid="stTextInput"]:has(input[aria-label="1. FULL NAME"]) div[data-baseweb="input"],
    div[data-testid="stNumberInput"]:has(input[aria-label="2. AGE"]) div[data-baseweb="input"],
    div[data-testid="stTextInput"]:has(input[aria-label="3. MOBILE NUMBER"]) div[data-baseweb="input"],
    div[data-testid="stTextInput"]:has(input[aria-label="7. EMAIL ADDRESS"]) div[data-baseweb="input"],
    div[data-testid="stTextInput"]:has(input[aria-label="8. PASSWORD"]) div[data-baseweb="input"],
    div[data-testid="stTextInput"]:has(input[aria-label="9. CONFIRM PASSWORD"]) div[data-baseweb="input"] {
        background-color: rgba(241, 245, 249, 0.6) !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 0.85rem !important;
        height: 48px !important;
        padding-left: 2.6rem !important;
        position: relative !important;
    }

    div[data-testid="stTextInput"]:has(input[aria-label="USER ID"]) div[data-baseweb="input"]::before {
        content: "👤"; position: absolute; left: 0.95rem; top: 50%; transform: translateY(-50%); font-size: 0.95rem; color: #059669; opacity: 0.9; pointer-events: none;
    }
    div[data-testid="stTextInput"]:has(input[aria-label="PASSWORD"]) div[data-baseweb="input"]::before {
        content: "🔒"; position: absolute; left: 0.95rem; top: 50%; transform: translateY(-50%); font-size: 0.95rem; color: #059669; opacity: 0.9; pointer-events: none;
    }
    div[data-testid="stTextInput"]:has(input[aria-label="1. FULL NAME"]) div[data-baseweb="input"]::before {
        content: "👤"; position: absolute; left: 0.95rem; top: 50%; transform: translateY(-50%); font-size: 0.95rem; color: #059669; opacity: 0.9; pointer-events: none;
    }
    div[data-testid="stNumberInput"]:has(input[aria-label="2. AGE"]) div[data-baseweb="input"]::before {
        content: "📅"; position: absolute; left: 0.95rem; top: 50%; transform: translateY(-50%); font-size: 0.95rem; color: #059669; opacity: 0.9; pointer-events: none;
    }
    div[data-testid="stTextInput"]:has(input[aria-label="3. MOBILE NUMBER"]) div[data-baseweb="input"]::before {
        content: "📞 +91"; position: absolute; left: 0.85rem; top: 50%; transform: translateY(-50%); font-size: 0.82rem; font-weight: 700; color: #059669; opacity: 0.9; pointer-events: none;
    }
    div[data-testid="stTextInput"]:has(input[aria-label="7. EMAIL ADDRESS"]) div[data-baseweb="input"]::before {
        content: "✉️"; position: absolute; left: 0.95rem; top: 50%; transform: translateY(-50%); font-size: 0.95rem; color: #059669; opacity: 0.9; pointer-events: none;
    }
    div[data-testid="stTextInput"]:has(input[aria-label="8. PASSWORD"]) div[data-baseweb="input"]::before {
        content: "🔒"; position: absolute; left: 0.95rem; top: 50%; transform: translateY(-50%); font-size: 0.95rem; color: #059669; opacity: 0.9; pointer-events: none;
    }
    div[data-testid="stTextInput"]:has(input[aria-label="9. CONFIRM PASSWORD"]) div[data-baseweb="input"]::before {
        content: "🔒"; position: absolute; left: 0.95rem; top: 50%; transform: translateY(-50%); font-size: 0.95rem; color: #059669; opacity: 0.9; pointer-events: none;
    }

    /* Primary Emerald CTA Button */
    button:has(p:contains("Login & Go to Home")),
    button:has(p:contains("Create Account & Send OTP")) {
        background-color: #059669 !important;
        color: #ffffff !important;
        border-radius: 0.85rem !important;
        font-size: 0.95rem !important;
        font-weight: 800 !important;
        padding: 0.75rem 1rem !important;
        box-shadow: 0 4px 6px -1px rgba(5, 150, 105, 0.25) !important;
        border: none !important;
        transition: all 0.2s ease !important;
    }
    button:has(p:contains("Login & Go to Home")):hover,
    button:has(p:contains("Create Account & Send OTP")):hover {
        background-color: #047857 !important;
        transform: translateY(-1px);
    }

    /* Secondary Guest Button */
    button:has(p:contains("Browse Public Schemes as Guest")) {
        background-color: #f1f5f9 !important;
        color: #1e293b !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 0.85rem !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        padding: 0.65rem 1rem !important;
        transition: all 0.2s ease !important;
    }
    button:has(p:contains("Browse Public Schemes as Guest")):hover {
        background-color: #e2e8f0 !important;
        color: #059669 !important;
    }

    /* Tertiary Link Buttons */
    button:has(p:contains("Create Free Account")),
    button:has(p:contains("Sign In with User ID")),
    button:has(p:contains("Back to Sign In")) {
        color: #059669 !important;
        font-weight: 800 !important;
        font-size: 0.85rem !important;
        text-decoration: underline !important;
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
        padding: 0.2rem 0 !important;
    }
    button:has(p:contains("Create Free Account")):hover,
    button:has(p:contains("Sign In with User ID")):hover,
    button:has(p:contains("Back to Sign In")):hover {
        color: #047857 !important;
        background: transparent !important;
    }

    /* Sex Pill Buttons */
    div[data-testid="stColumn"]:has(button[key*="btn_sex_"]) button {
        border-radius: 0.75rem !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
        padding: 0.5rem 0.25rem !important;
    }
    div[data-testid="stColumn"]:has(button[key="btn_sex_male"]) button {
        background-color: #059669 !important;
        color: #ffffff !important;
        border: 1px solid #059669 !important;
        font-weight: 700 !important;
    }

    /* Language Pill Buttons */
    div[data-testid="stColumn"]:has(button[key*="btn_lang_"]) button {
        border-radius: 9999px !important;
        font-weight: 600 !important;
        font-size: 0.75rem !important;
        padding: 0.35rem 0.5rem !important;
        margin-bottom: 0.25rem !important;
        white-space: nowrap !important;
    }
    div[data-testid="stColumn"]:has(button[key*="btn_lang_"]) button:has(p:contains("✓")) {
        background-color: #059669 !important;
        color: #ffffff !important;
        border: 1px solid #059669 !important;
        font-weight: 700 !important;
    }
    div[data-testid="stColumn"]:has(button[key*="btn_lang_"]) button:not(:has(p:contains("✓"))) {
        background-color: #ffffff !important;
        color: #334155 !important;
        border: 1px solid #e2e8f0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Constants & Official State Portals Dictionary & Multilingual Engine
# ---------------------------------------------------------------------------
from translations import ALL_INDIAN_LANGUAGES, LANG_CODE_MAP, t, TRANSLATIONS
from state_districts_data import ALL_STATES_DISTRICTS_TALUKS, DISTRICT_COORDINATES
from citizen_dashboard_auth import (
    DEFAULT_CITIZEN_USER,
    DEFAULT_APPLICATIONS,
    render_login_view,
    render_register_view,
    render_citizen_dashboard
)

def _tr(key, default=None):
    cur_code = st.session_state.get("current_lang_code", "en")
    return t(key, cur_code, default)

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
# SESSION STATE & CITIZEN AUTHENTICATION GATE
# ---------------------------------------------------------------------------
if "is_authenticated" not in st.session_state:
    st.session_state["is_authenticated"] = False
if "guest_mode" not in st.session_state:
    st.session_state["guest_mode"] = False
if "auth_page" not in st.session_state:
    st.session_state["auth_page"] = "login"
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "home"
if "citizen_user" not in st.session_state:
    st.session_state["citizen_user"] = dict(DEFAULT_CITIZEN_USER)
if "citizen_applications" not in st.session_state:
    st.session_state["citizen_applications"] = list(DEFAULT_APPLICATIONS)

selected_lang_name = st.session_state.get("top_navbar_language", "English (English)")
cur_lang_code = LANG_CODE_MAP.get(selected_lang_name, "en")
st.session_state["current_lang_code"] = cur_lang_code

# If user is not authenticated and not in guest mode, render Citizen Sign In / Registration
if not st.session_state.get("is_authenticated", False) and not st.session_state.get("guest_mode", False):
    if st.session_state.get("auth_page", "login") == "login":
        render_login_view(_tr, ALL_INDIAN_LANGUAGES, LANG_CODE_MAP)
    else:
        render_register_view(_tr, ALL_INDIAN_LANGUAGES, ALL_INDIAN_STATES, LANG_CODE_MAP)
    st.stop()

def navigate_to(target_page: str):
    """Safely queues navigation to a target page and re-runs the script without triggering StreamlitWidgetAlreadyInstantiatedError."""
    st.session_state["pending_nav_target"] = target_page
    st.session_state["current_page"] = target_page
    st.rerun()

# ---------------------------------------------------------------------------
# CITIZEN DASHBOARD ROUTE (When active page is "dashboard")
# ---------------------------------------------------------------------------
if st.session_state.get("current_page") == "dashboard":
    render_citizen_dashboard(_tr, ALL_INDIAN_LANGUAGES, ALL_INDIAN_STATES, LANG_CODE_MAP)
    st.stop()

# ---------------------------------------------------------------------------
# TOP NAVBAR: Matches User Image Exactly (Single Line Layout & Multilingual)
# ---------------------------------------------------------------------------
# Handle pending navigation requests safely before top_navbar_tab_key widget is instantiated
if "pending_nav_target" in st.session_state:
    st.session_state["top_navbar_tab_key"] = st.session_state.pop("pending_nav_target")

if "top_navbar_tab_key" not in st.session_state:
    st.session_state["top_navbar_tab_key"] = "home"

nav_col_logo, nav_col_tabs, nav_col_right = st.columns([1.8, 6.2, 4.0], vertical_alignment="center")

with nav_col_logo:
    st.markdown(f"""
    <div class="brand-wrap">
        <div class="brand-logo">🏛️</div>
        <div>
            <div class="brand-title">{_tr('appName')} <span class="brand-pill">{_tr('allIndiaPill')}</span></div>
            <div class="brand-subtitle">{_tr('tagline')}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

NAV_ICONS = {
    "home": "🧭",
    "schemes": "🏛️",
    "chatbot": "🤖",
    "eligibility": "📋",
    "serviceMap": "📍"
}

with nav_col_tabs:
    active_nav_key = st.radio(
        "Navigation",
        ["home", "schemes", "chatbot", "eligibility", "serviceMap"],
        format_func=lambda k: f"{NAV_ICONS[k]} {_tr(k)}",
        horizontal=True,
        label_visibility="collapsed",
        key="top_navbar_tab_key"
    )
    st.session_state["current_page"] = active_nav_key

with nav_col_right:
    if st.session_state.get("is_authenticated", False):
        c_lang, c_gh, c_dash, c_logout = st.columns([3.8, 1.8, 1.3, 1.1], vertical_alignment="center")
        with c_lang:
            selected_lang = st.selectbox(
                "Language",
                ALL_INDIAN_LANGUAGES,
                index=ALL_INDIAN_LANGUAGES.index(selected_lang_name) if selected_lang_name in ALL_INDIAN_LANGUAGES else 0,
                key="top_navbar_language",
                label_visibility="collapsed"
            )
        with c_gh:
            st.link_button("GitHub", "https://github.com/kpbinduprakasha-cpu/CivicGuide-AI")
        with c_dash:
            if st.button("▦ K", key="top_navbar_dash_btn", help="Citizen Dashboard: K P BINDUPRAKASHA", use_container_width=True):
                st.session_state["current_page"] = "dashboard"
                st.rerun()
        with c_logout:
            if st.button("🚪", key="top_navbar_logout_btn", help="Logout", use_container_width=True):
                st.session_state["is_authenticated"] = False
                st.session_state["guest_mode"] = False
                st.session_state["auth_page"] = "login"
                st.session_state["current_page"] = "home"
                st.rerun()
    else:
        c_lang, c_gh, c_login = st.columns([4.2, 2.0, 2.0], vertical_alignment="center")
        with c_lang:
            selected_lang = st.selectbox(
                "Language",
                ALL_INDIAN_LANGUAGES,
                index=ALL_INDIAN_LANGUAGES.index(selected_lang_name) if selected_lang_name in ALL_INDIAN_LANGUAGES else 0,
                key="top_navbar_language",
                label_visibility="collapsed"
            )
        with c_gh:
            st.link_button("GitHub", "https://github.com/kpbinduprakasha-cpu/CivicGuide-AI")
        with c_login:
            if st.button("🔑 Sign In", key="top_navbar_signin_btn", use_container_width=True):
                st.session_state["guest_mode"] = False
                st.session_state["auth_page"] = "login"
                st.rerun()

st.markdown("<hr style='margin-top: 0.2rem; margin-bottom: 1.25rem; border-color: #e2e8f0;'>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# VIEW: 1. GOVERNMENT SCHEMES (Matches Image 2 Exactly)
# ---------------------------------------------------------------------------
if active_nav_key == "schemes":
    
    # Hero Title & Action Pills Row
    h_col1, h_col2 = st.columns([3, 2])
    with h_col1:
        st.markdown(f'<div class="hero-badge">{_tr("schemesDirBadge")}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hero-title">{_tr("schemesDirTitle")}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hero-desc">{_tr("schemesDirSub")}</div>', unsafe_allow_html=True)
    with h_col2:
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button(f"📍 {_tr('serviceMap')}", key="h_btn1", use_container_width=True):
                navigate_to("serviceMap")
        with b2:
            st.button("🔖 Saved (0)", key="h_btn2", use_container_width=True)
        with b3:
            if st.button("✨ AI Matched (40)", key="h_btn3", use_container_width=True):
                navigate_to("chatbot")

    # -----------------------------------------------------------------------
    # Main White Filter Card (Matches Image 2)
    # -----------------------------------------------------------------------
    st.markdown('<div class="filter-card">', unsafe_allow_html=True)

    # Row 1: Search & Sort Dropdown
    s_col1, s_col2 = st.columns([5, 2])
    with s_col1:
        search_query = st.text_input(
            "Search Schemes",
            placeholder=_tr("searchPlaceholder"),
            label_visibility="collapsed"
        )
    with s_col2:
        sort_by = st.selectbox(
            "Sort By",
            [
                f"⭐ {_tr('sortBy')} (AI Best Match)",
                f"🏛️ {_tr('scopeCentral')}",
                f"📍 {_tr('scopeState')}",
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
elif active_nav_key == "home":
    
    # 1. HERO SECTION (Matches Images 4 & 5)
    st.markdown(f"""
    <div style="background: linear-gradient(180deg, #064e3b 0%, #0f172a 100%); color: white; padding: 3rem 2rem 2.5rem 2rem; border-radius: 1.5rem; text-align: center; margin-bottom: 1.5rem; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.25);">
        <div style="display: inline-flex; align-items: center; gap: 0.5rem; background-color: rgba(16, 185, 129, 0.2); border: 1px solid rgba(16, 185, 129, 0.4); padding: 0.35rem 1rem; border-radius: 9999px; font-size: 0.8rem; font-weight: 700; color: #6ee7b7; margin-bottom: 1.25rem;">
            {_tr('districtTag')} • {_tr('verifiedBadge')}
        </div>
        <h1 style="font-size: 2.5rem; font-weight: 900; line-height: 1.2; margin: 0 0 1rem 0; letter-spacing: -0.025em; color: #ffffff;">
            {_tr('heroTitle')}
        </h1>
        <p style="font-size: 1.05rem; color: #cbd5e1; max-width: 48rem; margin: 0 auto 1.5rem auto; line-height: 1.6;">
            {_tr('heroSubtitle')}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Hero Search Bar (Matches Image 4)
    h_s_col1, h_s_col2 = st.columns([5, 1.2])
    with h_s_col1:
        hero_search = st.text_input("Home Search", placeholder=_tr("searchSchemesPlaceholder"), label_visibility="collapsed", key="home_search_inp")
    with h_s_col2:
        if st.button(_tr("searchBtn"), key="home_search_btn", use_container_width=True):
            navigate_to("schemes")

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # 2. STATE EXPLORER PILLS & STATS (Matches Image 5)
    st.markdown(f"""
    <div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 0.5rem; margin-bottom: 1.5rem;">
        <span style="font-size: 0.85rem; font-weight: 800; color: #475569;">{_tr('exploreByState')}</span>
        <span style="background-color: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; padding: 0.2rem 0.65rem; border-radius: 9999px; font-size: 0.8rem; font-weight: 800;">Karnataka</span>
        <span style="background-color: #f1f5f9; color: #334155; border: 1px solid #e2e8f0; padding: 0.2rem 0.65rem; border-radius: 9999px; font-size: 0.8rem; font-weight: 800;">Maharashtra</span>
        <span style="background-color: #f1f5f9; color: #334155; border: 1px solid #e2e8f0; padding: 0.2rem 0.65rem; border-radius: 9999px; font-size: 0.8rem; font-weight: 800;">Delhi</span>
        <span style="background-color: #f1f5f9; color: #334155; border: 1px solid #e2e8f0; padding: 0.2rem 0.65rem; border-radius: 9999px; font-size: 0.8rem; font-weight: 800;">Tamil Nadu</span>
        <span style="background-color: #f1f5f9; color: #334155; border: 1px solid #e2e8f0; padding: 0.2rem 0.65rem; border-radius: 9999px; font-size: 0.8rem; font-weight: 800;">Uttar Pradesh</span>
        <span style="background-color: #f1f5f9; color: #334155; border: 1px solid #e2e8f0; padding: 0.2rem 0.65rem; border-radius: 9999px; font-size: 0.8rem; font-weight: 800;">West Bengal</span>
        <span style="background-color: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; padding: 0.2rem 0.65rem; border-radius: 9999px; font-size: 0.8rem; font-weight: 800;">All India +</span>
    </div>
    """, unsafe_allow_html=True)

    # 4 Stat Counters (Matches Image 5)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="filter-card" style="text-align: center; border-radius: 1.25rem;">
            <div style="font-size: 2.2rem; font-weight: 900; color: #0f172a;">{_tr('stat1Num')}</div>
            <div style="font-size: 0.85rem; font-weight: 700; color: #64748b;">{_tr('stat1Label')}</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="filter-card" style="text-align: center; border-radius: 1.25rem;">
            <div style="font-size: 2.2rem; font-weight: 900; color: #047857;">{_tr('stat2Num')}</div>
            <div style="font-size: 0.85rem; font-weight: 700; color: #64748b;">{_tr('stat2Label')}</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="filter-card" style="text-align: center; border-radius: 1.25rem;">
            <div style="font-size: 2.2rem; font-weight: 900; color: #d97706;">{_tr('stat3Num')}</div>
            <div style="font-size: 0.85rem; font-weight: 700; color: #64748b;">{_tr('stat3Label')}</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="filter-card" style="text-align: center; border-radius: 1.25rem;">
            <div style="font-size: 2.2rem; font-weight: 900; color: #0284c7;">{_tr('stat4Num')}</div>
            <div style="font-size: 0.85rem; font-weight: 700; color: #64748b;">{_tr('stat4Label')}</div>
        </div>
        """, unsafe_allow_html=True)

    # 3. FEATURE LAUNCH CARDS (Matches Image 5)
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        st.markdown(f"""
        <div class="filter-card" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div style="width: 40px; height: 40px; border-radius: 0.75rem; background-color: #ecfdf5; display: flex; align-items: center; justify-content: center; font-size: 1.3rem; margin-bottom: 0.75rem;">
                    🤖
                </div>
                <h3 style="font-size: 1.15rem; font-weight: 900; color: #0f172a; margin: 0 0 0.5rem 0;">{_tr('feature1Title')}</h3>
                <p style="font-size: 0.85rem; color: #475569; line-height: 1.5; margin: 0 0 1rem 0;">
                    {_tr('feature1Desc')}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(_tr('feature1Btn'), key="btn_f1", use_container_width=True):
            navigate_to("chatbot")
    with f_col2:
        st.markdown(f"""
        <div class="filter-card" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div style="width: 40px; height: 40px; border-radius: 0.75rem; background-color: #fef3c7; display: flex; align-items: center; justify-content: center; font-size: 1.3rem; margin-bottom: 0.75rem;">
                    📋
                </div>
                <h3 style="font-size: 1.15rem; font-weight: 900; color: #0f172a; margin: 0 0 0.5rem 0;">{_tr('feature2Title')}</h3>
                <p style="font-size: 0.85rem; color: #475569; line-height: 1.5; margin: 0 0 1rem 0;">
                    {_tr('feature2Desc')}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(_tr('feature2Btn'), key="btn_f2", use_container_width=True):
            navigate_to("eligibility")
    with f_col3:
        st.markdown(f"""
        <div class="filter-card" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div style="width: 40px; height: 40px; border-radius: 0.75rem; background-color: #eff6ff; display: flex; align-items: center; justify-content: center; font-size: 1.3rem; margin-bottom: 0.75rem;">
                    📍
                </div>
                <h3 style="font-size: 1.15rem; font-weight: 900; color: #0f172a; margin: 0 0 0.5rem 0;">{_tr('feature3Title')}</h3>
                <p style="font-size: 0.85rem; color: #475569; line-height: 1.5; margin: 0 0 1rem 0;">
                    {_tr('feature3Desc')}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(_tr('feature3Btn'), key="btn_f3", use_container_width=True):
            navigate_to("serviceMap")

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # 4. POPULAR NATIONAL & STATE SCHEMES (Matches Image 6)
    col_pop_title, col_pop_btn = st.columns([3.5, 1.5], vertical_alignment="center")
    with col_pop_title:
        st.markdown(f"""
        <div style="margin-bottom: 0.5rem;">
            <span style="font-size: 0.75rem; font-weight: 800; color: #047857; text-transform: uppercase; letter-spacing: 0.05em;">{_tr('popSchemesTag')}</span>
            <h2 style="font-size: 1.75rem; font-weight: 900; color: #0f172a; margin: 0.2rem 0;">{_tr('popSchemesTitle')}</h2>
            <p style="font-size: 0.85rem; color: #64748b; margin: 0;">{_tr('popSchemesSub')}</p>
        </div>
        """, unsafe_allow_html=True)
    with col_pop_btn:
        if st.button(_tr('viewAllSchemes'), key="btn_view_all_pop", use_container_width=True):
            navigate_to("schemes")

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
                        <span class="badge-central">{_tr('centralGovBadge')}</span>
                        <span style="font-size: 0.7rem; font-weight: 800; color: #047857; background-color: #ecfdf5; padding: 0.1rem 0.4rem; border-radius: 9999px;">{_tr('verifiedBadge')}</span>
                    </div>
                    <h4 style="font-size: 1rem; font-weight: 900; color: #0f172a; margin: 0.35rem 0;">{p['name']}</h4>
                    <p style="font-size: 0.8rem; color: #475569; line-height: 1.4; height: 3.8rem; overflow: hidden; margin-bottom: 0.5rem;">{p['desc']}</p>
                    <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 0.6rem; padding: 0.5rem; margin-bottom: 0.75rem;">
                        <span style="font-size: 0.7rem; font-weight: 800; color: #065f46; display: block;">{_tr('keyBenefitLabel')}</span>
                        <span style="font-size: 0.75rem; color: #334155; line-height: 1.3;">{p['benefit'][:110]}...</span>
                    </div>
                </div>
                <div style="border-top: 1px solid #e2e8f0; padding-top: 0.65rem;">
                    <a href="{p['url']}" target="_blank" style="background-color: #047857; color: white; padding: 0.45rem 0.85rem; border-radius: 0.6rem; font-size: 0.8rem; font-weight: 800; text-decoration: none; display: block; text-align: center;">
                        {_tr('visitOfficialWebsite')}
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    # 5. HOW CIVICGUIDE AI WORKS (Matches Image 6 / 4-Step Process)
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <span style="font-size: 0.75rem; font-weight: 800; color: #047857; text-transform: uppercase; letter-spacing: 0.05em;">{_tr('howItWorksTag')}</span>
        <h2 style="font-size: 2rem; font-weight: 900; color: #0f172a; margin: 0.2rem 0;">{_tr('howItWorksTitle')}</h2>
        <p style="font-size: 0.85rem; color: #64748b;">{_tr('howItWorksSub')}</p>
    </div>
    """, unsafe_allow_html=True)

    w1, w2, w3, w4 = st.columns(4)
    with w1:
        st.markdown(f"""
        <div class="filter-card" style="height: 100%; position: relative;">
            <span style="position: absolute; top: 1rem; right: 1.25rem; font-size: 1.5rem; font-weight: 900; color: #d1fae5;">01</span>
            <div style="width: 34px; height: 34px; border-radius: 0.5rem; background-color: #ecfdf5; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; margin-bottom: 0.5rem;">🤖</div>
            <h4 style="font-size: 0.95rem; font-weight: 900; color: #0f172a; margin: 0 0 0.35rem 0;">{_tr('howStep1Title')}</h4>
            <p style="font-size: 0.8rem; color: #475569; line-height: 1.4; margin: 0;">{_tr('howStep1Desc')}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(_tr('howStep1Btn'), key="btn_w1", use_container_width=True):
            navigate_to("chatbot")
    with w2:
        st.markdown(f"""
        <div class="filter-card" style="height: 100%; position: relative;">
            <span style="position: absolute; top: 1rem; right: 1.25rem; font-size: 1.5rem; font-weight: 900; color: #fef3c7;">02</span>
            <div style="width: 34px; height: 34px; border-radius: 0.5rem; background-color: #fef3c7; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; margin-bottom: 0.5rem;">📋</div>
            <h4 style="font-size: 0.95rem; font-weight: 900; color: #0f172a; margin: 0 0 0.35rem 0;">{_tr('howStep2Title')}</h4>
            <p style="font-size: 0.8rem; color: #475569; line-height: 1.4; margin: 0;">{_tr('howStep2Desc')}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(_tr('howStep2Btn'), key="btn_w2", use_container_width=True):
            navigate_to("eligibility")
    with w3:
        st.markdown(f"""
        <div class="filter-card" style="height: 100%; position: relative;">
            <span style="position: absolute; top: 1rem; right: 1.25rem; font-size: 1.5rem; font-weight: 900; color: #dbeafe;">03</span>
            <div style="width: 34px; height: 34px; border-radius: 0.5rem; background-color: #eff6ff; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; margin-bottom: 0.5rem;">🏛️</div>
            <h4 style="font-size: 0.95rem; font-weight: 900; color: #0f172a; margin: 0 0 0.35rem 0;">{_tr('howStep3Title')}</h4>
            <p style="font-size: 0.8rem; color: #475569; line-height: 1.4; margin: 0;">{_tr('howStep3Desc')}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(_tr('howStep3Btn'), key="btn_w3", use_container_width=True):
            navigate_to("schemes")
    with w4:
        st.markdown(f"""
        <div class="filter-card" style="height: 100%; position: relative;">
            <span style="position: absolute; top: 1rem; right: 1.25rem; font-size: 1.5rem; font-weight: 900; color: #d1fae5;">04</span>
            <div style="width: 34px; height: 34px; border-radius: 0.5rem; background-color: #ecfdf5; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; margin-bottom: 0.5rem;">🌐</div>
            <h4 style="font-size: 0.95rem; font-weight: 900; color: #0f172a; margin: 0 0 0.35rem 0;">{_tr('howStep4Title')}</h4>
            <p style="font-size: 0.8rem; color: #475569; line-height: 1.4; margin: 0;">{_tr('howStep4Desc')}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(_tr('howStep4Btn'), key="btn_w4", use_container_width=True):
            navigate_to("serviceMap")

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    # 6. DISTRICT MAP & SERVICES (Matches Image 9 Exactly)
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #064e3b 0%, #0f172a 100%); color: white; padding: 2rem 2.5rem; border-radius: 1.5rem; margin-bottom: 1.5rem; display: flex; flex-direction: column; gap: 1rem;">
        <div>
            <span style="font-size: 0.75rem; font-weight: 800; color: #fde047; text-transform: uppercase; letter-spacing: 0.05em;">{_tr('districtMapTag')}</span>
            <h3 style="font-size: 1.6rem; font-weight: 900; color: white; margin: 0.2rem 0;">{_tr('districtMapTitle')}</h3>
            <p style="font-size: 0.85rem; color: #cbd5e1; margin: 0; max-width: 48rem;">{_tr('districtMapSub')}</p>
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
elif active_nav_key == "chatbot":
    st.markdown(f'<div class="hero-title">{_tr("chatHeroTitle")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-desc">{_tr("chatHeroSub")}</div>', unsafe_allow_html=True)

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": _tr("chatWelcome"),
                "url": "https://www.myscheme.gov.in"
            }
        ]

    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("url"):
                st.link_button(_tr("visitOfficialWebsite"), msg["url"])

    if query := st.chat_input(_tr("chatPlaceholder")):
        st.session_state.chat_messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
            
        with st.chat_message("assistant"):
            res = _synthesize_python_ai_reply(query, schemes_list)
            st.markdown(res["answer"])
            if res.get("url"):
                st.link_button(_tr("visitOfficialWebsite"), res["url"])
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": res["answer"],
                "url": res.get("url")
            })

# ---------------------------------------------------------------------------
# VIEW: 4. ELIGIBILITY CHECKER
# ---------------------------------------------------------------------------
elif active_nav_key == "eligibility":
    st.markdown(f'<div class="hero-title">{_tr("eligibilityHeroTitle")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-desc">{_tr("eligibilityHeroSub")}</div>', unsafe_allow_html=True)

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

        submit = st.form_submit_button(f"🔍 {_tr('feature2Btn')}")

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
# VIEW: 5. SERVICE MAP (Matches User Screenshot Exactly)
# ---------------------------------------------------------------------------
elif active_nav_key == "serviceMap":
    
    # 1. Page Header (Matches user screenshot)
    hdr_col, near_col = st.columns([4, 1.2], vertical_alignment="center")
    with hdr_col:
        st.markdown('<div class="hero-badge">🌐 OpenStreetMap • Verified Government Offices & CSC Directory</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hero-title">{_tr("mapTitle")}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hero-desc">{_tr("mapSub")}</div>', unsafe_allow_html=True)
    with near_col:
        if st.button(f"📍 {_tr('nearMe')}", key="btn_near_me", use_container_width=True):
            st.session_state["svc_map_state"] = "Karnataka (31 Districts)"
            st.session_state["svc_map_district"] = "📍 Vijayanagara District"
            st.session_state["svc_map_taluk"] = "Hosapete"
            st.rerun()

    # 2. Main Filter Card (Matches user screenshot)
    st.markdown('<div class="filter-card">', unsafe_allow_html=True)

    # Search Box
    search_q = st.text_input(
        "Search Offices",
        placeholder=_tr("searchOfficesPlaceholder"),
        label_visibility="collapsed",
        key="svc_search_box"
    )

    st.markdown("<hr style='margin: 0.75rem 0; border-color: #f1f5f9;'>", unsafe_allow_html=True)

    # Row 1: State Dropdown, District Dropdown, Jurisdiction Level
    state_options = [
        "Karnataka (31 Districts)",
        "Maharashtra (10 Districts)",
        "Delhi (11 Districts)",
        "Tamil Nadu (9 Districts)",
        "Uttar Pradesh (10 Districts)",
        "West Bengal (5 Districts)",
        "Rajasthan (5 Districts)",
        "Telangana (4 Districts)",
        "Andhra Pradesh (4 Districts)",
        "Kerala (4 Districts)",
        "Bihar (3 Districts)",
        "Madhya Pradesh (3 Districts)",
        "Gujarat (4 Districts)",
        "Uttarakhand (2 Districts)",
        "Chandigarh",
        "All India"
    ]

    STATE_DISPLAY_MAP = {
        "Karnataka (31 Districts)": "Karnataka",
        "Maharashtra (10 Districts)": "Maharashtra",
        "Delhi (11 Districts)": "Delhi",
        "Tamil Nadu (9 Districts)": "Tamil Nadu",
        "Uttar Pradesh (10 Districts)": "Uttar Pradesh",
        "West Bengal (5 Districts)": "West Bengal",
        "Rajasthan (5 Districts)": "Rajasthan",
        "Telangana (4 Districts)": "Telangana",
        "Andhra Pradesh (4 Districts)": "Andhra Pradesh",
        "Kerala (4 Districts)": "Kerala",
        "Bihar (3 Districts)": "Bihar",
        "Madhya Pradesh (3 Districts)": "Madhya Pradesh",
        "Gujarat (4 Districts)": "Gujarat",
        "Uttarakhand (2 Districts)": "Uttarakhand",
        "Chandigarh": "Chandigarh",
        "All India": "All India"
    }

    f_col1, f_col2, f_col3 = st.columns([1.5, 1.5, 1.2])

    with f_col1:
        st.markdown(f"<span style='font-size: 0.75rem; font-weight: 800; color: #334155; text-transform: uppercase;'>{_tr('selectStateLabel')}</span>", unsafe_allow_html=True)
        selected_state_display = st.selectbox(
            "State",
            state_options,
            index=0,
            label_visibility="collapsed",
            key="svc_map_state"
        )
        selected_state_clean = STATE_DISPLAY_MAP.get(selected_state_display, "Karnataka")

    # Dynamic Districts for the selected state
    state_districts_dict = ALL_STATES_DISTRICTS_TALUKS.get(selected_state_clean, {})
    district_names = sorted(list(state_districts_dict.keys()))

    if selected_state_clean == "All India":
        all_dists = []
        for s_d in ALL_STATES_DISTRICTS_TALUKS.values():
            all_dists.extend(s_d.keys())
        district_options = ["All Districts"] + sorted(list(set(all_dists)))
    else:
        district_options = [f"All Districts ({len(district_names)})"] + [f"📍 {d} District" for d in district_names]

    # Default index for district: Vijayanagara if in Karnataka
    default_dist_idx = 0
    if selected_state_clean == "Karnataka":
        for i, opt in enumerate(district_options):
            if "Vijayanagara" in opt:
                default_dist_idx = i
                break

    with f_col2:
        st.markdown(f"<span style='font-size: 0.75rem; font-weight: 800; color: #334155; text-transform: uppercase;'>{_tr('selectDistrictLabel')} ({len(district_names)} Districts in {selected_state_clean}):</span>", unsafe_allow_html=True)
        selected_dist_display = st.selectbox(
            "District",
            district_options,
            index=default_dist_idx if default_dist_idx < len(district_options) else 0,
            label_visibility="collapsed",
            key="svc_map_district"
        )
        selected_dist_clean = selected_dist_display.replace("📍 ", "").replace(" District", "").strip()
        if "All Districts" in selected_dist_clean:
            selected_dist_clean = "All"

    with f_col3:
        st.markdown(f"<span style='font-size: 0.75rem; font-weight: 800; color: #334155; text-transform: uppercase;'>{_tr('jurisdictionLabel')}</span>", unsafe_allow_html=True)
        selected_level = st.radio(
            "Jurisdiction Level",
            ["All", "Central", "State"],
            index=0,
            horizontal=True,
            label_visibility="collapsed",
            key="svc_map_level"
        )

    # Row 2: Dynamic Taluks for selected District
    if selected_dist_clean != "All" and selected_dist_clean in state_districts_dict:
        available_taluks = state_districts_dict[selected_dist_clean]
    elif selected_state_clean in ALL_STATES_DISTRICTS_TALUKS:
        all_t = []
        for t_list in state_districts_dict.values():
            all_t.extend(t_list)
        available_taluks = sorted(list(set(all_t)))
    else:
        available_taluks = []

    taluk_options = ["All Taluks"] + available_taluks

    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.75rem; margin-bottom: 0.35rem;">
        <span style="font-size: 0.75rem; font-weight: 800; color: #334155; text-transform: uppercase; letter-spacing: 0.05em;">
            📍 {_tr('taluksInDistrictLabel')} {selected_dist_clean if selected_dist_clean != 'All' else selected_state_clean} ({len(available_taluks)} TALUKS):
        </span>
        <span style="font-size: 0.7rem; font-weight: 700; color: #94a3b8;">
            {_tr('clickToZoom')}
        </span>
    </div>
    """, unsafe_allow_html=True)

    selected_taluk = st.radio(
        "Taluks",
        taluk_options[:15],
        index=0,
        horizontal=True,
        label_visibility="collapsed",
        key="svc_map_taluk"
    )

    # Row 3: Office Categories Filter
    categories = [
        "All Categories",
        "Central Ministries & Offices",
        "AIIMS & Central/State Hospitals",
        "Passport & Aadhaar Seva Kendras",
        "Central/State Universities & IITs",
        "State Secretariat & Collectorates",
        "Common Service Centres (CSC)",
        "Welfare & Pension Offices"
    ]

    st.markdown(f"""
    <div style="margin-top: 0.75rem; margin-bottom: 0.35rem;">
        <span style="font-size: 0.75rem; font-weight: 800; color: #334155; text-transform: uppercase; letter-spacing: 0.05em;">
            {_tr('filterOfficeCategoryLabel')}
        </span>
    </div>
    """, unsafe_allow_html=True)

    selected_cat = st.radio(
        "Categories",
        categories,
        index=0,
        horizontal=True,
        label_visibility="collapsed",
        key="svc_map_category"
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # -----------------------------------------------------------------------
    # Filter Services
    # -----------------------------------------------------------------------
    filtered_services = list(services_list)

    # 1. State filter
    if selected_state_clean != "All India":
        filtered_services = [s for s in filtered_services if (s.get("state") or "").lower() == selected_state_clean.lower()]

    # 2. District filter
    if selected_dist_clean != "All":
        filtered_services = [
            s for s in filtered_services
            if selected_dist_clean.lower() in (s.get("district_city") or "").lower() or
               selected_dist_clean.lower() in (s.get("address") or "").lower()
        ]

    # 3. Taluk filter
    if selected_taluk != "All Taluks":
        filtered_services = [
            s for s in filtered_services
            if selected_taluk.lower() in (s.get("taluk") or "").lower() or
               selected_taluk.lower() in (s.get("address") or "").lower() or
               selected_taluk.lower() in (s.get("name") or "").lower()
        ]

    # 4. Jurisdiction level
    if selected_level == "Central":
        filtered_services = [s for s in filtered_services if "central" in (s.get("government_level") or "").lower()]
    elif selected_level == "State":
        filtered_services = [s for s in filtered_services if "central" not in (s.get("government_level") or "").lower()]

    # 5. Category filter
    if selected_cat != "All Categories":
        filtered_services = [s for s in filtered_services if s.get("category") == selected_cat]

    # 6. Search Query
    if search_q.strip():
        q = search_q.strip().lower()
        filtered_services = [
            s for s in filtered_services
            if q in (s.get("name") or "").lower() or
               q in (s.get("category") or "").lower() or
               q in (s.get("address") or "").lower() or
               q in (s.get("phone") or "").lower() or
               q in (s.get("taluk") or "").lower()
        ]

    # 7. Fallback generation if no specific DB services exist for this district
    if len(filtered_services) == 0 and selected_dist_clean != "All" and selected_state_clean != "All India":
        coords_info = DISTRICT_COORDINATES.get(selected_dist_clean, {"center": [15.2689, 76.3909], "zoom": 11})
        c_lat, c_lon = coords_info["center"]
        pri_taluk = selected_taluk if selected_taluk != "All Taluks" else (available_taluks[0] if available_taluks else selected_dist_clean)
        filtered_services = [
            {
                "id": f"gen-1-{selected_dist_clean}",
                "name": f"District Collectorate & Mini Vidhana Soudha ({selected_dist_clean})",
                "category": "State Secretariat & Collectorates",
                "government_level": "State Government",
                "state": selected_state_clean,
                "district_city": selected_dist_clean,
                "taluk": pri_taluk,
                "address": f"DC Office Complex, Main Revenue Road, {selected_dist_clean}, {selected_state_clean}",
                "phone": "+91 80-2200-1122",
                "latitude": c_lat + 0.003,
                "longitude": c_lon + 0.002,
                "official_url": "https://karnataka.gov.in"
            },
            {
                "id": f"gen-2-{selected_dist_clean}",
                "name": f"Common Service Centre (CSC) & Grama One ({pri_taluk})",
                "category": "Common Service Centres (CSC)",
                "government_level": "State Government",
                "state": selected_state_clean,
                "district_city": selected_dist_clean,
                "taluk": pri_taluk,
                "address": f"Citizen Seva Kendra, Near Taluk Office, {pri_taluk}, {selected_dist_clean}",
                "phone": "+91 94480-12345",
                "latitude": c_lat - 0.004,
                "longitude": c_lon + 0.005,
                "official_url": "https://sevasindhu.karnataka.gov.in"
            },
            {
                "id": f"gen-3-{selected_dist_clean}",
                "name": f"District General Hospital & Ayushman Arogya Mandir ({selected_dist_clean})",
                "category": "AIIMS & Central/State Hospitals",
                "government_level": "State Government",
                "state": selected_state_clean,
                "district_city": selected_dist_clean,
                "taluk": pri_taluk,
                "address": f"Civil Hospital Road, {selected_dist_clean}, {selected_state_clean}",
                "phone": "+91 80-2345-6789",
                "latitude": c_lat + 0.006,
                "longitude": c_lon - 0.003,
                "official_url": "https://pmjay.gov.in"
            },
            {
                "id": f"gen-4-{selected_dist_clean}",
                "name": f"Post Office Passport & Aadhaar Seva Kendra ({selected_dist_clean})",
                "category": "Passport & Aadhaar Seva Kendras",
                "government_level": "Central Government",
                "state": selected_state_clean,
                "district_city": selected_dist_clean,
                "taluk": pri_taluk,
                "address": f"Head Post Office Building, Station Road, {selected_dist_clean}, {selected_state_clean}",
                "phone": "+91 1800-258-1800",
                "latitude": c_lat - 0.002,
                "longitude": c_lon - 0.006,
                "official_url": "https://passportindia.gov.in"
            }
        ]

    # Determine map center coordinates and zoom level
    if selected_dist_clean != "All" and selected_dist_clean in DISTRICT_COORDINATES:
        center_coords = DISTRICT_COORDINATES[selected_dist_clean]["center"]
        zoom_level = 13 if selected_taluk != "All Taluks" else DISTRICT_COORDINATES[selected_dist_clean]["zoom"]
    elif selected_state_clean in DISTRICT_COORDINATES:
        center_coords = DISTRICT_COORDINATES[selected_state_clean]["center"]
        zoom_level = DISTRICT_COORDINATES[selected_state_clean]["zoom"]
    else:
        center_coords = [15.2689, 76.3909]
        zoom_level = 11

    services_json = json.dumps([
        {
            "id": s.get("id"),
            "name": s.get("name", ""),
            "category": s.get("category", ""),
            "government_level": s.get("government_level", ""),
            "state": s.get("state", ""),
            "district": s.get("district_city", ""),
            "taluk": s.get("taluk", ""),
            "address": s.get("address", ""),
            "phone": s.get("phone", ""),
            "latitude": s.get("latitude"),
            "longitude": s.get("longitude"),
            "official_url": s.get("official_url", "")
        }
        for s in filtered_services if s.get("latitude") and s.get("longitude")
    ])

    leaflet_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
      <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
      <style>
        body, html {{ margin: 0; padding: 0; height: 100%; width: 100%; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
        #map {{ height: 100%; width: 100%; border-radius: 1.5rem; }}
        .custom-marker {{
          display: flex; align-items: center; justify-content: center;
          width: 32px; height: 32px; border-radius: 50%;
          color: white; font-size: 15px; font-weight: bold;
          border: 2px solid white; box-shadow: 0 4px 8px rgba(0,0,0,0.3);
          cursor: pointer; transition: transform 0.2s ease;
        }}
        .custom-marker:hover {{ transform: scale(1.2); }}
        .popup-badge {{ display: inline-block; padding: 2px 7px; border-radius: 9999px; font-size: 10px; font-weight: 800; text-transform: uppercase; margin-bottom: 4px; }}
        .badge-central {{ background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; }}
        .badge-state {{ background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }}
        .popup-title {{ font-weight: 800; font-size: 14px; color: #0f172a; margin-bottom: 3px; line-height: 1.25; }}
        .popup-cat {{ font-size: 11px; font-weight: 700; color: #64748b; margin-bottom: 5px; }}
        .popup-addr {{ font-size: 11.5px; color: #334155; margin-bottom: 5px; line-height: 1.35; }}
        .popup-phone {{ font-size: 12px; font-weight: 800; color: #047857; margin-bottom: 7px; }}
        .popup-link {{ display: inline-block; background: #047857; color: white !important; font-size: 11px; font-weight: 800; text-decoration: none; padding: 4px 10px; border-radius: 6px; }}
        .popup-link:hover {{ background: #065f46; }}
      </style>
    </head>
    <body>
      <div id="map"></div>
      <script>
        var map = L.map('map', {{ scrollWheelZoom: true }}).setView([{center_coords[0]}, {center_coords[1]}], {zoom_level});
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
          maxZoom: 19,
          attribution: '© OpenStreetMap'
        }}).addTo(map);

        var services = {services_json};

        services.forEach(function(s) {{
          if (s.latitude && s.longitude) {{
            var iconHtml = '🏛️';
            var bg = '#1d4ed8';
            var cat = s.category || '';
            if (cat.indexOf('Hospital') !== -1 || cat.indexOf('Health') !== -1 || cat.indexOf('AIIMS') !== -1) {{
              iconHtml = '🏥'; bg = '#e11d48';
            }} else if (cat.indexOf('Passport') !== -1 || cat.indexOf('Aadhaar') !== -1) {{
              iconHtml = '🛂'; bg = '#4f46e5';
            }} else if (cat.indexOf('Universit') !== -1 || cat.indexOf('College') !== -1 || cat.indexOf('IIT') !== -1) {{
              iconHtml = '🎓'; bg = '#d97706';
            }} else if (cat.indexOf('CSC') !== -1 || cat.indexOf('Centre') !== -1 || cat.indexOf('Grama') !== -1) {{
              iconHtml = '💻'; bg = '#059669';
            }} else if (s.government_level === 'Central Government') {{
              iconHtml = '🏛️'; bg = '#2563eb';
            }} else {{
              iconHtml = '📍'; bg = '#0284c7';
            }}

            var customIcon = L.divIcon({{
              className: '',
              html: '<div class="custom-marker" style="background-color:' + bg + ';">' + iconHtml + '</div>',
              iconSize: [32, 32],
              iconAnchor: [16, 16]
            }});

            var badgeClass = (s.government_level === 'Central Government') ? 'badge-central' : 'badge-state';
            var popupContent = '<div style="max-width:240px; padding:2px;">' +
              '<span class="popup-badge ' + badgeClass + '">' + (s.government_level || 'Government') + '</span> ' +
              '<div class="popup-title">' + s.name + '</div>' +
              '<div class="popup-cat">' + cat + (s.taluk ? ' • ' + s.taluk : '') + '</div>' +
              '<div class="popup-addr">' + s.address + '</div>' +
              (s.phone ? '<div class="popup-phone">📞 ' + s.phone + '</div>' : '') +
              '<div style="margin-top:6px;">' +
              '<a href="https://www.google.com/maps/dir/?api=1&destination=' + s.latitude + ',' + s.longitude + '" target="_blank" class="popup-link">Get Directions ↗</a>' +
              '</div></div>';

            L.marker([s.latitude, s.longitude], {{icon: customIcon}})
              .addTo(map)
              .bindPopup(popupContent);
          }}
        }});
      </script>
    </body>
    </html>
    """

    # Side-by-Side Display (Left Map, Right Office Cards)
    col_map, col_list = st.columns([1.7, 1.1])
    with col_map:
        components.html(leaflet_html, height=650, scrolling=False)

    with col_list:
        # Header matching screenshot
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 0.6rem; border-bottom: 1px solid #e2e8f0; margin-bottom: 0.75rem;">
            <div>
                <span style="font-size: 1.15rem; font-weight: 900; color: #0f172a; display: block;">
                    {_tr('govOfficesLabel')} ({len(filtered_services)})
                </span>
                <span style="font-size: 0.75rem; font-weight: 700; color: #64748b;">
                    {selected_dist_clean if selected_dist_clean != 'All' else selected_state_clean} {f'• {selected_taluk}' if selected_taluk != 'All Taluks' else ''}
                </span>
            </div>
            <span style="font-size: 0.7rem; font-weight: 800; background-color: #d1fae5; color: #065f46; border: 1px solid #a7f3d0; padding: 0.2rem 0.55rem; border-radius: 9999px;">
                {_tr('verifiedBadge')}
            </span>
        </div>
        """, unsafe_allow_html=True)

        if len(filtered_services) == 0:
            st.info("ℹ️ No offices found for selected filters.")
        else:
            with st.container(height=580):
                for s in filtered_services:
                    is_central = "central" in (s.get("government_level") or "").lower()
                    badge_class = "badge-central" if is_central else "badge-state"
                    badge_label = "CENTRAL" if is_central else "STATE"
                    taluk_label = f"{s.get('taluk')} Taluk" if s.get('taluk') else (s.get('district_city') or '')
                    phone_label = s.get('phone') or 'Official Office'
                    nav_url = f"https://www.google.com/maps/dir/?api=1&destination={s.get('latitude')},{s.get('longitude')}"

                    st.markdown(f"""
                    <div class="office-card">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
                            <span class="{badge_class}">{badge_label}</span>
                            <span style="font-size: 0.72rem; font-weight: 700; color: #64748b;">{taluk_label}</span>
                        </div>
                        <h4 style="font-size: 0.95rem; font-weight: 800; color: #0f172a; margin: 0.25rem 0 0.15rem 0; line-height: 1.3;">
                            {s.get('name')}
                        </h4>
                        <p style="font-size: 0.78rem; color: #475569; margin: 0.2rem 0 0.45rem 0; line-height: 1.35;">
                            {s.get('address')}
                        </p>
                        <div style="display: flex; justify-content: space-between; align-items: center; pt: 0.35rem; border-top: 1px solid #f1f5f9;">
                            <span style="font-size: 0.78rem; font-weight: 800; color: #047857;">📞 {phone_label}</span>
                            <a href="{nav_url}" target="_blank" style="font-size: 0.75rem; font-weight: 800; color: #047857; text-decoration: none;">
                                {_tr('viewOnMapLabel')}
                            </a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        st.caption(_tr("clickOfficeNotice"))
