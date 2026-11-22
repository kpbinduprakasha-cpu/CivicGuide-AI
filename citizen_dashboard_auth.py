"""
CivicGuide AI - Citizen Authentication & Dashboard Module
Provides pixel-perfect Citizen Sign In, Registration, and Citizen Dashboard
matching official screenshots and React Tailwind components.
"""

import streamlit as st

def render_html(html_str: str):
    """Safely renders HTML in Streamlit without triggering Markdown 4-space code block formatting."""
    clean_lines = [line.strip() for line in html_str.strip().splitlines() if line.strip()]
    st.markdown("\n".join(clean_lines), unsafe_allow_html=True)

DEFAULT_CITIZEN_USER = {
    "full_name": "K P BINDUPRAKASHA",
    "user_id": "@kpb1ndup625",
    "email": "kpbinduprakasha@gmail.com",
    "mobile": "+91 9740397354",
    "age": 24,
    "sex": "Male",
    "state": "Karnataka",
    "languages": ["English", "Kannada"]
}

DEFAULT_APPLICATIONS = [
    {
        "id": "app-cent-1",
        "scheme_name": "PM-Kisan Samman Nidhi",
        "government_level": "Central Government",
        "category": "Agriculture",
        "ack_no": "ACK-PMKISAN-2026-9182",
        "applied_date": "12 Jan 2026",
        "status": "Approved",
        "benefit": "₹6,000 / year (Direct DBT)",
        "approval_date": "Sanctioned: 28 Jan 2026",
        "portal_url": "https://pmkisan.gov.in"
    },
    {
        "id": "app-cent-2",
        "scheme_name": "Ayushman Bharat - PM-JAY",
        "government_level": "Central Government",
        "category": "Healthcare",
        "ack_no": "ACK-ABPMJAY-2026-4431",
        "applied_date": "18 Jan 2026",
        "status": "Approved",
        "benefit": "₹5,00,000 / year Cashless Hospitalization",
        "approval_date": "Sanctioned: 02 Feb 2026",
        "portal_url": "https://pmjay.gov.in"
    },
    {
        "id": "app-cent-3",
        "scheme_name": "PM Surya Ghar: Muft Bijli Yojana",
        "government_level": "Central Government",
        "category": "Financial assistance",
        "ack_no": "ACK-SURYA-2026-1077",
        "applied_date": "05 Feb 2026",
        "status": "In Verification",
        "benefit": "Up to ₹78,000 Solar Rooftop Subsidy",
        "approval_date": "Expected by 25 Feb 2026",
        "portal_url": "https://pmsuryaghar.gov.in"
    },
    {
        "id": "app-cent-4",
        "scheme_name": "Pradhan Mantri Mudra Yojana (PMMY)",
        "government_level": "Central Government",
        "category": "Financial assistance",
        "ack_no": "ACK-MUDRA-2026-6209",
        "applied_date": "10 Feb 2026",
        "status": "Approved",
        "benefit": "₹50,000 Shishu Collateral-Free Micro-Credit",
        "approval_date": "Sanctioned: 14 Feb 2026",
        "portal_url": "https://www.mudra.org.in"
    },
    {
        "id": "app-state-1",
        "scheme_name": "Gruha Lakshmi Scheme",
        "government_level": "Karnataka State",
        "category": "Women and child welfare",
        "ack_no": "ACK-KAR-GL-2026-8801",
        "applied_date": "15 Jan 2026",
        "status": "Approved",
        "benefit": "₹2,000 / month (Direct DBT to Woman Head)",
        "approval_date": "Sanctioned: 25 Jan 2026",
        "portal_url": "https://sevasindhu.karnataka.gov.in"
    },
    {
        "id": "app-state-2",
        "scheme_name": "Yuva Nidhi Scheme",
        "government_level": "Karnataka State",
        "category": "Employment",
        "ack_no": "ACK-KAR-YN-2026-3190",
        "applied_date": "22 Jan 2026",
        "status": "Approved",
        "benefit": "₹3,000 / month Unemployment Assistance",
        "approval_date": "Sanctioned: 01 Feb 2026",
        "portal_url": "https://sevasindhu.karnataka.gov.in"
    },
    {
        "id": "app-state-3",
        "scheme_name": "SSP Post-Matric & Vidyasiri Scholarship",
        "government_level": "Karnataka State",
        "category": "Education",
        "ack_no": "ACK-KAR-SSP-2026-7241",
        "applied_date": "08 Feb 2026",
        "status": "Approved",
        "benefit": "Full College Tuition Reimbursement + Hostel Fee",
        "approval_date": "Sanctioned: 15 Feb 2026",
        "portal_url": "https://ssp.postmatric.karnataka.gov.in"
    },
    {
        "id": "app-state-4",
        "scheme_name": "Anna Bhagya Scheme (Cash Transfer)",
        "government_level": "Karnataka State",
        "category": "Food and civil supplies",
        "ack_no": "ACK-KAR-AB-2026-5510",
        "applied_date": "03 Feb 2026",
        "status": "In Verification",
        "benefit": "₹170 / month per person DBT (for 5 kg rice)",
        "approval_date": "Expected by 28 Feb 2026",
        "portal_url": "https://ahara.kar.nic.in"
    }
]

REGISTER_LANGUAGES_LIST = [
    'English', 'Hindi', 'Kannada', 'Telugu', 'Tamil', 
    'Marathi', 'Bengali', 'Gujarati', 'Malayalam', 'Punjabi', 
    'Odia', 'Assamese', 'Urdu', 'Sanskrit', 'Konkani', 
    'Nepali', 'Maithili', 'Santali', 'Kashmiri', 'Sindhi', 
    'Dogri', 'Manipuri', 'Bodo'
]


