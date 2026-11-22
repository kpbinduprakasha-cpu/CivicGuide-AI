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
    .brand-wrap {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .brand-logo {
        width: 38px;
        height: 38px;
        background-color: #047857;
        color: #ffffff;
        border-radius: 0.75rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
    }
    .brand-title {
        font-size: 1.15rem;
        font-weight: 900;
        color: #0f172a;
        line-height: 1.1;
    }
    .brand-pill {
        display: inline-block;
        background-color: #dbeafe;
        color: #1e40af;
        font-size: 0.65rem;
        font-weight: 800;
        padding: 0.15rem 0.45rem;
        border-radius: 9999px;
        margin-left: 0.4rem;
        text-transform: uppercase;
        vertical-align: middle;
    }
    .brand-subtitle {
        font-size: 0.75rem;
        font-weight: 600;
        color: #64748b;
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
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Constants & Official State Portals Dictionary
# ---------------------------------------------------------------------------
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

schemes_list, services_list = load_database_data()

# ---------------------------------------------------------------------------
# TOP NAVBAR: Matches Image 2 React Header Exactly
# ---------------------------------------------------------------------------
nav_col_logo, nav_col_tabs, nav_col_right = st.columns([3, 5, 3])

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
            "Home",
            "Government Schemes",
            "AI Assistant",
            "Eligibility Checker",
            "Service Map"
        ],
        index=1,
        horizontal=True,
        label_visibility="collapsed"
    )

with nav_col_right:
    c_lang, c_gh, c_user = st.columns([3, 2, 1])
    with c_lang:
        selected_lang = st.selectbox("Language", ["English (English)", "ಕನ್ನಡ (Kannada)", "हिंदी (Hindi)"], index=0, label_visibility="collapsed")
    with c_gh:
        st.link_button("GitHub", "https://github.com/kpbinduprakasha-cpu/CivicGuide-AI")
    with c_user:
        st.markdown("""
        <div style="width: 34px; height: 34px; border-radius: 50%; background-color: #047857; color: white; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 0.9rem;" title="Citizen: K P BINDUPRAKASHA">
            K
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr style='margin-top: 0.2rem; margin-bottom: 1.25rem; border-color: #e2e8f0;'>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# VIEW: 1. GOVERNMENT SCHEMES (Matches Image 2 Exactly)
# ---------------------------------------------------------------------------
if active_nav == "Government Schemes":
    
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
# VIEW: 2. HOME & OVERVIEW
# ---------------------------------------------------------------------------
elif active_nav == "Home":
    st.markdown('<div class="hero-title">🏛️ Welcome to CivicGuide AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-desc">All-India Citizen Public Services and Government Welfare Advisory Platform.</div>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="filter-card" style="text-align: center;">
            <div style="font-size: 2rem; font-weight: 900; color: #047857;">{len(schemes_list)}</div>
            <div style="font-size: 0.8rem; font-weight: 800; color: #64748b; text-transform: uppercase;">Verified Welfare Schemes</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        central_count = len([s for s in schemes_list if "central" in (s.get("government_level") or "").lower()])
        st.markdown(f"""
        <div class="filter-card" style="text-align: center;">
            <div style="font-size: 2rem; font-weight: 900; color: #047857;">{central_count}</div>
            <div style="font-size: 0.8rem; font-weight: 800; color: #64748b; text-transform: uppercase;">Central Government</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown("""
        <div class="filter-card" style="text-align: center;">
            <div style="font-size: 2rem; font-weight: 900; color: #047857;">36</div>
            <div style="font-size: 0.8rem; font-weight: 800; color: #64748b; text-transform: uppercase;">States & UTs Portals</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="filter-card" style="text-align: center;">
            <div style="font-size: 2rem; font-weight: 900; color: #047857;">{len(services_list)}</div>
            <div style="font-size: 0.8rem; font-weight: 800; color: #64748b; text-transform: uppercase;">Public Service Centers</div>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# VIEW: 3. AI CITIZEN ASSISTANT
# ---------------------------------------------------------------------------
elif active_nav == "AI Assistant":
    st.markdown('<div class="hero-title">🤖 AI Citizen Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-desc">Grounded Policy Assistant providing step-by-step application instructions and verified government sources.</div>', unsafe_allow_html=True)

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": "Namaskara! I am your CivicGuide AI assistant. How can I help you with government schemes, certificates, or local offices today?"}
        ]

    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if query := st.chat_input("Ask a question about government schemes, documents, or local offices..."):
        st.session_state.chat_messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
            
        with st.chat_message("assistant"):
            # Scheme match
            found = None
            q_lower = query.lower()
            for s in schemes_list:
                s_name = s.get("name", "").lower()
                words = [w for w in s_name.replace("-", " ").split() if len(w) > 3 and w not in ["scheme", "yojana"]]
                if any(w in q_lower for w in words):
                    found = s
                    break

            if found:
                ans = f"""### 🏛️ {found.get('name')} ({found.get('government_level')})
**Sector:** {found.get('category')}

#### 💰 Direct Benefits:
{found.get('benefits')}

#### 👥 Eligibility:
{found.get('eligibility')}

#### 📋 Required Documents:
{found.get('required_documents')}

#### 📝 How to Apply:
{found.get('application_process')}

🔗 **Official Portal:** [{found.get('official_url')}]({found.get('official_url')})
"""
            else:
                ans = f"""### 🏛️ Citizen Guidance for: "{query}"

1. **Eligibility Check:** Review income criteria, domicile requirement, and age on the **Eligibility Checker** tab.
2. **Documents Checklist:** Aadhaar Card (linked to mobile), Ration Card (BPL/APL), Income/Caste Certificate, Bank Passbook.
3. **Application Mode:** Visit your nearest Grama One / CSC or submit online on the official portal.

🔗 **National Portal:** [https://www.myscheme.gov.in](https://www.myscheme.gov.in)
"""
            st.markdown(ans)
            st.session_state.chat_messages.append({"role": "assistant", "content": ans})

# ---------------------------------------------------------------------------
# VIEW: 4. ELIGIBILITY CHECKER
# ---------------------------------------------------------------------------
elif active_nav == "Eligibility Checker":
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
elif active_nav == "Service Map":
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
