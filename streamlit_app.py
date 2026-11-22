import os
import sqlite3
import importlib.util
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Page Configuration & Styling
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="CivicGuide AI • Central & State Public Services Platform",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Contrast, Accessible Theme Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.3rem !important;
        font-weight: 900 !important;
        color: #064e3b !important;
        margin-bottom: 0.2rem !important;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .sub-title {
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        color: #475569 !important;
        margin-bottom: 1rem !important;
    }
    .scope-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 800;
        text-transform: uppercase;
        margin-right: 0.5rem;
    }
    .badge-central {
        background-color: #eff6ff;
        color: #1e3a8a;
        border: 1px solid #bfdbfe;
    }
    .badge-state {
        background-color: #fef3c7;
        color: #78350f;
        border: 1px solid #fde68a;
    }
    .portal-banner {
        background: linear-gradient(135deg, #ecfdf5 0%, #f0fdfa 50%, #f0f9ff 100%);
        border: 2px solid #6ee7b7;
        border-radius: 1.25rem;
        padding: 1.25rem;
        margin-bottom: 1.5rem;
    }
    .scheme-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 1.25rem;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    }
    .scheme-card:hover {
        border-color: #10b981;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    .benefit-box {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 0.75rem;
        padding: 0.75rem;
        margin: 0.5rem 0;
        font-weight: 600;
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
        "description": "Official National Platform for All-India Central & State Government Welfare Schemes across all 36 States and Union Territories."
    },
    "Karnataka": {
        "name": "Karnataka Seva Sindhu & Nadakacheri Portal",
        "url": "https://sevasindhu.karnataka.gov.in",
        "description": "Official Government of Karnataka portal for citizen services, guarantee schemes (Gruha Lakshmi, Yuva Nidhi, Gruha Jyothi, Shakti), and revenue certificates."
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
# Database Loader with Caching & Verified Git-Tracked Seed Fallbacks
# ---------------------------------------------------------------------------
def _ensure_sqlite_database_seeded(db_path, schemes, services):
    """Ensure SQLite database is created and seeded with all verified records."""
    try:
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS schemes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT, name_kn TEXT, name_hi TEXT,
                category TEXT, description TEXT, description_kn TEXT, description_hi TEXT,
                benefits TEXT, benefits_kn TEXT, benefits_hi TEXT,
                eligibility TEXT, eligibility_kn TEXT, eligibility_hi TEXT,
                required_documents TEXT, application_process TEXT, official_url TEXT,
                government_level TEXT, state TEXT, source_date TEXT, verified INTEGER
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS public_services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT, name_kn TEXT, name_hi TEXT,
                category TEXT, state TEXT, district_city TEXT, taluk TEXT,
                government_level TEXT, address TEXT, latitude REAL, longitude REAL,
                phone TEXT, official_url TEXT, verified INTEGER
            )
        ''')
        cur.execute('SELECT COUNT(*) FROM schemes')
        if cur.fetchone()[0] == 0 and schemes:
            for s in schemes:
                cur.execute('''
                    INSERT INTO schemes (name, name_kn, name_hi, category, description, description_kn, description_hi,
                                         benefits, benefits_kn, benefits_hi, eligibility, eligibility_kn, eligibility_hi,
                                         required_documents, application_process, official_url, government_level, state, source_date, verified)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    s.get('name'), s.get('name_kn'), s.get('name_hi'), s.get('category'),
                    s.get('description'), s.get('description_kn'), s.get('description_hi'),
                    s.get('benefits'), s.get('benefits_kn'), s.get('benefits_hi'),
                    s.get('eligibility'), s.get('eligibility_kn'), s.get('eligibility_hi'),
                    s.get('required_documents'), s.get('application_process'), s.get('official_url'),
                    s.get('government_level'), s.get('state'), s.get('source_date'), 1 if s.get('verified') else 0
                ))
        cur.execute('SELECT COUNT(*) FROM public_services')
        if cur.fetchone()[0] == 0 and services:
            for sv in services:
                cur.execute('''
                    INSERT INTO public_services (name, name_kn, name_hi, category, state, district_city, taluk,
                                                 government_level, address, latitude, longitude, phone, official_url, verified)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    sv.get('name'), sv.get('name_kn'), sv.get('name_hi'), sv.get('category'),
                    sv.get('state'), sv.get('district_city'), sv.get('taluk'),
                    sv.get('government_level'), sv.get('address'), sv.get('latitude'), sv.get('longitude'),
                    sv.get('phone'), sv.get('official_url'), 1 if sv.get('verified') else 0
                ))
        conn.commit()
        conn.close()
    except Exception:
        pass

def _load_data_from_python_modules():
    """Directly loads verified data from git-tracked Python modules without external dependencies."""
    schemes = []
    services = []
    curr_dir = os.path.dirname(os.path.abspath(__file__))

    # 1. Load All-India Schemes from git-tracked backend/app/utils/all_india_schemes_data.py
    schemes_candidates = [
        os.path.join(curr_dir, "backend", "app", "utils", "all_india_schemes_data.py"),
        os.path.join("backend", "app", "utils", "all_india_schemes_data.py"),
    ]
    for s_path in schemes_candidates:
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
                    break
            except Exception:
                pass

    # 2. Load Public Services from git-tracked backend/app/utils/all_india_services_data.py
    services_candidates = [
        os.path.join(curr_dir, "backend", "app", "utils", "all_india_services_data.py"),
        os.path.join("backend", "app", "utils", "all_india_services_data.py"),
    ]
    for sv_path in services_candidates:
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
                    break
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

    # If database file is missing or contains 0 records (e.g. deployed to Streamlit Community Cloud),
    # load directly from our git-tracked verified datasets:
    if not schemes or len(schemes) == 0:
        py_schemes, py_services = _load_data_from_python_modules()
        schemes = py_schemes
        if not services or len(services) == 0:
            services = py_services

        # Auto-seed SQLite database file in database/users.db for future queries
        target_db = os.path.join("database", "users.db")
        _ensure_sqlite_database_seeded(target_db, schemes, services)

    return schemes, services

schemes_list, services_list = load_database_data()

# ---------------------------------------------------------------------------
# Sidebar: Citizen Profile & App Navigation
# ---------------------------------------------------------------------------
with st.sidebar:
    st.image("https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/landmark.svg", width=48)
    st.markdown("### **CivicGuide AI**")
    st.caption("Citizen Public Services & Welfare Advisory Platform")
    
    st.markdown("---")
    st.markdown("#### **Active Citizen Profile**")
    st.markdown("""
    **Citizen:** K P BINDUPRAKASHA  
    **Age / Gender:** 24 Years • Male  
    **Location:** Vijayanagara, Karnataka  
    **Occupation:** Graduate / Job Aspirant  
    **Ration Card:** BPL Priority Card  
    """)
    
    st.markdown("---")
    nav_choice = st.radio(
        "Navigate Platform",
        [
            "🏛️ Schemes Directory",
            "🤖 AI Citizen Assistant",
            "📋 Eligibility Screening",
            "📍 Service Map & Taluks",
            "ℹ️ About & GitHub"
        ]
    )
    
    st.markdown("---")
    st.markdown("#### **Project Repository**")
    st.markdown("""
    [![GitHub](https://img.shields.io/badge/GitHub-CivicGuide--AI-047857?logo=github)](https://github.com/kpbinduprakasha-cpu/CivicGuide-AI)  
    **Author:** [@kpbinduprakasha-cpu](https://github.com/kpbinduprakasha-cpu)
    """)

# ---------------------------------------------------------------------------
# Main Page View: 1. Schemes Directory
# ---------------------------------------------------------------------------
if nav_choice == "🏛️ Schemes Directory":
    st.markdown('<div class="main-title">🏛️ Government Welfare Schemes Directory</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Verified Central & State Government Welfare Schemes across India with Document Checklists and Direct Official Links.</div>', unsafe_allow_html=True)
    
    # Row 1: Search & Controls
    c1, c2, c3 = st.columns([3, 2, 2])
    with c1:
        search_query = st.text_input("🔍 Search Schemes", placeholder="e.g., scholarship, solar, 2000, farmer, loan...")
    with c2:
        category_options = ["All", "Agriculture", "Education", "Healthcare", "Employment", "Housing", "Women and child welfare", "Social welfare", "Financial assistance"]
        selected_category = st.selectbox("📂 Welfare Sector", category_options)
    with c3:
        view_mode = st.radio("Display Mode", ["🎴 Cards View", "📋 Combined Table View"], horizontal=True)

    # Row 2: Three-Tier Scope Selector & State Selector
    col_scope, col_state = st.columns([3, 2])
    with col_scope:
        scope_choice = st.radio(
            "Schemes Scope",
            [
                "🏛️ Central Government",
                "📍 State Government",
                "🇮🇳 All Combined"
            ],
            horizontal=True
        )
    with col_state:
        selected_state = st.selectbox("🏛️ State Portal & Region Link", ALL_INDIAN_STATES, index=0)

    # Official State Government Portal Banner
    portal_info = STATE_OFFICIAL_PORTALS.get(selected_state, STATE_OFFICIAL_PORTALS["All India"])
    st.markdown(f"""
    <div class="portal-banner">
        <div style="font-weight: 800; font-size: 0.85rem; color: #047857; text-transform: uppercase;">
            Verified Official {selected_state if selected_state != 'All India' else 'National'} Government Portal
        </div>
        <div style="font-size: 1.25rem; font-weight: 800; color: #0f172a; margin: 0.25rem 0;">
            {portal_info['name']}
        </div>
        <p style="font-size: 0.95rem; color: #334155; margin-bottom: 0.75rem;">
            {portal_info['description']}
        </p>
        <a href="{portal_info['url']}" target="_blank" style="display: inline-block; background-color: #059669; color: white; padding: 0.5rem 1.25rem; border-radius: 0.75rem; font-weight: 800; text-decoration: none;">
            Visit Official {selected_state if selected_state != 'All India' else 'myScheme'} Website ↗
        </a>
    </div>
    """, unsafe_allow_html=True)

    # Filter Logic
    filtered = list(schemes_list)

    # Scope Filtering:
    # 1. Central: shows central schemes
    # 2. State: only shows when a state is selected; otherwise prompt user
    # 3. All: shows all combined
    if scope_choice == "🏛️ Central Government":
        filtered = [s for s in filtered if "central" in (s.get("government_level") or "").lower()]
    elif scope_choice == "📍 State Government":
        if selected_state and selected_state != "All India":
            filtered = [
                s for s in filtered 
                if ("central" not in (s.get("government_level") or "").lower()) and
                (selected_state.lower() in (s.get("state") or "").lower() or selected_state.lower() in (s.get("government_level") or "").lower())
            ]
        else:
            filtered = [] # Otherwise no show, prompt user
    else: # All Combined
        pass

    # Category Filtering
    if selected_category != "All":
        filtered = [s for s in filtered if selected_category.lower() in (s.get("category") or "").lower()]

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

    # Display Schemes
    if scope_choice == "📍 State Government" and (not selected_state or selected_state == "All India"):
        st.warning("📍 **Please select a State from the dropdown above to view its State Government schemes.**")
        st.info("State Government welfare programs are specific to individual states. Choose Karnataka, Maharashtra, Delhi, Tamil Nadu, Uttar Pradesh, Rajasthan, etc., to load official initiatives.")
    elif len(filtered) == 0:
        st.info(f"ℹ️ No schemes found matching Welfare Sector '**{selected_category}**' under '**{scope_choice}**' for '**{selected_state}**'.")
        if selected_category != "All":
            st.markdown(f"💡 **Tip:** Change **Welfare Sector** to **'All'** to view all verified initiatives for {selected_state}.")
        if search_query.strip():
            st.markdown(f"💡 **Tip:** Try clearing the search keyword: `{search_query}`.")
        st.markdown("💡 You can also switch Scope to **🏛️ Central Government** (10 schemes) or **🇮🇳 All Combined** (47 schemes) to view nationwide benefits.")
    else:
        st.markdown(f"**Showing {len(filtered)} verified schemes**")

        if view_mode == "📋 Combined Table View":
            table_data = []
            for idx, s in enumerate(filtered, 1):
                is_central = "central" in (s.get("government_level") or "").lower()
                table_data.append({
                    "#": idx,
                    "Scheme Name": s.get("name"),
                    "Sector": s.get("category"),
                    "Government Level": "🏛️ Central" if is_central else f"📍 State: {s.get('state', 'State')}",
                    "Direct Benefits": s.get("benefits"),
                    "Eligibility": s.get("eligibility"),
                    "Official Portal": s.get("official_url")
                })
            df = pd.DataFrame(table_data)
            
            # Action controls row: CSV download
            csv_data = df.to_csv(index=False).encode('utf-8')
            t_col1, t_col2 = st.columns([4, 1])
            with t_col2:
                st.download_button(
                    "📥 Export Small Table (CSV)",
                    data=csv_data,
                    file_name="civicguide_schemes_small_table.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            # Compact table rendering
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "#": st.column_config.NumberColumn("#", width="small"),
                    "Scheme Name": st.column_config.TextColumn("Scheme Name", width="medium"),
                    "Sector": st.column_config.TextColumn("Sector", width="small"),
                    "Government Level": st.column_config.TextColumn("Government Level", width="small"),
                    "Direct Benefits": st.column_config.TextColumn("Direct Benefits", width="large"),
                    "Eligibility": st.column_config.TextColumn("Eligibility", width="large"),
                    "Official Portal": st.column_config.LinkColumn("Official Portal", display_text="Visit ↗")
                }
            )
        else:
            # Cards View (Grid of 3 columns)
            cols = st.columns(3)
            for idx, scheme in enumerate(filtered):
                col = cols[idx % 3]
                with col:
                    is_central = "central" in (scheme.get("government_level") or "").lower()
                    badge_html = '<span class="scope-badge badge-central">🏛️ Central Government</span>' if is_central else f'<span class="scope-badge badge-state">📍 State Government • {scheme.get("state")}</span>'
                    
                    st.markdown(f"""
                    <div class="scheme-card">
                        <div>{badge_html}</div>
                        <h4 style="margin: 0.5rem 0; font-weight: 800; color: #0f172a;">{scheme.get('name')}</h4>
                        <span style="font-size: 0.8rem; font-weight: 700; color: #059669;">{scheme.get('category')}</span>
                        <p style="font-size: 0.85rem; color: #475569; margin: 0.5rem 0;">{scheme.get('description')[:140]}...</p>
                        <div class="benefit-box">
                            💰 <strong>Benefit:</strong> {scheme.get('benefits')}
                        </div>
                        <div style="font-size: 0.8rem; color: #334155; margin-top: 0.5rem;">
                            <strong>Eligibility:</strong> {scheme.get('eligibility')[:120]}...
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander(f"📋 Document Checklist & Apply for {scheme.get('name')}"):
                        st.markdown(f"**Mandatory Documents:** {scheme.get('required_documents')}")
                        st.markdown(f"**How to Apply:** {scheme.get('application_process')}")
                        if scheme.get('official_url'):
                            st.link_button("Visit Official Application Portal ↗", scheme.get('official_url'))

# ---------------------------------------------------------------------------
# Main Page View: 2. AI Citizen Assistant
# ---------------------------------------------------------------------------
elif nav_choice == "🤖 AI Citizen Assistant":
    st.markdown('<div class="main-title">🤖 AI Citizen Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Grounded RAG Policy Assistant providing step-by-step application instructions and verified government sources.</div>', unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Namaskara! I am your CivicGuide AI policy assistant. How can I assist you with government schemes, taluk offices, or eligibility guidelines today?"
            }
        ]

    # Quick Prompts
    st.markdown("**Quick Citizen Queries:**")
    qcols = st.columns(4)
    quick_queries = [
        "How to apply for Gruha Lakshmi Scheme?",
        "PM Surya Ghar solar subsidy steps",
        "Harapanahalli Taluk General Hospital services",
        "Yuva Nidhi Scheme eligibility criteria"
    ]
    def _generate_assistant_reply(query):
        q = query.lower()
        # 1. Match scheme from loaded verified schemes
        for s in schemes_list:
            s_name = (s.get("name") or "").lower()
            name_words = [w for w in s_name.replace("-", " ").replace(":", " ").split() if len(w) > 3 and w not in ["scheme", "yojana", "pradhan", "mantri"]]
            if any(w in q for w in name_words):
                gov_lvl = s.get('government_level', 'Government Scheme')
                state_lbl = f" • {s.get('state')}" if s.get('state') and s.get('state') != 'All India' else ""
                return f"""### 🏛️ Verified Scheme Guidance: {s.get('name')}
**Level:** {gov_lvl}{state_lbl} | **Sector:** {s.get('category')}

#### 💰 Direct Benefits:
{s.get('benefits')}

#### 👥 Eligibility Criteria:
{s.get('eligibility')}

#### 📋 Required Documents:
{s.get('required_documents')}

#### 📝 Step-by-Step Application Process:
{s.get('application_process')}

🔗 **Official Application Portal:** [{s.get('official_url')}]({s.get('official_url')})
"""

        # 2. Match public service office from loaded directory
        for sv in services_list:
            t = (sv.get("taluk") or "").lower()
            sv_name = (sv.get("name") or "").lower()
            if t and t in q and ("hospital" in q or "office" in q or "csc" in q or "centre" in q or "tahsildar" in q):
                return f"""### 📍 Verified Public Facility: {sv.get('name')}
**Category:** {sv.get('category')} | **Taluk:** {sv.get('taluk')} ({sv.get('district_city')}, {sv.get('state')})

- 🏢 **Address:** {sv.get('address')}
- 📞 **Helpline / Phone:** {sv.get('phone')}
- 🏛️ **Government Jurisdiction:** {sv.get('government_level')}

🔗 **Official Portal:** [{sv.get('official_url')}]({sv.get('official_url')})
"""

        # 3. Comprehensive standard citizen procedure
        return f"""### 🏛️ Verified Government Guidance for: "{query}"

1. **Eligibility Evaluation:** Check demographic qualifications (age, annual income, resident state, ration card status) under **📋 Eligibility Screening**.
2. **Mandatory Documents Checklist:**
   - Aadhaar Card (linked to active mobile number for OTP)
   - Income / Caste Certificate (Nadakacheri / Revenue Dept)
   - Bank Account linked to Aadhaar (NPCI / DBT enabled)
   - Ration Card (BPL Priority / Antyodaya / APL)
3. **Application Mode:**
   - **Online:** Official state or central portals (Seva Sindhu, myScheme, PM-Kisan)
   - **Offline / Assisted:** Visit your nearest Grama One, Karnataka One, or CSC Center
4. **Tracking:** Always record your Acknowledgement Number / Reference ID to verify status.

🔗 **National myScheme Portal:** [https://www.myscheme.gov.in](https://www.myscheme.gov.in)  
🔗 **Karnataka Seva Sindhu Portal:** [https://sevasindhu.karnataka.gov.in](https://sevasindhu.karnataka.gov.in)
"""

    for i, q in enumerate(quick_queries):
        if qcols[i].button(q, key=f"quick_{i}"):
            st.session_state.messages.append({"role": "user", "content": q})
            reply = _generate_assistant_reply(q)
            st.session_state.messages.append({"role": "assistant", "content": reply})

    # Render Chat History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input
    if user_query := st.chat_input("Ask a question about government schemes, eligibility, or local public offices..."):
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            response_text = _generate_assistant_reply(user_query)
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})

# ---------------------------------------------------------------------------
# Main Page View: 3. Eligibility Screening
# ---------------------------------------------------------------------------
elif nav_choice == "📋 Eligibility Screening":
    st.markdown('<div class="main-title">📋 Citizen Demographic Eligibility Checker</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Evaluate your demographic qualifications against all 47 verified Central & State government schemes.</div>', unsafe_allow_html=True)

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
        
        # Simple rule-based match
        matched = []
        for s in schemes_list:
            score = 0
            reasons = []
            desc = (s.get("description") or "").lower()
            elig = (s.get("eligibility") or "").lower()
            
            # Age checks
            if age >= 18:
                score += 1
                reasons.append("Adult citizen criteria satisfied (Age ≥ 18)")
            # Gender checks
            if gender.lower() == "female" and ("woman" in desc or "women" in desc or "girl" in desc):
                score += 2
                reasons.append("Eligible for specialized women & family welfare programs")
            # Occupation checks
            if "unemployed" in occupation.lower() and ("unemployed" in elig or "yuva" in desc):
                score += 2
                reasons.append("Qualifies for unemployment youth assistance")
            if "farmer" in occupation.lower() and ("farmer" in desc or "kisan" in desc):
                score += 2
                reasons.append("Qualifies for agricultural financial direct support")
            # Income checks
            if income <= 250000:
                score += 1
                reasons.append("Meets low/middle income threshold (≤ ₹2.5 Lakh)")

            status = "Qualified" if score >= 3 else "Conditions Apply" if score >= 2 else "Criteria Not Met"
            matched.append({"scheme": s, "status": status, "score": score, "reasons": reasons})

        matched.sort(key=lambda x: x["score"], reverse=True)
        
        c_qual, c_cond, c_all = st.columns(3)
        c_qual.metric("Qualified Schemes", len([m for m in matched if m["status"] == "Qualified"]))
        c_cond.metric("Conditions Apply", len([m for m in matched if m["status"] == "Conditions Apply"]))
        c_all.metric("Total Evaluated", len(matched))

        st.markdown("### **Top Matched Welfare Schemes For You**")
        for item in matched[:9]:
            s = item["scheme"]
            st.markdown(f"""
            <div class="scheme-card">
                <span class="scope-badge {'badge-central' if 'central' in (s.get('government_level') or '').lower() else 'badge-state'}">{s.get('government_level')}</span>
                <span style="float: right; font-weight: 800; color: {'#059669' if item['status'] == 'Qualified' else '#d97706'};">● {item['status']}</span>
                <h4 style="margin: 0.5rem 0; font-weight: 800;">{s.get('name')}</h4>
                <div class="benefit-box">💰 Benefit: {s.get('benefits')}</div>
                <div style="font-size: 0.85rem; color: #064e3b; font-weight: 600;">
                    ✓ Matched Criteria: {' • '.join(item['reasons'])}
                </div>
            </div>
            """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Main Page View: 4. Service Map & Taluk Locator
# ---------------------------------------------------------------------------
elif nav_choice == "📍 Service Map & Taluks":
    st.markdown('<div class="main-title">📍 Public Services Map & Taluk Directory</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Find Deputy Commissioner, Tahsildar, District Hospitals, and Grama One / CSC centers.</div>', unsafe_allow_html=True)

    m1, m2 = st.columns(2)
    with m1:
        map_state = st.selectbox("Select State", ["Karnataka", "Maharashtra", "Delhi", "Tamil Nadu"], index=0)
    with m2:
        dist_options = ["Vijayanagara (HQ: Hosapete)", "Ballari", "Bengaluru Urban", "Mysuru"] if map_state == "Karnataka" else ["Mumbai", "Pune", "Central Delhi", "Chennai"]
        map_district = st.selectbox("Select District", dist_options)

    # 6 Taluks for Vijayanagara District
    if "Vijayanagara" in map_district:
        st.markdown("#### **Administrative Taluks in Vijayanagara District (6 Taluks):**")
        taluk_cols = st.columns(6)
        taluks = ["Hosapete (HQ)", "Harapanahalli", "Kudligi", "Huvina Hadagali", "Hagaribommanahalli", "Kottur"]
        for idx, t_name in enumerate(taluks):
            taluk_cols[idx].button(f"📍 {t_name}", key=f"t_{idx}")

    # Map Visualization
    if services_list:
        df_services = pd.DataFrame(services_list)
        # Filter valid lat/long
        map_data = df_services.dropna(subset=['latitude', 'longitude'])
        if not map_data.empty:
            st.markdown("#### **Interactive Public Offices Map**")
            st.map(map_data[['latitude', 'longitude']], zoom=10)

        st.markdown("#### **Verified Public Service Offices Directory**")
        st.dataframe(
            df_services[['name', 'category', 'taluk', 'address', 'phone', 'government_level']],
            use_container_width=True
        )

# ---------------------------------------------------------------------------
# Main Page View: 5. About & GitHub
# ---------------------------------------------------------------------------
else:
    st.markdown('<div class="main-title">ℹ️ About CivicGuide AI</div>', unsafe_allow_html=True)
    st.markdown("""
    **CivicGuide AI** is an open-source, citizen-centric public services platform developed to bridge the gap between Indian citizens and government welfare initiatives.

    ### **Key Architecture Highlights**
    - **Frontend:** React 18, Vite, Tailwind CSS, Lucide React, Leaflet Maps.
    - **Backend:** Python Flask RESTful APIs, SQLAlchemy ORM, ChromaDB RAG Vector Store.
    - **Streamlit Cloud:** Native Streamlit application (`streamlit_app.py`) for one-click serverless cloud hosting.
    - **Open Source Repository:** [https://github.com/kpbinduprakasha-cpu/CivicGuide-AI](https://github.com/kpbinduprakasha-cpu/CivicGuide-AI)
    - **Lead Developer:** **K P Bindu Prakasha** ([@kpbinduprakasha-cpu](https://github.com/kpbinduprakasha-cpu))
    """)
    st.link_button("⭐ Star & View Repository on GitHub", "https://github.com/kpbinduprakasha-cpu/CivicGuide-AI")