def render_login_view(_tr, all_languages, lang_code_map):
    """Renders Citizen Sign In Page matching media_1795365221491_d814aff9.png exactly."""
    _, center_col, _ = st.columns([1, 1.35, 1])
    
    with center_col:
        # Top Brand & Language Bar
        top_c1, top_c2 = st.columns([2.8, 1.2], vertical_alignment="center")
        with top_c1:
            render_html(f"""
            <div class="brand-wrap">
                <div class="brand-logo" style="width: 42px; height: 42px; border-radius: 0.85rem; font-size: 1.25rem;">🏛️</div>
                <div>
                    <div class="brand-title" style="font-size: 1.25rem; font-weight: 900;">{_tr('appName')} <span class="brand-pill" style="font-size: 0.65rem;">{_tr('allIndiaPill')}</span></div>
                    <div class="brand-subtitle" style="font-size: 0.72rem;">{_tr('tagline')}</div>
                </div>
            </div>
            """)
        with top_c2:
            selected_lang_name = st.session_state.get("top_navbar_language", "English (English)")
            st.selectbox(
                "Language",
                all_languages,
                index=all_languages.index(selected_lang_name) if selected_lang_name in all_languages else 0,
                key="login_page_language",
                label_visibility="collapsed"
            )
            if st.session_state.get("login_page_language"):
                st.session_state["top_navbar_language"] = st.session_state["login_page_language"]
                st.session_state["current_lang_code"] = lang_code_map.get(st.session_state["login_page_language"], "en")

        st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)

        # Main White Card (Exact match to screenshot 1)
        render_html(f"""
        <div style="background-color: #ffffff; border: 1px solid rgba(226, 232, 240, 0.9); border-radius: 2rem; padding: 2.25rem 2.25rem 1.75rem 2.25rem; box-shadow: 0 20px 25px -5px rgba(226, 232, 240, 0.7), 0 8px 10px -6px rgba(226, 232, 240, 0.4);">
            <div style="text-align: center; margin-bottom: 1.75rem;">
                <div style="display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.28rem 0.95rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 800; background-color: #ecfdf5; color: #065f46; border: 1px solid #a7f3d0; margin-bottom: 0.75rem;">
                    <span>🛡️</span> Citizen Sign In
                </div>
                <h1 style="font-size: 1.85rem; font-weight: 900; color: #0f172a; margin: 0; letter-spacing: -0.03em;">
                    Welcome to CivicGuide AI
                </h1>
            </div>
        </div>
        """)

        with st.container():
            # Field 1: USER ID
            render_html("""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: -0.85rem; margin-bottom: 0.35rem;">
                <span style="font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; color: #1e293b;">
                    USER ID <span style="color: #ef4444;">*</span>
                </span>
                <span style="font-size: 0.72rem; color: #94a3b8;">e.g. rahul123 or citizen</span>
            </div>
            """)

            user_id_val = st.text_input(
                "USER ID",
                value=st.session_state.get("login_uid_val", "@kpb1ndup625"),
                key="login_uid_val",
                label_visibility="collapsed"
            )

            # Field 2: PASSWORD
            render_html("""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.85rem; margin-bottom: 0.35rem;">
                <span style="font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; color: #1e293b;">
                    PASSWORD <span style="color: #ef4444;">*</span>
                </span>
                <span style="font-size: 0.72rem; font-weight: 700; color: #059669; cursor: pointer;">Forgot Password?</span>
            </div>
            """)

            pwd_val = st.text_input(
                "PASSWORD",
                value=st.session_state.get("login_pwd_val", "password123"),
                type="password",
                key="login_pwd_val",
                label_visibility="collapsed"
            )

            # Checkbox: Remember me
            st.markdown("<div style='height: 0.35rem;'></div>", unsafe_allow_html=True)
            rem_me = st.checkbox("Remember me on this browser", value=True, key="login_chk_remember")

            st.markdown("<div style='height: 0.35rem;'></div>", unsafe_allow_html=True)

            # Primary CTA Button
            if st.button("→] Login & Go to Home →", key="btn_login_home", type="primary", use_container_width=True):
                st.session_state["is_authenticated"] = True
                st.session_state["guest_mode"] = False
                st.session_state["current_page"] = "home"
                st.session_state["pending_nav_target"] = "home"
                st.rerun()

            # Divider
            render_html("""
            <div style="position: relative; margin: 1.25rem 0; text-align: center;">
                <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 0;">
                <span style="position: absolute; top: -9px; left: 50%; transform: translateX(-50%); background-color: #ffffff; padding: 0 0.85rem; font-size: 0.72rem; font-weight: 800; color: #94a3b8; letter-spacing: 0.05em;">
                    OR
                </span>
            </div>
            """)

            # Guest CTA Button
            if st.button("🧭 Browse Public Schemes as Guest", key="btn_guest_browse", use_container_width=True):
                st.session_state["guest_mode"] = True
                st.session_state["is_authenticated"] = False
                st.session_state["current_page"] = "home"
                st.session_state["pending_nav_target"] = "home"
                st.rerun()

            st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

            # Create Account Link
            render_html("""
            <div style="border-top: 1px solid #f1f5f9; padding-top: 1.25rem; text-align: center; font-size: 0.82rem; color: #64748b;">
                Don't have an account yet?
            </div>
            """)

            if st.button("Create Free Account", key="btn_goto_register_link", use_container_width=True):
                st.session_state["auth_page"] = "register"
                st.rerun()

        render_html("""
        <div style="text-align: center; margin-top: 1.75rem; font-size: 0.75rem; font-weight: 600; color: #94a3b8;">
            CivicGuide AI • Central & State Government Welfare Directory
        </div>
        """)


def render_register_view(_tr, all_languages, all_states, lang_code_map):
    """Renders Citizen Account Registration Page matching media_1795365258023_54a6e44b.png exactly."""
    _, center_col, _ = st.columns([1, 2.4, 1])

    with center_col:
        # Top Bar: Back link, Center Logo, Right Language
        top_c1, top_c2, top_c3 = st.columns([1.6, 2.8, 1.4], vertical_alignment="center")
        with top_c1:
            if st.button("❮ Back to Sign In", key="btn_back_to_login", use_container_width=True):
                st.session_state["auth_page"] = "login"
                st.rerun()
        with top_c2:
            render_html(f"""
            <div style="display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
                <div class="brand-logo" style="width: 34px; height: 34px; border-radius: 0.65rem; font-size: 1.05rem;">🏛️</div>
                <span style="font-weight: 800; font-size: 1.15rem; color: #0f172a; tracking-tight">{_tr('appName')}</span>
            </div>
            """)
        with top_c3:
            selected_lang_name = st.session_state.get("top_navbar_language", "English (English)")
            st.selectbox(
                "Language",
                all_languages,
                index=all_languages.index(selected_lang_name) if selected_lang_name in all_languages else 0,
                key="reg_page_language",
                label_visibility="collapsed"
            )
            if st.session_state.get("reg_page_language"):
                st.session_state["top_navbar_language"] = st.session_state["reg_page_language"]
                st.session_state["current_lang_code"] = lang_code_map.get(st.session_state["reg_page_language"], "en")

        st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)

        # Main White Card (Exact match to screenshot 2)
        render_html("""
        <div style="background-color: #ffffff; border: 1px solid rgba(226, 232, 240, 0.9); border-radius: 2rem; padding: 2.25rem 2.5rem 1.75rem 2.5rem; box-shadow: 0 20px 25px -5px rgba(226, 232, 240, 0.7);">
            <div style="text-align: center; margin-bottom: 1.75rem;">
                <div style="display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.28rem 0.95rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 800; background-color: #ecfdf5; color: #065f46; border: 1px solid #a7f3d0; margin-bottom: 0.65rem;">
                    <span>👤⁺</span> One-Time Citizen Registration
                </div>
                <h1 style="font-size: 1.95rem; font-weight: 900; color: #0f172a; margin: 0 0 0.35rem 0; letter-spacing: -0.025em;">
                    Create Your Account
                </h1>
                <p style="font-size: 0.8rem; color: #64748b; margin: 0 auto; max-width: 480px; line-height: 1.45;">
                    Fill in your citizen details. A unique User ID will be generated and a 6-digit OTP will be sent to your email.
                </p>
            </div>
        </div>
        """)

        with st.container():
            # Field 1: FULL NAME
            render_html("""
            <div style="margin-top: -0.85rem; margin-bottom: 0.35rem;">
                <span style="font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; color: #1e293b;">
                    1. FULL NAME <span style="color: #ef4444;">*</span>
                </span>
            </div>
            """)

            r_name = st.text_input(
                "1. FULL NAME",
                value=st.session_state.get("reg_name_val", "Rahul Kumar"),
                placeholder="e.g. Rahul Kumar",
                key="reg_name_val",
                label_visibility="collapsed"
            )

            render_html("""
            <p style="font-size: 0.72rem; color: #94a3b8; margin: 0.25rem 0 1rem 0;">
                A unique User ID (e.g. @rahul123) will be auto-generated from your name.
            </p>
            """)

            # Grid Row 1: AGE & MOBILE NUMBER
            c_age, c_mob = st.columns(2)
            with c_age:
                render_html("""
                <div style="margin-bottom: 0.35rem;">
                    <span style="font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; color: #1e293b;">
                        2. AGE <span style="color: #ef4444;">*</span>
                    </span>
                </div>
                """)
                r_age = st.number_input(
                    "2. AGE",
                    min_value=1,
                    max_value=120,
                    value=int(st.session_state.get("reg_age_val", 24)),
                    key="reg_age_val",
                    label_visibility="collapsed"
                )

            with c_mob:
                render_html("""
                <div style="margin-bottom: 0.35rem;">
                    <span style="font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; color: #1e293b;">
                        3. MOBILE NUMBER <span style="color: #ef4444;">*</span>
                    </span>
                </div>
                """)
                r_mob = st.text_input(
                    "3. MOBILE NUMBER",
                    value=st.session_state.get("reg_mob_val", "9876543210"),
                    placeholder="9876543210",
                    key="reg_mob_val",
                    label_visibility="collapsed"
                )

            st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

            # Grid Row 2: STATE / UT & SEX
            c_state, c_sex = st.columns(2)
            with c_state:
                render_html("""
                <div style="margin-bottom: 0.35rem;">
                    <span style="font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; color: #1e293b;">
                        4. STATE / UT <span style="color: #ef4444;">*</span>
                    </span>
                </div>
                """)
                states_clean = [s for s in all_states if s != "All India"]
                def_state_idx = states_clean.index("Karnataka") if "Karnataka" in states_clean else 0
                r_state = st.selectbox(
                    "4. STATE / UT",
                    states_clean,
                    index=def_state_idx,
                    key="reg_state_val",
                    label_visibility="collapsed"
                )

            with c_sex:
                render_html("""
                <div style="margin-bottom: 0.35rem;">
                    <span style="font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; color: #1e293b;">
                        5. SEX <span style="color: #ef4444;">*</span>
                    </span>
                </div>
                """)

                if "reg_sex_selected" not in st.session_state:
                    st.session_state["reg_sex_selected"] = "Male"
                cur_sex = st.session_state["reg_sex_selected"]

                s1, s2, s3, s4 = st.columns(4)
                with s1:
                    if st.button("Male", key="btn_sex_male", use_container_width=True):
                        st.session_state["reg_sex_selected"] = "Male"
                        st.rerun()
                with s2:
                    if st.button("Female", key="btn_sex_female", use_container_width=True):
                        st.session_state["reg_sex_selected"] = "Female"
                        st.rerun()
                with s3:
                    if st.button("Other", key="btn_sex_other1", use_container_width=True):
                        st.session_state["reg_sex_selected"] = "Other"
                        st.rerun()
                with s4:
                    if st.button("Other", key="btn_sex_other2", use_container_width=True):
                        st.session_state["reg_sex_selected"] = "Prefer not to say"
                        st.rerun()

            st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

            # Field 6: LANGUAGES KNOWN (SELECT MULTIPLE)
            if "reg_selected_langs" not in st.session_state:
                st.session_state["reg_selected_langs"] = ["English", "Kannada"]
            sel_langs = st.session_state["reg_selected_langs"]

            render_html(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.45rem;">
                <span style="font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; color: #1e293b;">
                    6. LANGUAGES KNOWN (SELECT MULTIPLE) <span style="color: #ef4444;">*</span>
                </span>
                <span style="font-size: 0.72rem; color: #64748b; font-weight: 600;">
                    {len(sel_langs)} selected
                </span>
            </div>
            """)

            def toggle_lang(lang_name):
                if lang_name in st.session_state["reg_selected_langs"]:
                    if len(st.session_state["reg_selected_langs"]) > 1:
                        st.session_state["reg_selected_langs"].remove(lang_name)
                else:
                    st.session_state["reg_selected_langs"].append(lang_name)
                st.rerun()

            # Render 23 language pills matching Screenshot 2
            with st.container():
                st.markdown("""
                <div style="background-color: rgba(248, 250, 252, 0.7); border: 1px solid #e2e8f0; border-radius: 1.25rem; padding: 0.75rem 0.65rem; margin-bottom: 0.85rem;">
                """, unsafe_allow_html=True)
                
                # 3 rows of 7, 7, 7, 2
                l_cols1 = st.columns(7)
                for i, lang in enumerate(REGISTER_LANGUAGES_LIST[:7]):
                    with l_cols1[i]:
                        is_sel = lang in sel_langs
                        lbl = f"✓ {lang}" if is_sel else lang
                        if st.button(lbl, key=f"btn_lang_{lang}", use_container_width=True):
                            toggle_lang(lang)

                l_cols2 = st.columns(7)
                for i, lang in enumerate(REGISTER_LANGUAGES_LIST[7:14]):
                    with l_cols2[i]:
                        is_sel = lang in sel_langs
                        lbl = f"✓ {lang}" if is_sel else lang
                        if st.button(lbl, key=f"btn_lang_{lang}", use_container_width=True):
                            toggle_lang(lang)

                l_cols3 = st.columns(7)
                for i, lang in enumerate(REGISTER_LANGUAGES_LIST[14:21]):
                    with l_cols3[i]:
                        is_sel = lang in sel_langs
                        lbl = f"✓ {lang}" if is_sel else lang
                        if st.button(lbl, key=f"btn_lang_{lang}", use_container_width=True):
                            toggle_lang(lang)

                l_cols4 = st.columns(7)
                for i, lang in enumerate(REGISTER_LANGUAGES_LIST[21:23]):
                    with l_cols4[i]:
                        is_sel = lang in sel_langs
                        lbl = f"✓ {lang}" if is_sel else lang
                        if st.button(lbl, key=f"btn_lang_{lang}", use_container_width=True):
                            toggle_lang(lang)

                st.markdown("</div>", unsafe_allow_html=True)

            # Field 7: EMAIL ADDRESS
            render_html("""
            <div style="margin-bottom: 0.35rem;">
                <span style="font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; color: #1e293b;">
                    7. EMAIL ADDRESS (FOR OTP VERIFICATION) <span style="color: #ef4444;">*</span>
                </span>
            </div>
            """)

            r_email = st.text_input(
                "7. EMAIL ADDRESS",
                value=st.session_state.get("reg_email_val", "citizen@example.com"),
                placeholder="citizen@example.com",
                key="reg_email_val",
                label_visibility="collapsed"
            )

            render_html("""
            <p style="font-size: 0.72rem; color: #94a3b8; margin: 0.25rem 0 1rem 0;">
                A 6-digit OTP will be sent to this email upon submission.
            </p>
            """)

            # Grid Row 3: PASSWORD & CONFIRM PASSWORD
            c_p1, c_p2 = st.columns(2)
            with c_p1:
                render_html("""
                <div style="margin-bottom: 0.35rem;">
                    <span style="font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; color: #1e293b;">
                        8. PASSWORD <span style="color: #ef4444;">*</span>
                    </span>
                </div>
                """)
                r_pwd = st.text_input(
                    "8. PASSWORD",
                    value=st.session_state.get("reg_p1_val", "password123"),
                    type="password",
                    placeholder="Min 8 characters",
                    key="reg_p1_val",
                    label_visibility="collapsed"
                )

            with c_p2:
                render_html("""
                <div style="margin-bottom: 0.35rem;">
                    <span style="font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; color: #1e293b;">
                        9. CONFIRM PASSWORD <span style="color: #ef4444;">*</span>
                    </span>
                </div>
                """)
                r_cpwd = st.text_input(
                    "9. CONFIRM PASSWORD",
                    value=st.session_state.get("reg_p2_val", "password123"),
                    type="password",
                    placeholder="Repeat your password",
                    key="reg_p2_val",
                    label_visibility="collapsed"
                )

            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

            # Submit CTA
            if st.button("Create Account & Send OTP →", key="btn_submit_reg", use_container_width=True, type="primary"):
                st.session_state["citizen_user"] = {
                    "full_name": r_name.strip() or "Rahul Kumar",
                    "user_id": f"@{r_name.lower().replace(' ', '')[:10]}123" if r_name else "@rahul123",
                    "email": r_email.strip().lower() or "citizen@example.com",
                    "mobile": f"+91 {r_mob.strip()}" if r_mob else "+91 9876543210",
                    "age": int(r_age),
                    "sex": cur_sex,
                    "state": r_state,
                    "languages": sel_langs if sel_langs else ["English", "Kannada"]
                }
                st.session_state["is_authenticated"] = True
                st.session_state["guest_mode"] = False
                st.session_state["current_page"] = "home"
                st.session_state["pending_nav_target"] = "home"
                st.rerun()

            render_html("""
            <div style="border-top: 1px solid #f1f5f9; padding-top: 1.25rem; margin-top: 1rem; text-align: center; font-size: 0.82rem; color: #64748b;">
                Already have an account?
            </div>
            """)

            if st.button("Sign In with User ID", key="btn_nav_to_login_link", use_container_width=True):
                st.session_state["auth_page"] = "login"
                st.rerun()


def render_citizen_dashboard(_tr, all_languages, all_states, lang_code_map):
    """Renders Citizen Dashboard matching Images 1, 2, and 3 exactly."""
    user = st.session_state.get("citizen_user", DEFAULT_CITIZEN_USER)
    apps = st.session_state.get("citizen_applications", DEFAULT_APPLICATIONS)

    # -----------------------------------------------------------------------
    # Top Bar: Matching Image 1 Exactly
    # -----------------------------------------------------------------------
    top_c1, top_c2 = st.columns([3.5, 3.5], vertical_alignment="center")
    with top_c1:
        render_html(f"""
        <div class="brand-wrap">
            <div class="brand-logo" style="width: 40px; height: 40px; border-radius: 0.85rem; font-size: 1.25rem;">🏛️</div>
            <div>
                <div class="brand-title">{_tr('appName')} <span class="brand-pill">{_tr('allIndiaPill')}</span></div>
                <div class="brand-subtitle">{_tr('citizenDashboard')}</div>
            </div>
        </div>
        """)
    with top_c2:
        btn_home_col, lang_col, logout_col = st.columns([2.4, 2.6, 1.8], vertical_alignment="center")
        with btn_home_col:
            if st.button(f"🏠 {_tr('goToHome')}", key="dash_top_btn_home", use_container_width=True):
                st.session_state["current_page"] = "home"
                st.session_state["pending_nav_target"] = "home"
                st.rerun()
        with lang_col:
            selected_lang_name = st.session_state.get("top_navbar_language", "English (English)")
            st.selectbox(
                "Language",
                all_languages,
                index=all_languages.index(selected_lang_name) if selected_lang_name in all_languages else 0,
                key="dash_page_lang",
                label_visibility="collapsed"
            )
            if st.session_state.get("dash_page_lang"):
                st.session_state["top_navbar_language"] = st.session_state["dash_page_lang"]
                st.session_state["current_lang_code"] = lang_code_map.get(st.session_state["dash_page_lang"], "en")
        with logout_col:
            if st.button(f"🚪 {_tr('logout')}", key="dash_top_btn_logout", use_container_width=True):
                st.session_state["is_authenticated"] = False
                st.session_state["guest_mode"] = False
                st.session_state["auth_page"] = "login"
                st.session_state["current_page"] = "home"
                st.rerun()

    st.markdown("<hr style='margin-top: 0.5rem; margin-bottom: 1.5rem; border-color: #e2e8f0;'>", unsafe_allow_html=True)

    # -----------------------------------------------------------------------
    # Section 1: Citizen Profile & Direct Application Tools (Matches Image 1)
    # -----------------------------------------------------------------------
    p_left, p_right = st.columns([2.1, 1.1])

    with p_left:
        # Profile Card
        hdr_c1, hdr_c2 = st.columns([3, 2], vertical_alignment="center")
        with hdr_c1:
            render_html(f"""
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.25rem;">👤</span>
                <span style="font-size: 1.35rem; font-weight: 900; color: #0f172a;">{_tr('citizenProfile')}</span>
            </div>
            <p style="font-size: 0.8rem; color: #64748b; margin: 0.2rem 0 1rem 0;">
                {_tr('citizenProfileSub')}
            </p>
            """)
        with hdr_c2:
            e_col1, e_col2 = st.columns(2)
            with e_col1:
                if st.button("✏️ Edit Profile", key="btn_edit_profile", use_container_width=True):
                    st.session_state["show_edit_prof"] = not st.session_state.get("show_edit_prof", False)
                    st.rerun()
            with e_col2:
                if st.button("🔒 Change Password", key="btn_change_pwd", use_container_width=True):
                    st.session_state["show_change_pwd"] = not st.session_state.get("show_change_pwd", False)
                    st.rerun()

        # Optional Edit Profile Form Drawer
        if st.session_state.get("show_edit_prof", False):
            with st.container():
                st.markdown("""
                <div style="background-color: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 1rem; padding: 1.25rem; margin-bottom: 1rem;">
                    <span style="font-size: 0.85rem; font-weight: 800; color: #0f172a;">✏️ Edit Citizen Profile Attributes</span>
                </div>
                """, unsafe_allow_html=True)
                ed_name = st.text_input("Full Legal Name", value=user.get("full_name", "K P BINDUPRAKASHA"), key="ed_inp_name")
                ed_c1, ed_c2 = st.columns(2)
                with ed_c1:
                    ed_age = st.number_input("Age", min_value=1, max_value=120, value=int(user.get("age", 24)), key="ed_inp_age")
                with ed_c2:
                    ed_mob = st.text_input("Mobile Number", value=user.get("mobile", "+91 9740397354").replace("+91 ", ""), key="ed_inp_mob")
                
                ed_c3, ed_c4 = st.columns(2)
                with ed_c3:
                    clean_states = [s for s in all_states if s != "All India"]
                    state_val = user.get("state", "Karnataka")
                    idx = clean_states.index(state_val) if state_val in clean_states else 0
                    ed_state = st.selectbox("State / Territory", clean_states, index=idx, key="ed_inp_state")
                with ed_c4:
                    sex_options = ["Male", "Female", "Other"]
                    sex_val = user.get("sex", "Male")
                    sex_idx = sex_options.index(sex_val) if sex_val in sex_options else 0
                    ed_sex = st.selectbox("Sex", sex_options, index=sex_idx, key="ed_inp_sex")
                
                ed_langs = st.multiselect(
                    "Languages Known",
                    [l.split(" ")[0] for l in all_languages],
                    default=user.get("languages", ["English", "Kannada"]),
                    key="ed_inp_langs"
                )

                if st.button("Save Profile Changes", key="btn_save_profile_ed", type="primary"):
                    st.session_state["citizen_user"]["full_name"] = ed_name.strip()
                    st.session_state["citizen_user"]["age"] = int(ed_age)
                    st.session_state["citizen_user"]["mobile"] = f"+91 {ed_mob.strip()}"
                    st.session_state["citizen_user"]["state"] = ed_state
                    st.session_state["citizen_user"]["sex"] = ed_sex
                    st.session_state["citizen_user"]["languages"] = ed_langs
                    st.session_state["show_edit_prof"] = False
                    st.success("Profile attributes updated successfully!")
                    st.rerun()

        # Optional Change Password Form Drawer
        if st.session_state.get("show_change_pwd", False):
            with st.container():
                st.markdown("""
                <div style="background-color: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 1rem; padding: 1.25rem; margin-bottom: 1rem;">
                    <span style="font-size: 0.85rem; font-weight: 800; color: #0f172a;">🔒 Change Account Password</span>
                </div>
                """, unsafe_allow_html=True)
                st.text_input("Current Password", value="", type="password", key="pwd_cur")
                p_new = st.text_input("New Password (Min 8 characters)", value="", type="password", key="pwd_new")
                p_conf = st.text_input("Confirm New Password", value="", type="password", key="pwd_conf")
                if st.button("Update Password", key="btn_save_pwd", type="primary"):
                    if len(p_new) < 8:
                        st.error("Password must be at least 8 characters.")
                    elif p_new != p_conf:
                        st.error("Passwords do not match.")
                    else:
                        st.session_state["show_change_pwd"] = False
                        st.success("Password updated successfully!")
                        st.rerun()

        # Details Grid (Matches Image 1) - Without GitHub button & rendered cleanly via render_html
        lang_pills = " ".join([
            f'<span style="background-color: #ffffff; border: 1px solid #cbd5e1; border-radius: 9999px; font-size: 0.75rem; font-weight: 700; color: #047857; padding: 0.2rem 0.75rem; display: inline-block;">{l}</span>'
            for l in user.get('languages', ['English', 'Kannada'])
        ])

        render_html(f"""
        <div style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 1.5rem; padding: 1.75rem; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">
                <div style="background-color: #f8fafc; border: 1px solid #f1f5f9; border-radius: 1rem; padding: 0.85rem 1.15rem;">
                    <div style="font-size: 0.65rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; margin-bottom: 0.25rem;">FULL NAME</div>
                    <div style="font-size: 1.05rem; font-weight: 800; color: #0f172a;">{user.get('full_name')}</div>
                </div>
                <div style="background-color: #f8fafc; border: 1px solid #f1f5f9; border-radius: 1rem; padding: 0.85rem 1.15rem;">
                    <div style="font-size: 0.65rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; margin-bottom: 0.25rem;">USER ID (LOGIN ID)</div>
                    <div style="font-size: 1.05rem; font-weight: 800; color: #047857;">{user.get('user_id')}</div>
                </div>
                <div style="background-color: #f8fafc; border: 1px solid #f1f5f9; border-radius: 1rem; padding: 0.85rem 1.15rem;">
                    <div style="font-size: 0.65rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; margin-bottom: 0.25rem;">EMAIL ADDRESS</div>
                    <div style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.95rem; font-weight: 800; color: #0f172a;">
                        <span>{user.get('email')}</span>
                        <span style="background-color: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; border-radius: 9999px; font-size: 0.65rem; font-weight: 800; padding: 0.1rem 0.5rem;">Verified</span>
                    </div>
                </div>
                <div style="background-color: #f8fafc; border: 1px solid #f1f5f9; border-radius: 1rem; padding: 0.85rem 1.15rem;">
                    <div style="font-size: 0.65rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; margin-bottom: 0.25rem;">MOBILE NUMBER</div>
                    <div style="font-size: 1.05rem; font-weight: 800; color: #0f172a;">{user.get('mobile')}</div>
                </div>
                <div style="background-color: #f8fafc; border: 1px solid #f1f5f9; border-radius: 1rem; padding: 0.85rem 1.15rem;">
                    <div style="font-size: 0.65rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; margin-bottom: 0.25rem;">AGE & SEX</div>
                    <div style="font-size: 1.05rem; font-weight: 800; color: #0f172a;">{user.get('age')} years old • {user.get('sex')}</div>
                </div>
                <div style="background-color: #f8fafc; border: 1px solid #f1f5f9; border-radius: 1rem; padding: 0.85rem 1.15rem;">
                    <div style="font-size: 0.65rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; margin-bottom: 0.25rem;">STATE / TERRITORY</div>
                    <div style="font-size: 1.05rem; font-weight: 800; color: #0f172a;">📍 {user.get('state')}</div>
                </div>
            </div>
            <div style="background-color: #f8fafc; border: 1px solid #f1f5f9; border-radius: 1rem; padding: 0.85rem 1.15rem; margin-top: 1rem;">
                <div style="font-size: 0.65rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; margin-bottom: 0.35rem;">LANGUAGES KNOWN</div>
                <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                    {lang_pills}
                </div>
            </div>
        </div>
        """)

    with p_right:
        # Direct Application Tools (Matches Image 1)
        render_html(f"""
        <div style="font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; margin-bottom: 0.65rem;">
            {_tr('directTools')}
        </div>
        """)

        if st.button("🏛️ Government Schemes\nBrowse verified national & state welfare", key="tool_btn_schemes", use_container_width=True):
            st.session_state["pending_nav_target"] = "schemes"
            st.session_state["current_page"] = "schemes"
            st.rerun()

        st.markdown("<div style='height: 0.4rem;'></div>", unsafe_allow_html=True)

        if st.button("🤖 AI Policy Chatbot\nAsk questions in regional languages", key="tool_btn_chat", use_container_width=True):
            st.session_state["pending_nav_target"] = "chatbot"
            st.session_state["current_page"] = "chatbot"
            st.rerun()

        st.markdown("<div style='height: 0.4rem;'></div>", unsafe_allow_html=True)

        if st.button("📋 Eligibility Checker\nFind matching welfare programs", key="tool_btn_elig", use_container_width=True):
            st.session_state["pending_nav_target"] = "eligibility"
            st.session_state["current_page"] = "eligibility"
            st.rerun()

        st.markdown("<div style='height: 0.4rem;'></div>", unsafe_allow_html=True)

        if st.button("📍 Government Service Map\nLocate CSCs, hospitals & offices", key="tool_btn_map", use_container_width=True):
            st.session_state["pending_nav_target"] = "serviceMap"
            st.session_state["current_page"] = "serviceMap"
            st.rerun()

    st.markdown("<div style='height: 1.75rem;'></div>", unsafe_allow_html=True)

    # -----------------------------------------------------------------------
    # Section 2: Scheme Applications & Approvals Tracker (Matches Image 2)
    # -----------------------------------------------------------------------
    tr_h1, tr_h2 = st.columns([4, 1.2], vertical_alignment="center")
    with tr_h1:
        render_html(f"""
        <div style="display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.2rem 0.65rem; border-radius: 9999px; font-size: 0.72rem; font-weight: 800; background-color: #eff6ff; color: #1e40af; border: 1px solid #bfdbfe; margin-bottom: 0.35rem;">
            🕒 Central & State Government Applications Overview
        </div>
        <h2 style="font-size: 1.55rem; font-weight: 900; color: #0f172a; margin: 0 0 0.2rem 0;">
            {_tr('trackerTitle')}
        </h2>
        <p style="font-size: 0.8rem; color: #64748b; margin: 0;">
            {_tr('trackerSub')}
        </p>
        """)
    with tr_h2:
        if st.button(f"➕ {_tr('applySchemeBtn')}", key="dash_btn_apply_scheme", type="primary", use_container_width=True):
            st.session_state["pending_nav_target"] = "schemes"
            st.session_state["current_page"] = "schemes"
            st.rerun()

    st.markdown("<div style='height: 0.85rem;'></div>", unsafe_allow_html=True)

    # 4 Metric Cards (Image 2)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        render_html("""
        <div style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 1.25rem; padding: 1.25rem; box-shadow: 0 1px 3px rgba(0,0,0,0.02); height: 100%;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                <span style="font-size: 0.7rem; font-weight: 800; text-transform: uppercase; color: #1d4ed8; letter-spacing: 0.05em;">TOTAL APPLIED</span>
                <span style="background-color: #eff6ff; color: #1d4ed8; border-radius: 0.5rem; padding: 0.25rem 0.5rem; font-size: 0.85rem;">📄</span>
            </div>
            <div style="display: flex; align-items: baseline; gap: 0.4rem; margin-bottom: 0.2rem;">
                <span style="font-size: 2rem; font-weight: 900; color: #0f172a;">8</span>
                <span style="font-size: 0.85rem; font-weight: 800; color: #475569;">Schemes</span>
            </div>
            <div style="font-size: 0.75rem; color: #64748b; margin-bottom: 1rem;">4 Central • 4 State Govts</div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #f1f5f9; padding-top: 0.75rem; font-size: 0.72rem;">
                <span style="color: #64748b;">Application Portfolio</span>
                <span style="font-weight: 800; color: #1d4ed8; background-color: #eff6ff; padding: 0.15rem 0.5rem; border-radius: 0.35rem;">100% Active</span>
            </div>
        </div>
        """)

    with m2:
        render_html("""
        <div style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 1.25rem; padding: 1.25rem; box-shadow: 0 1px 3px rgba(0,0,0,0.02); height: 100%;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                <span style="font-size: 0.7rem; font-weight: 800; text-transform: uppercase; color: #047857; letter-spacing: 0.05em;">TOTAL APPROVED</span>
                <span style="background-color: #ecfdf5; color: #047857; border-radius: 0.5rem; padding: 0.25rem 0.5rem; font-size: 0.85rem;">✓</span>
            </div>
            <div style="display: flex; align-items: baseline; gap: 0.4rem; margin-bottom: 0.2rem;">
                <span style="font-size: 2rem; font-weight: 900; color: #047857;">6</span>
                <span style="font-size: 0.85rem; font-weight: 800; color: #047857;">Sanctioned</span>
            </div>
            <div style="font-size: 0.75rem; color: #64748b; margin-bottom: 1rem;">75% Overall Approval Success</div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #f1f5f9; padding-top: 0.75rem; font-size: 0.72rem;">
                <span style="color: #64748b;">Verified Direct Benefits</span>
                <span style="font-weight: 800; color: #047857; background-color: #ecfdf5; padding: 0.15rem 0.5rem; border-radius: 0.35rem;">Active</span>
            </div>
        </div>
        """)

    with m3:
        render_html("""
        <div style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 1.25rem; padding: 1.25rem; box-shadow: 0 1px 3px rgba(0,0,0,0.02); height: 100%;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                <span style="font-size: 0.7rem; font-weight: 800; text-transform: uppercase; color: #b45309; letter-spacing: 0.05em;">IN VERIFICATION</span>
                <span style="background-color: #fffbeb; color: #b45309; border-radius: 0.5rem; padding: 0.25rem 0.5rem; font-size: 0.85rem;">⏳</span>
            </div>
            <div style="display: flex; align-items: baseline; gap: 0.4rem; margin-bottom: 0.2rem;">
                <span style="font-size: 2rem; font-weight: 900; color: #b45309;">2</span>
                <span style="font-size: 0.85rem; font-weight: 800; color: #b45309;">Processing</span>
            </div>
            <div style="font-size: 0.75rem; color: #64748b; margin-bottom: 1rem;">1 Central • 1 State Under Review</div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #f1f5f9; padding-top: 0.75rem; font-size: 0.72rem;">
                <span style="color: #64748b;">Departmental Scrutiny</span>
                <span style="font-weight: 800; color: #b45309; background-color: #fffbeb; padding: 0.15rem 0.5rem; border-radius: 0.35rem;">Pending Signoff</span>
            </div>
        </div>
        """)

    with m4:
        render_html("""
        <div style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 1.25rem; padding: 1.25rem; box-shadow: 0 1px 3px rgba(0,0,0,0.02); height: 100%;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                <span style="font-size: 0.7rem; font-weight: 800; text-transform: uppercase; color: #7e22ce; letter-spacing: 0.05em;">ANNUAL SUPPORT</span>
                <span style="background-color: #faf5ff; color: #7e22ce; border-radius: 0.5rem; padding: 0.25rem 0.5rem; font-size: 0.85rem;">🪙</span>
            </div>
            <div style="display: flex; align-items: baseline; gap: 0.4rem; margin-bottom: 0.2rem;">
                <span style="font-size: 2rem; font-weight: 900; color: #7e22ce;">₹66,000+</span>
            </div>
            <div style="font-size: 0.75rem; color: #64748b; margin-bottom: 1rem;">Direct Cash DBT + ₹5L Health Cover</div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #f1f5f9; padding-top: 0.75rem; font-size: 0.72rem;">
                <span style="color: #64748b;">Direct to Bank Account</span>
                <span style="font-weight: 800; color: #7e22ce; background-color: #faf5ff; padding: 0.15rem 0.5rem; border-radius: 0.35rem;">Aadhaar Linked</span>
            </div>
        </div>
        """)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Circle Graphs (Matches Image 2)
    render_html(f"""
    <div style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 1.5rem; padding: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
            <div>
                <div style="display: inline-flex; align-items: center; gap: 0.4rem; font-size: 0.85rem; font-weight: 800; color: #047857; margin-bottom: 0.2rem;">
                    🕒 {_tr('circleGraphsTitle')}
                </div>
                <div style="font-size: 0.78rem; color: #64748b;">
                    {_tr('circleGraphsSub')}
                </div>
            </div>
            <span style="font-size: 0.72rem; font-weight: 800; color: #475569; background-color: #f1f5f9; padding: 0.25rem 0.65rem; border-radius: 9999px;">
                Official 2026 Audit View
            </span>
        </div>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.25rem;">
            <!-- Graph 1 -->
            <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 1.25rem; padding: 1.5rem; text-align: center;">
                <div style="font-size: 0.72rem; font-weight: 800; text-transform: uppercase; color: #475569; letter-spacing: 0.05em; margin-bottom: 1rem;">
                    OVERALL APPROVAL RATE
                </div>
                <div style="position: relative; width: 120px; height: 120px; margin: 0 auto 0.75rem auto;">
                    <svg width="120" height="120" viewBox="0 0 100 100">
                        <circle cx="50" cy="50" r="40" stroke="#e2e8f0" stroke-width="10" fill="transparent" />
                        <circle cx="50" cy="50" r="40" stroke="#10b981" stroke-width="10" fill="transparent"
                                stroke-dasharray="251.3" stroke-dashoffset="62.8" stroke-linecap="round"
                                transform="rotate(-90 50 50)" />
                        <text x="50" y="56" font-size="20" font-weight="900" text-anchor="middle" fill="#0f172a">75%</text>
                    </svg>
                </div>
                <div style="font-size: 0.75rem; font-weight: 700; color: #047857;">6 of 8 Sanctioned</div>
                <div style="font-size: 0.68rem; color: #64748b;">Direct benefit transfer enabled</div>
            </div>
            <!-- Graph 2 -->
            <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 1.25rem; padding: 1.5rem; text-align: center;">
                <div style="font-size: 0.72rem; font-weight: 800; text-transform: uppercase; color: #475569; letter-spacing: 0.05em; margin-bottom: 1rem;">
                    CENTRAL VS. STATE GOVERNMENT
                </div>
                <div style="position: relative; width: 120px; height: 120px; margin: 0 auto 0.75rem auto;">
                    <svg width="120" height="120" viewBox="0 0 100 100">
                        <circle cx="50" cy="50" r="40" stroke="#3b82f6" stroke-width="10" fill="transparent"
                                stroke-dasharray="251.3" stroke-dashoffset="125.65" stroke-linecap="round"
                                transform="rotate(-90 50 50)" />
                        <circle cx="50" cy="50" r="40" stroke="#10b981" stroke-width="10" fill="transparent"
                                stroke-dasharray="251.3" stroke-dashoffset="125.65" stroke-linecap="round"
                                transform="rotate(90 50 50)" />
                        <text x="50" y="56" font-size="18" font-weight="900" text-anchor="middle" fill="#0f172a">50 / 50</text>
                    </svg>
                </div>
                <div style="font-size: 0.75rem; font-weight: 700; color: #1e40af;">4 Central • 4 State</div>
                <div style="font-size: 0.68rem; color: #64748b;">Balanced jurisdictional reach</div>
            </div>
            <!-- Graph 3 -->
            <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 1.25rem; padding: 1.5rem; text-align: center;">
                <div style="font-size: 0.72rem; font-weight: 800; text-transform: uppercase; color: #475569; letter-spacing: 0.05em; margin-bottom: 1rem;">
                    APPLICATION STATUS LIFECYCLE
                </div>
                <div style="position: relative; width: 120px; height: 120px; margin: 0 auto 0.75rem auto;">
                    <svg width="120" height="120" viewBox="0 0 100 100">
                        <circle cx="50" cy="50" r="40" stroke="#10b981" stroke-width="10" fill="transparent"
                                stroke-dasharray="251.3" stroke-dashoffset="62.8" stroke-linecap="round"
                                transform="rotate(-90 50 50)" />
                        <circle cx="50" cy="50" r="40" stroke="#f59e0b" stroke-width="10" fill="transparent"
                                stroke-dasharray="251.3" stroke-dashoffset="188.4" stroke-linecap="round"
                                transform="rotate(180 50 50)" />
                        <text x="50" y="56" font-size="18" font-weight="900" text-anchor="middle" fill="#0f172a">6 / 2</text>
                    </svg>
                </div>
                <div style="font-size: 0.75rem; font-weight: 700; color: #b45309;">6 Approved • 2 In Review</div>
                <div style="font-size: 0.68rem; color: #64748b;">0 Rejected applications</div>
            </div>
        </div>
    </div>
    """)

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    # -----------------------------------------------------------------------
    # Section 3: Application Records & Verification Dossier (Matches Image 3)
    # -----------------------------------------------------------------------
    dos_h1, dos_h2 = st.columns([3.5, 2.5], vertical_alignment="center")
    with dos_h1:
        render_html(f"""
        <h2 style="font-size: 1.45rem; font-weight: 900; color: #0f172a; margin: 0 0 0.2rem 0;">
            {_tr('dossierTitle')}
        </h2>
        <p style="font-size: 0.8rem; color: #64748b; margin: 0;">
            {_tr('dossierSub')}
        </p>
        """)
    with dos_h2:
        search_dossier = st.text_input(
            "Filter ledger",
            placeholder="🔍 Filter by scheme, ack, category...",
            key="inp_dossier_search",
            label_visibility="collapsed"
        )

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    # Filter Pills
    filter_choice = st.radio(
        "Dossier Filter",
        ["All Schemes (8)", "🏛️ Central Gov (4)", "📍 State Gov (4)", "✓ Approved Only (6)", "⏳ In Review (2)"],
        horizontal=True,
        label_visibility="collapsed",
        key="dossier_filter_choice"
    )

    filtered_apps = list(apps)
    if filter_choice == "🏛️ Central Gov (4)":
        filtered_apps = [a for a in filtered_apps if "central" in a.get("government_level", "").lower()]
    elif filter_choice == "📍 State Gov (4)":
        filtered_apps = [a for a in filtered_apps if "state" in a.get("government_level", "").lower()]
    elif filter_choice == "✓ Approved Only (6)":
        filtered_apps = [a for a in filtered_apps if a.get("status") == "Approved"]
    elif filter_choice == "⏳ In Review (2)":
        filtered_apps = [a for a in filtered_apps if a.get("status") != "Approved"]

    if search_dossier and search_dossier.strip():
        q = search_dossier.strip().lower()
        filtered_apps = [
            a for a in filtered_apps
            if q in a.get("scheme_name", "").lower()
            or q in a.get("ack_no", "").lower()
            or q in a.get("category", "").lower()
            or q in a.get("government_level", "").lower()
        ]

    st.markdown("<div style='height: 0.65rem;'></div>", unsafe_allow_html=True)

    # 8 Application Ledger Cards (Matches Image 3)
    for app in filtered_apps:
        is_approved = app.get("status") == "Approved"
        status_bg = "#ecfdf5" if is_approved else "#fffbeb"
        status_color = "#047857" if is_approved else "#b45309"
        status_border = "#a7f3d0" if is_approved else "#fde68a"
        status_icon = "✓ Approved" if is_approved else "⏳ In Verification"

        gov_level = app.get("government_level", "").upper()
        applied_date = app.get("applied_date", "")
        category = app.get("category", "")
        scheme_title = app.get("scheme_name", "")
        ack_no = app.get("ack_no", "")
        benefit = app.get("benefit", "")
        approval_date = app.get("approval_date", "")
        portal_url = app.get("portal_url", "https://www.myscheme.gov.in")

        render_html(f"""
        <div style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 1.25rem; padding: 1.2rem 1.6rem; margin-bottom: 0.85rem; box-shadow: 0 1px 2px rgba(0,0,0,0.02); display: flex; justify-content: space-between; align-items: center;">
            <div style="flex: 1;">
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.35rem; font-size: 0.72rem; color: #64748b; font-weight: 700;">
                    <span style="background-color: #eff6ff; color: #1d4ed8; padding: 0.15rem 0.55rem; border-radius: 9999px; font-weight: 800; font-size: 0.68rem;">{gov_level}</span>
                    <span>•</span>
                    <span>Applied: {applied_date}</span>
                    <span>•</span>
                    <span>Category: {category}</span>
                </div>
                <h3 style="font-size: 1.15rem; font-weight: 900; color: #0f172a; margin: 0 0 0.35rem 0;">
                    {scheme_title}
                </h3>
                <div style="font-size: 0.82rem; color: #475569; font-weight: 600;">
                    <span style="font-family: monospace; font-weight: 700; color: #0f172a;">Ack No: {ack_no}</span>
                    <span style="margin: 0 0.35rem;">•</span>
                    <span>Benefit: <strong style="color: #047857;">{benefit}</strong></span>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 1rem; margin-left: 1.5rem;">
                <div style="text-align: right;">
                    <div style="display: inline-flex; align-items: center; gap: 0.35rem; background-color: {status_bg}; color: {status_color}; border: 1px solid {status_border}; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 800; margin-bottom: 0.25rem;">
                        {status_icon}
                    </div>
                    <div style="font-size: 0.7rem; color: #64748b; font-weight: 600;">
                        {approval_date}
                    </div>
                </div>
                <a href="{portal_url}" target="_blank" style="display: flex; align-items: center; justify-content: center; width: 36px; height: 36px; border-radius: 0.75rem; border: 1px solid #e2e8f0; background-color: #f8fafc; color: #475569 !important; text-decoration: none; font-size: 1rem; transition: all 0.2s ease;">
                    ↗
                </a>
            </div>
        </div>
        """)
