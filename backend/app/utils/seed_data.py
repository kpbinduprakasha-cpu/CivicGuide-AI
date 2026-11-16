import os
from sqlalchemy import inspect, text
from ..models import db, User, Scheme, PublicService, Document
from ..rag.rag_engine import rag_engine
from .all_india_schemes_data import ALL_INDIA_SCHEMES

def seed_database(app):
    with app.app_context():
        # Ensure database tables exist
        db.create_all()

        # 1. Seed Initial Admin and Demo User if none exists
        admin_user = User.query.filter((User.user_id == 'admin') | (User.email == 'admin@civicguide.gov.in')).first()
        if not admin_user:
            admin_user = User(
                user_id='admin',
                full_name='National & State Administrator - CivicGuide AI',
                email='admin@civicguide.gov.in',
                age=35,
                mobile_number='9876543210',
                state='Delhi',
                sex='Prefer not to say',
                role='admin',
                is_verified=True
            )
            admin_user.set_languages_list(['English', 'Hindi'])
            admin_user.set_password('Admin@CivicGuide2026')
            db.session.add(admin_user)
            print("[Seed] Created default Administrator account: User ID 'admin' / Admin@CivicGuide2026")
        else:
            admin_user.full_name = 'National & State Administrator - CivicGuide AI'
            admin_user.is_verified = True

        citizen_user = User.query.filter((User.user_id == 'citizen') | (User.email == 'citizen@civicguide.gov.in')).first()
        if not citizen_user:
            citizen_user = User(
                user_id='citizen',
                full_name='Rahul Kumar',
                email='citizen@civicguide.gov.in',
                age=28,
                mobile_number='9876543211',
                state='Karnataka',
                sex='Male',
                role='user',
                is_verified=True
            )
            citizen_user.set_languages_list(['English', 'Kannada', 'Hindi'])
            citizen_user.set_password('Citizen@2026')
            db.session.add(citizen_user)
            print("[Seed] Created default Citizen demo account: User ID 'citizen' / Citizen@2026")
        else:
            citizen_user.is_verified = True

        # 2. Ensure 'state' column exists on schemes table & Seed All-India Schemes
        try:
            inspector = inspect(db.engine)
            if 'schemes' in inspector.get_table_names():
                columns = [c['name'] for c in inspector.get_columns('schemes')]
                if 'state' not in columns:
                    with db.engine.connect() as conn:
                        conn.execute(text("ALTER TABLE schemes ADD COLUMN state VARCHAR(100) DEFAULT 'All India'"))
                        conn.commit()
                    print("[Seed] Successfully migrated schemes table: added 'state' column.")
        except Exception as e:
            print(f"[Seed] Scheme state column check/migration warning: {e}")

        # Seed or Update All-India Central and State Government Schemes
        added_count = 0
        updated_count = 0
        for s_data in ALL_INDIA_SCHEMES:
            existing = Scheme.query.filter_by(name=s_data['name']).first()
            if not existing:
                scheme_obj = Scheme(**s_data)
                db.session.add(scheme_obj)
                added_count += 1
            else:
                if 'state' in s_data:
                    existing.state = s_data['state']
                if 'government_level' in s_data:
                    existing.government_level = s_data['government_level']
                updated_count += 1
        db.session.commit()
        if added_count > 0 or updated_count > 0:
            print(f"[Seed] All-India Schemes synced: {added_count} added, {updated_count} verified/updated (Total: {Scheme.query.count()}).")

        # 3. Seed Verified Public Services Across All India (Central Government & Major States/Taluks)
        if PublicService.query.count() == 0:
            services_data = [
                # --- CENTRAL GOVERNMENT MINISTRIES & OFFICES (NEW DELHI) ---
                {
                    "name": "Central Secretariat & North Block (Ministry of Home Affairs & Finance)",
                    "name_kn": "ಕೇಂದ್ರ ಸಚಿವಾಲಯ ಹಾಗೂ ನಾರ್ತ್ ಬ್ಲಾಕ್ (ಗೃಹ ಹಾಗೂ ಹಣಕಾಸು ಸಚಿವಾಲಯ)",
                    "name_hi": "केंद्रीय सचिवालय एवं नॉर्थ ब्लॉक (गृह एवं वित्त मंत्रालय)",
                    "category": "Central Ministries & Offices",
                    "state": "Delhi",
                    "district_city": "New Delhi",
                    "taluk": "Central Delhi",
                    "government_level": "Central Government",
                    "address": "North Block, Central Secretariat, New Delhi - 110001",
                    "latitude": 28.6143,
                    "longitude": 77.2014,
                    "phone": "011-23092011",
                    "official_url": "https://mha.gov.in",
                    "verified": True
                },
                {
                    "name": "Shastri Bhawan (Ministry of Education & Social Justice)",
                    "name_kn": "ಶಾಸ್ತ್ರಿ ಭವನ (ಶಿಕ್ಷಣ ಮತ್ತು ಸಮಾಜ ಕಲ್ಯಾಣ ಸಚಿವಾಲಯ)",
                    "name_hi": "शास्त्री भवन (शिक्षा एवं सामाजिक न्याय मंत्रालय)",
                    "category": "Central Ministries & Offices",
                    "state": "Delhi",
                    "district_city": "New Delhi",
                    "taluk": "Central Delhi",
                    "government_level": "Central Government",
                    "address": "Dr. Rajendra Prasad Road, New Delhi - 110001",
                    "latitude": 28.6186,
                    "longitude": 77.2155,
                    "phone": "011-23386451",
                    "official_url": "https://education.gov.in",
                    "verified": True
                },
                {
                    "name": "NITI Aayog (National Institution for Transforming India)",
                    "name_kn": "ನೀತಿ ಆಯೋಗ ಮುಖ್ಯ ಕಚೇರಿ, ನವದೆಹಲಿ",
                    "name_hi": "नीति आयोग (राष्ट्रीय भारत परिवर्तन संस्थान), नई दिल्ली",
                    "category": "Central Ministries & Offices",
                    "state": "Delhi",
                    "district_city": "New Delhi",
                    "taluk": "Central Delhi",
                    "government_level": "Central Government",
                    "address": "Sansad Marg, Sansad Marg Area, New Delhi - 110001",
                    "latitude": 28.6235,
                    "longitude": 77.2120,
                    "phone": "011-23096620",
                    "official_url": "https://niti.gov.in",
                    "verified": True
                },
                {
                    "name": "UIDAI National Headquarters (Aadhaar Head Office)",
                    "name_kn": "ಯುಐಡಿಎಐ ರಾಷ್ಟ್ರೀಯ ಪ್ರಧಾನ ಕಚೇರಿ (ಆಧಾರ್ ಕೇಂದ್ರ ಕಚೇರಿ)",
                    "name_hi": "यूआईडीएआई मुख्यालय (आधार मुख्य कार्यालय), नई दिल्ली",
                    "category": "Passport & Aadhaar Seva Kendras",
                    "state": "Delhi",
                    "district_city": "New Delhi",
                    "taluk": "Central Delhi",
                    "government_level": "Central Government",
                    "address": "Bangla Sahib Road, Gole Market, New Delhi - 110001",
                    "latitude": 28.6270,
                    "longitude": 77.2080,
                    "phone": "1947",
                    "official_url": "https://uidai.gov.in",
                    "verified": True
                },

                # --- AIIMS & APEX CENTRAL/STATE HOSPITALS ---
                {
                    "name": "All India Institute of Medical Sciences (AIIMS) New Delhi",
                    "name_kn": "ಅಖಿಲ ಭಾರತ ವೈದ್ಯಕೀಯ ವಿಜ್ಞಾನ ಸಂಸ್ಥೆ (ಏಮ್ಸ್), ನವದೆಹಲಿ",
                    "name_hi": "अखिल भारतीय आयुर्विज्ञान संस्थान (एम्स), नई दिल्ली",
                    "category": "AIIMS & Central/State Hospitals",
                    "state": "Delhi",
                    "district_city": "New Delhi",
                    "taluk": "South Delhi",
                    "government_level": "Central Government",
                    "address": "Sri Aurobindo Marg, Ansari Nagar, New Delhi - 110029",
                    "latitude": 28.5672,
                    "longitude": 77.2100,
                    "phone": "011-26588500",
                    "official_url": "https://www.aiims.edu",
                    "verified": True
                },
                {
                    "name": "All India Institute of Medical Sciences (AIIMS) Rishikesh",
                    "name_kn": "ಅಖಿಲ ಭಾರತ ವೈದ್ಯಕೀಯ ವಿಜ್ಞಾನ ಸಂಸ್ಥೆ (ಏಮ್ಸ್), ಋಷಿಕೇಶ",
                    "name_hi": "अखिल भारतीय आयुर्विज्ञान संस्थान (एम्स), ऋषिकेश",
                    "category": "AIIMS & Central/State Hospitals",
                    "state": "Uttarakhand",
                    "district_city": "Dehradun",
                    "taluk": "Rishikesh",
                    "government_level": "Central Government",
                    "address": "Virbhadra Road, Rishikesh, Uttarakhand - 249203",
                    "latitude": 30.0760,
                    "longitude": 78.2880,
                    "phone": "0135-2462929",
                    "official_url": "https://aiimsrishikesh.edu.in",
                    "verified": True
                },
                {
                    "name": "All India Institute of Medical Sciences (AIIMS) Bhopal",
                    "name_kn": "ಅಖಿಲ ಭಾರತ ವೈದ್ಯಕೀಯ ವಿಜ್ಞಾನ ಸಂಸ್ಥೆ (ಏಮ್ಸ್), ಭೋಪಾಲ್",
                    "name_hi": "अखिल भारतीय आयुर्विज्ञान संस्थान (एम्स), भोपाल",
                    "category": "AIIMS & Central/State Hospitals",
                    "state": "Madhya Pradesh",
                    "district_city": "Bhopal",
                    "taluk": "Huzur",
                    "government_level": "Central Government",
                    "address": "Saket Nagar, AIIMS Campus, Bhopal, Madhya Pradesh - 462020",
                    "latitude": 23.2065,
                    "longitude": 77.4600,
                    "phone": "0755-2672317",
                    "official_url": "https://aiimsbhopal.edu.in",
                    "verified": True
                },
                {
                    "name": "Postgraduate Institute of Medical Education and Research (PGIMER) Chandigarh",
                    "name_kn": "ಪಿಜಿಐಎಂಇಆರ್, ಚಂಡೀಗಢ",
                    "name_hi": "स्नातकोत्तर चिकित्सा शिक्षा एवं अनुसंधान संस्थान (पीजीआईएमईआर), चंडीगढ़",
                    "category": "AIIMS & Central/State Hospitals",
                    "state": "Chandigarh",
                    "district_city": "Chandigarh",
                    "taluk": "Sector 12",
                    "government_level": "Central Government",
                    "address": "Sector 12, Chandigarh - 160012",
                    "latitude": 30.7634,
                    "longitude": 76.7766,
                    "phone": "0172-2746018",
                    "official_url": "https://pgimer.edu.in",
                    "verified": True
                },
                {
                    "name": "NIMHANS (National Institute of Mental Health & Neurosciences) Bengaluru",
                    "name_kn": "ನಿಮ್ಹಾನ್ಸ್ ರಾಷ್ಟ್ರೀಯ ವೈದ್ಯಕೀಯ ಸಂಸ್ಥೆ, ಬೆಂಗಳೂರು",
                    "name_hi": "राष्ट्रीय मानसिक स्वास्थ्य एवं तंत्रिका विज्ञान संस्थान (निमहंस), बेंगलुरु",
                    "category": "AIIMS & Central/State Hospitals",
                    "state": "Karnataka",
                    "district_city": "Bengaluru",
                    "taluk": "Bengaluru South",
                    "government_level": "Central Government",
                    "address": "Hosur Road, Lakkasandra, Bengaluru, Karnataka - 560029",
                    "latitude": 12.9392,
                    "longitude": 77.5956,
                    "phone": "080-26995000",
                    "official_url": "https://nimhans.ac.in",
                    "verified": True
                },
                {
                    "name": "Victoria Hospital (BMCRI Apex State Hospital) Bengaluru",
                    "name_kn": "ವಿಕ್ಟೋರಿಯಾ ಸಾರ್ವಜನಿಕ ಆಸ್ಪತ್ರೆ, ಬೆಂಗಳೂರು",
                    "name_hi": "विक्टोरिया अस्पताल (बीएमसीआरआई), बेंगलुरु",
                    "category": "AIIMS & Central/State Hospitals",
                    "state": "Karnataka",
                    "district_city": "Bengaluru",
                    "taluk": "Bengaluru Urban",
                    "government_level": "State Government",
                    "address": "Fort, Near City Market, Kalasipalya, Bengaluru, Karnataka - 560002",
                    "latitude": 12.9634,
                    "longitude": 77.5752,
                    "phone": "080-26701150",
                    "official_url": "https://bmcri.edu.in",
                    "verified": True
                },
                {
                    "name": "King Edward Memorial (KEM) Hospital Mumbai",
                    "name_kn": "ಕೆಇಎಂ ಆಸ್ಪತ್ರೆ, ಮುಂಬೈ",
                    "name_hi": "किंग एडवर्ड मेमोरियल (केईएम) अस्पताल, मुंबई",
                    "category": "AIIMS & Central/State Hospitals",
                    "state": "Maharashtra",
                    "district_city": "Mumbai",
                    "taluk": "Parel",
                    "government_level": "State Government",
                    "address": "Acharya Donde Marg, Parel, Mumbai, Maharashtra - 400012",
                    "latitude": 19.0026,
                    "longitude": 72.8422,
                    "phone": "022-24107000",
                    "official_url": "https://kem.edu",
                    "verified": True
                },
                {
                    "name": "SSKM Hospital & IPGMER Kolkata",
                    "name_kn": "ಎಸ್ ಎಸ್ ಕೆ ಎಂ ಆಸ್ಪತ್ರೆ, ಕೋಲ್ಕತ್ತಾ",
                    "name_hi": "एसएसकेएम अस्पताल एवं आईजीआईएमईआर, कोलकाता",
                    "category": "AIIMS & Central/State Hospitals",
                    "state": "West Bengal",
                    "district_city": "Kolkata",
                    "taluk": "Bhowanipore",
                    "government_level": "State Government",
                    "address": "244 AJC Bose Road, Bhowanipore, Kolkata, West Bengal - 700020",
                    "latitude": 22.5385,
                    "longitude": 88.3440,
                    "phone": "033-22231589",
                    "official_url": "https://ipgmer.gov.in",
                    "verified": True
                },

                # --- PASSPORT & AADHAAR SEVA KENDRAS (CENTRAL GOVERNMENT) ---
                {
                    "name": "Regional Passport Office (RPO) & PSK ITO New Delhi",
                    "name_kn": "ಪ್ರಾದೇಶಿಕ ಪಾಸ್‌ಪೋರ್ಟ್ ಕಚೇರಿ (ಆರ್‌ಪಿಒ), ನವದೆಹಲಿ",
                    "name_hi": "क्षेत्रीय पासपोर्ट कार्यालय एवं पीएसके आईटीओ, नई दिल्ली",
                    "category": "Passport & Aadhaar Seva Kendras",
                    "state": "Delhi",
                    "district_city": "New Delhi",
                    "taluk": "Central Delhi",
                    "government_level": "Central Government",
                    "address": "Herald House, Bahadur Shah Zafar Marg, ITO, New Delhi - 110002",
                    "latitude": 28.6328,
                    "longitude": 77.2410,
                    "phone": "011-23238210",
                    "official_url": "https://passportindia.gov.in",
                    "verified": True
                },
                {
                    "name": "Passport Seva Kendra (PSK) Lalbagh Bengaluru",
                    "name_kn": "ಪಾಸ್‌ಪೋರ್ಟ್ ಸೇವಾ ಕೇಂದ್ರ (ಪಿಎಸ್‌ಕೆ) ಲಾಲ್‌ಬಾಗ್, ಬೆಂಗಳೂರು",
                    "name_hi": "पासपोर्ट सेवा केंद्र (पीएसके) लालबाग, बेंगलुरु",
                    "category": "Passport & Aadhaar Seva Kendras",
                    "state": "Karnataka",
                    "district_city": "Bengaluru",
                    "taluk": "Bengaluru South",
                    "government_level": "Central Government",
                    "address": "No. 45, Prestige Libra, Lalbagh Road, Bengaluru, Karnataka - 560027",
                    "latitude": 12.9510,
                    "longitude": 77.5870,
                    "phone": "1800-258-1800",
                    "official_url": "https://passportindia.gov.in",
                    "verified": True
                },
                {
                    "name": "Aadhaar Seva Kendra (UIDAI) Andheri East Mumbai",
                    "name_kn": "ಆಧಾರ್ ಸೇವಾ ಕೇಂದ್ರ (ಯುಐಡಿಎಐ), ಅಂಧೇರಿ ಈಸ್ಟ್, ಮುಂಬೈ",
                    "name_hi": "आधार सेवा केंद्र (यूआईडीएआई) अंधेरी पूर्व, मुंबई",
                    "category": "Passport & Aadhaar Seva Kendras",
                    "state": "Maharashtra",
                    "district_city": "Mumbai",
                    "taluk": "Andheri",
                    "government_level": "Central Government",
                    "address": "Lotus Trade Centre, Opposite Star TV, Andheri East, Mumbai - 400053",
                    "latitude": 19.1136,
                    "longitude": 72.8697,
                    "phone": "1947",
                    "official_url": "https://uidai.gov.in",
                    "verified": True
                },
                {
                    "name": "Passport Seva Kendra (PSK) Begumpet Hyderabad",
                    "name_kn": "ಪಾಸ್‌ಪೋರ್ಟ್ ಸೇವಾ ಕೇಂದ್ರ, ಬೇಗಂಪೇಟೆ, ಹೈದರಾಬಾದ್",
                    "name_hi": "पासपोर्ट सेवा केंद्र (पीएसके) बेगमपेट, हैदराबाद",
                    "category": "Passport & Aadhaar Seva Kendras",
                    "state": "Telangana",
                    "district_city": "Hyderabad",
                    "taluk": "Begumpet",
                    "government_level": "Central Government",
                    "address": "Kumarguda, Beside White House Building, Begumpet, Hyderabad - 500016",
                    "latitude": 17.4410,
                    "longitude": 78.4720,
                    "phone": "1800-258-1800",
                    "official_url": "https://passportindia.gov.in",
                    "verified": True
                },
                {
                    "name": "Regional Passport Office (RPO) Anandapur Kolkata",
                    "name_kn": "ಪ್ರಾದೇಶಿಕ ಪಾಸ್‌ಪೋರ್ಟ್ ಕಚೇರಿ (ಆರ್‌ಪಿಒ), ಆನಂದಪುರ, ಕೋಲ್ಕತ್ತಾ",
                    "name_hi": "क्षेत्रीय पासपोर्ट कार्यालय (आरपीओ) आनंदपुर, कोलकाता",
                    "category": "Passport & Aadhaar Seva Kendras",
                    "state": "West Bengal",
                    "district_city": "Kolkata",
                    "taluk": "Anandapur",
                    "government_level": "Central Government",
                    "address": "Plot No. 787, Anandapur, EM Bypass, Kolkata, West Bengal - 700107",
                    "latitude": 22.5120,
                    "longitude": 88.4010,
                    "phone": "033-24434222",
                    "official_url": "https://passportindia.gov.in",
                    "verified": True
                },
                {
                    "name": "Passport Seva Kendra (PSK) Aminjikarai Chennai",
                    "name_kn": "ಪಾಸ್‌ಪೋರ್ಟ್ ಸೇವಾ ಕೇಂದ್ರ, ಅಮಿಂಜಿಕರೈ, ಚೆನ್ನೈ",
                    "name_hi": "पासपोर्ट सेवा केंद्र (पीएसके) अमीनजीकरई, चेन्नई",
                    "category": "Passport & Aadhaar Seva Kendras",
                    "state": "Tamil Nadu",
                    "district_city": "Chennai",
                    "taluk": "Aminjikarai",
                    "government_level": "Central Government",
                    "address": "Navins Presidium, 103 Nelson Manickam Road, Aminjikarai, Chennai - 600029",
                    "latitude": 13.0720,
                    "longitude": 80.2220,
                    "phone": "1800-258-1800",
                    "official_url": "https://passportindia.gov.in",
                    "verified": True
                },

                # --- CENTRAL & STATE UNIVERSITIES & PREMIER INSTITUTES ---
                {
                    "name": "Indian Institute of Technology (IIT) Delhi",
                    "name_kn": "ಭಾರತೀಯ ತಂತ್ರಜ್ಞಾನ ಸಂಸ್ಥೆ (ಐಐಟಿ) ದೆಹಲಿ",
                    "name_hi": "भारतीय प्रौद्योगिकी संस्थान (आईआईटी) दिल्ली",
                    "category": "Central/State Universities & IITs",
                    "state": "Delhi",
                    "district_city": "New Delhi",
                    "taluk": "Hauz Khas",
                    "government_level": "Central Government",
                    "address": "Hauz Khas, New Delhi - 110016",
                    "latitude": 28.5450,
                    "longitude": 77.1926,
                    "phone": "011-26597135",
                    "official_url": "https://home.iitd.ac.in",
                    "verified": True
                },
                {
                    "name": "Indian Institute of Technology (IIT) Bombay",
                    "name_kn": "ಭಾರತೀಯ ತಂತ್ರಜ್ಞಾನ ಸಂಸ್ಥೆ (ಐಐಟಿ) ಬಾಂಬೆ",
                    "name_hi": "भारतीय प्रौद्योगिकी संस्थान (आईआईटी) बॉम्बे",
                    "category": "Central/State Universities & IITs",
                    "state": "Maharashtra",
                    "district_city": "Mumbai",
                    "taluk": "Powai",
                    "government_level": "Central Government",
                    "address": "Main Gate Rd, IIT Area, Powai, Mumbai, Maharashtra - 400076",
                    "latitude": 19.1334,
                    "longitude": 72.9133,
                    "phone": "022-25722545",
                    "official_url": "https://www.iitb.ac.in",
                    "verified": True
                },
                {
                    "name": "Indian Institute of Science (IISc) Bengaluru",
                    "name_kn": "ಭಾರತೀಯ ವಿಜ್ಞಾನ ಸಂಸ್ಥೆ (ಐಐಎಸ್ಸಿ), ಬೆಂಗಳೂರು",
                    "name_hi": "भारतीय विज्ञान संस्थान (आईआईएससी), बेंगलुरु",
                    "category": "Central/State Universities & IITs",
                    "state": "Karnataka",
                    "district_city": "Bengaluru",
                    "taluk": "Malleshwaram",
                    "government_level": "Central Government",
                    "address": "CV Raman Rd, Bengaluru, Karnataka - 560012",
                    "latitude": 13.0219,
                    "longitude": 77.5671,
                    "phone": "080-22932001",
                    "official_url": "https://iisc.ac.in",
                    "verified": True
                },
                {
                    "name": "Indian Institute of Technology (IIT) Madras",
                    "name_kn": "ಭಾರತೀಯ ತಂತ್ರಜ್ಞಾನ ಸಂಸ್ಥೆ (ಐಐಟಿ) ಮದ್ರಾಸ್",
                    "name_hi": "भारतीय प्रौद्योगिकी संस्थान (आईआईटी) मद्रास",
                    "category": "Central/State Universities & IITs",
                    "state": "Tamil Nadu",
                    "district_city": "Chennai",
                    "taluk": "Guindy",
                    "government_level": "Central Government",
                    "address": "Sardar Patel Road, Chennai, Tamil Nadu - 600036",
                    "latitude": 12.9915,
                    "longitude": 80.2337,
                    "phone": "044-22578100",
                    "official_url": "https://www.iitm.ac.in",
                    "verified": True
                },
                {
                    "name": "Banaras Hindu University (BHU) Central University",
                    "name_kn": "ಬನಾರಸ್ ಹಿಂದೂ ವಿಶ್ವವಿದ್ಯಾಲಯ (ಬಿಎಚ್‌ಯು), ವಾರಣಾಸಿ",
                    "name_hi": "काशी हिन्दू विश्वविद्यालय (बीएचयू), वाराणसी",
                    "category": "Central/State Universities & IITs",
                    "state": "Uttar Pradesh",
                    "district_city": "Varanasi",
                    "taluk": "Varanasi Sadar",
                    "government_level": "Central Government",
                    "address": "Ajagara, Banaras Hindu University, Varanasi, Uttar Pradesh - 221005",
                    "latitude": 25.2677,
                    "longitude": 82.9913,
                    "phone": "0542-2368558",
                    "official_url": "https://bhu.ac.in",
                    "verified": True
                },

                # --- STATE GOVT SECRETARIATS & DISTRICT COLLECTORATES ---
                {
                    "name": "Vidhana Soudha (Karnataka State Government Secretariat)",
                    "name_kn": "ವಿಧಾನ ಸೌಧ (ಕರ್ನಾಟಕ ಸರ್ಕಾರ ಸಚಿವಾಲಯ), ಬೆಂಗಳೂರು",
                    "name_hi": "विधान सौध (कर्नाटक राज्य सचिवालय), बेंगलुरु",
                    "category": "State Secretariat & Collectorates",
                    "state": "Karnataka",
                    "district_city": "Bengaluru",
                    "taluk": "Bengaluru Urban",
                    "government_level": "State Government",
                    "address": "Ambedkar Beedhi, Sampangi Rama Nagara, Bengaluru, Karnataka - 560001",
                    "latitude": 12.9796,
                    "longitude": 77.5907,
                    "phone": "080-22252441",
                    "official_url": "https://karnataka.gov.in",
                    "verified": True
                },
                {
                    "name": "Mantralaya (Maharashtra State Government Secretariat)",
                    "name_kn": "ಮಂತ್ರಿಲಯ (ಮಹಾರಾಷ್ಟ್ರ ರಾಜ್ಯ ಸರ್ಕಾರ ಸಚಿವಾಲಯ), ಮುಂಬೈ",
                    "name_hi": "मंत्रालय (महाराष्ट्र राज्य सचिवालय), मुंबई",
                    "category": "State Secretariat & Collectorates",
                    "state": "Maharashtra",
                    "district_city": "Mumbai",
                    "taluk": "Nariman Point",
                    "government_level": "State Government",
                    "address": "Madam Cama Road, Nariman Point, Mumbai, Maharashtra - 400032",
                    "latitude": 18.9270,
                    "longitude": 72.8270,
                    "phone": "022-22025142",
                    "official_url": "https://maharashtra.gov.in",
                    "verified": True
                },
                {
                    "name": "Fort St. George (Tamil Nadu State Secretariat)",
                    "name_kn": "ಫೋರ್ಟ್ ಸೇಂಟ್ ಜಾರ್ಜ್ (ತಮಿಳುನಾಡು ರಾಜ್ಯ ಸಚಿವಾಲಯ), ಚೆನ್ನೈ",
                    "name_hi": "फोर्ट सेंट जॉर्ज (तमिलनाडु राज्य सचिवालय), चेन्नई",
                    "category": "State Secretariat & Collectorates",
                    "state": "Tamil Nadu",
                    "district_city": "Chennai",
                    "taluk": "George Town",
                    "government_level": "State Government",
                    "address": "Rajaji Salai, Fort St George, Chennai, Tamil Nadu - 600009",
                    "latitude": 13.0800,
                    "longitude": 80.2870,
                    "phone": "044-25671510",
                    "official_url": "https://tn.gov.in",
                    "verified": True
                },
                {
                    "name": "Bapu Bhawan & UP Civil Secretariat Lucknow",
                    "name_kn": "ಉತ್ತರ ಪ್ರದೇಶ ಸಚಿವಾಲಯ (ಬಾಪು ಭವನ), ಲಖನೌ",
                    "name_hi": "बापू भवन एवं उत्तर प्रदेश सिविल सचिवालय, लखनऊ",
                    "category": "State Secretariat & Collectorates",
                    "state": "Uttar Pradesh",
                    "district_city": "Lucknow",
                    "taluk": "Hazratganj",
                    "government_level": "State Government",
                    "address": "Vidhan Sabha Marg, Hazratganj, Lucknow, Uttar Pradesh - 226001",
                    "latitude": 26.8467,
                    "longitude": 80.9462,
                    "phone": "0522-2238001",
                    "official_url": "https://up.gov.in",
                    "verified": True
                },
                {
                    "name": "Nabanna (West Bengal State Secretariat)",
                    "name_kn": "ನಬನ್ನಾ (ಪಶ್ಚಿಮ ಬಂಗಾಳ ರಾಜ್ಯ ಸಚಿವಾಲಯ), ಕೋಲ್ಕತ್ತಾ/ಹೌರಾ",
                    "name_hi": "नबन्ना (पश्चिम बंगाल राज्य सचिवालय), हावड़ा/कोलकाता",
                    "category": "State Secretariat & Collectorates",
                    "state": "West Bengal",
                    "district_city": "Kolkata",
                    "taluk": "Howrah",
                    "government_level": "State Government",
                    "address": "325 Sarat Chatterjee Road, Shibpur, Howrah, West Bengal - 711102",
                    "latitude": 22.5620,
                    "longitude": 88.3180,
                    "phone": "033-22145555",
                    "official_url": "https://wb.gov.in",
                    "verified": True
                },
                {
                    "name": "District Collectorate & DM Office Jaipur",
                    "name_kn": "ಜಿಲ್ಲಾಧಿಕಾರಿಗಳ ಕಚೇರಿ (ಕಲೆಕ್ಟರೇಟ್), ಜೈಪುರ",
                    "name_hi": "जिला कलेक्ट्रेट एवं डीएम कार्यालय, जयपुर",
                    "category": "State Secretariat & Collectorates",
                    "state": "Rajasthan",
                    "district_city": "Jaipur",
                    "taluk": "Jaipur City",
                    "government_level": "State Government",
                    "address": "Collectorate Circle, Bani Park, Jaipur, Rajasthan - 302016",
                    "latitude": 26.9220,
                    "longitude": 75.7980,
                    "phone": "0141-2201101",
                    "official_url": "https://jaipur.rajasthan.gov.in",
                    "verified": True
                },
                {
                    "name": "District Collectorate & DM Office Patna",
                    "name_kn": "ಜಿಲ್ಲಾಧಿಕಾರಿಗಳ ಕಚೇರಿ (ಕಲೆಕ್ಟರೇಟ್), ಪಾಟ್ನಾ",
                    "name_hi": "जिला कलेक्ट्रेट एवं डीएम कार्यालय, पटना",
                    "category": "State Secretariat & Collectorates",
                    "state": "Bihar",
                    "district_city": "Patna",
                    "taluk": "Patna Sadar",
                    "government_level": "State Government",
                    "address": "Ashok Rajpath, Near Gandhi Maidan, Patna, Bihar - 800001",
                    "latitude": 25.6180,
                    "longitude": 85.1410,
                    "phone": "0612-2219545",
                    "official_url": "https://patna.nic.in",
                    "verified": True
                },

                # --- COMMON SERVICE CENTRES (CSC / DIGITAL SEVA) ---
                {
                    "name": "Common Service Centre (CSC) Connaught Place New Delhi",
                    "name_kn": "ಸಾಮಾನ್ಯ ಸೇವಾ ಕೇಂದ್ರ (ಸಿಎಸ್‌ಸಿ), ಕನ್ನಾಟ್ ಪ್ಲೇಸ್, ನವದೆಹಲಿ",
                    "name_hi": "कॉमन सर्विस सेंटर (सीएससी), कनॉट प्लेस, नई दिल्ली",
                    "category": "Common Service Centres (CSC)",
                    "state": "Delhi",
                    "district_city": "New Delhi",
                    "taluk": "Connaught Place",
                    "government_level": "Central Government",
                    "address": "Inner Circle, Block F, Connaught Place, New Delhi - 110001",
                    "latitude": 28.6315,
                    "longitude": 77.2167,
                    "phone": "1800-3000-3468",
                    "official_url": "https://csc.gov.in",
                    "verified": True
                },
                {
                    "name": "CSC Digital Seva Kendra Jayanagar Bengaluru",
                    "name_kn": "ಸಿಎಸ್‌ಸಿ ಡಿಜಿಟಲ್ ಸೇವಾ ಕೇಂದ್ರ, ಜಯನಗರ, ಬೆಂಗಳೂರು",
                    "name_hi": "सीएससी डिजिटल सेवा केंद्र, जयनगर, बेंगलुरु",
                    "category": "Common Service Centres (CSC)",
                    "state": "Karnataka",
                    "district_city": "Bengaluru",
                    "taluk": "Jayanagar",
                    "government_level": "Central Government",
                    "address": "4th Block, 11th Main Rd, Jayanagar, Bengaluru, Karnataka - 560011",
                    "latitude": 12.9299,
                    "longitude": 77.5824,
                    "phone": "080-26581234",
                    "official_url": "https://csc.gov.in",
                    "verified": True
                },
                {
                    "name": "CSC Citizen Facilitation Centre Dadar Mumbai",
                    "name_kn": "ಸಿಎಸ್‌ಸಿ ನಾಗರಿಕ ಸೇವಾ ಕೇಂದ್ರ, ದಾದರ್, ಮುಂಬೈ",
                    "name_hi": "सीएससी नागरिक सुविधा केंद्र, दादर, मुंबई",
                    "category": "Common Service Centres (CSC)",
                    "state": "Maharashtra",
                    "district_city": "Mumbai",
                    "taluk": "Dadar",
                    "government_level": "Central Government",
                    "address": "Ranade Road, Near Dadar Railway Station, Mumbai, Maharashtra - 400028",
                    "latitude": 19.0178,
                    "longitude": 72.8478,
                    "phone": "022-24305678",
                    "official_url": "https://csc.gov.in",
                    "verified": True
                },

                # --- KARNATAKA / VIJAYANAGARA DISTRICT COMPREHENSIVE TALUKS ---
                # 1. Hosapete Taluk
                {
                    "name": "Vijayanagara District Collectorate & DC Office",
                    "name_kn": "ವಿಜಯನಗರ ಜಿಲ್ಲಾಧಿಕಾರಿಗಳ ಕಚೇರಿ, ಹೊಸಪೇಟೆ",
                    "name_hi": "विजयनगर जिला कलेक्ट्रेट एवं डीसी कार्यालय, होसपेट",
                    "category": "State Secretariat & Collectorates",
                    "state": "Karnataka",
                    "district_city": "Vijayanagara",
                    "taluk": "Hosapete",
                    "government_level": "State Government",
                    "address": "Mini Vidhana Soudha, Station Road, Hosapete, Vijayanagara - 583201",
                    "latitude": 15.2689,
                    "longitude": 76.3909,
                    "phone": "08394-222222",
                    "official_url": "https://vijayanagara.nic.in",
                    "verified": True
                },
                {
                    "name": "District General Hospital Hosapete",
                    "name_kn": "ಜಿಲ್ಲಾ ಸಾರ್ವಜನಿಕ ಆಸ್ಪತ್ರೆ, ಹೊಸಪೇಟೆ",
                    "name_hi": "जिला सामान्य अस्पताल, होसपेट",
                    "category": "AIIMS & Central/State Hospitals",
                    "state": "Karnataka",
                    "district_city": "Vijayanagara",
                    "taluk": "Hosapete",
                    "government_level": "State Government",
                    "address": "TB Dam Road, Hosapete, Vijayanagara - 583201",
                    "latitude": 15.2721,
                    "longitude": 76.3855,
                    "phone": "08394-224100",
                    "official_url": "https://vijayanagara.nic.in",
                    "verified": True
                },
                {
                    "name": "Vijayanagara College (Government Aided)",
                    "name_kn": "ವಿಜಯನಗರ ಕಾಲೇಜು, ಹೊಸಪೇಟೆ",
                    "name_hi": "विजयनगर कॉलेज, होसपेट",
                    "category": "Central/State Universities & IITs",
                    "state": "Karnataka",
                    "district_city": "Vijayanagara",
                    "taluk": "Hosapete",
                    "government_level": "State Government",
                    "address": "College Road, Patel Nagar, Hosapete, Vijayanagara - 583201",
                    "latitude": 15.2655,
                    "longitude": 76.3882,
                    "phone": "08394-228431",
                    "official_url": "https://vijayanagaracollege.org",
                    "verified": True
                },
                {
                    "name": "Grama One & Seva Sindhu Citizen Centre Hosapete",
                    "name_kn": "ಗ್ರಾಮ ಒನ್ ನಾಗರಿಕ ಸೇವಾ ಕೇಂದ್ರ, ಹೊಸಪೇಟೆ",
                    "name_hi": "ग्राम वन नागरिक सेवा केंद्र, होसपेट",
                    "category": "Common Service Centres (CSC)",
                    "state": "Karnataka",
                    "district_city": "Vijayanagara",
                    "taluk": "Hosapete",
                    "government_level": "State Government",
                    "address": "Near KSRTC Main Bus Station, Hosapete, Vijayanagara - 583201",
                    "latitude": 15.2705,
                    "longitude": 76.3934,
                    "phone": "08394-229988",
                    "official_url": "https://sevasindhu.karnataka.gov.in",
                    "verified": True
                },
                {
                    "name": "District Social Welfare Office Vijayanagara",
                    "name_kn": "ಜಿಲ್ಲಾ ಸಮಾಜ ಕಲ್ಯಾಣ ಕಚೇರಿ, ಹೊಸಪೇಟೆ",
                    "name_hi": "जिला समाज कल्याण कार्यालय, होसपेट",
                    "category": "Welfare & Pension Offices",
                    "state": "Karnataka",
                    "district_city": "Vijayanagara",
                    "taluk": "Hosapete",
                    "government_level": "State Government",
                    "address": "Mini Vidhana Soudha Complex, Hosapete, Vijayanagara - 583201",
                    "latitude": 15.2695,
                    "longitude": 76.3915,
                    "phone": "08394-221050",
                    "official_url": "https://sw.karnataka.gov.in",
                    "verified": True
                },

                # 2. Harapanahalli Taluk
                {
                    "name": "Taluk General Hospital Harapanahalli (100 Bed Hospital)",
                    "name_kn": "ತಾಲೂಕು ಸಾರ್ವಜನಿಕ ಆಸ್ಪತ್ರೆ, ಹರಪನಹಳ್ಳಿ",
                    "name_hi": "तालुक सामान्य अस्पताल, हरपनहल्ली",
                    "category": "AIIMS & Central/State Hospitals",
                    "state": "Karnataka",
                    "district_city": "Vijayanagara",
                    "taluk": "Harapanahalli",
                    "government_level": "State Government",
                    "address": "Hospital Road, Near Court Circle, Harapanahalli, Vijayanagara - 583131",
                    "latitude": 14.7958,
                    "longitude": 75.9867,
                    "phone": "08398-251234",
                    "official_url": "https://vijayanagara.nic.in",
                    "verified": True
                },
                {
                    "name": "Tahsildar & Taluk Office Harapanahalli",
                    "name_kn": "ತಹಶೀಲ್ದಾರ್ ಕಚೇರಿ, ಹರಪನಹಳ್ಳಿ",
                    "name_hi": "तहसीलदार कार्यालय, हरपनहल्ली",
                    "category": "State Secretariat & Collectorates",
                    "state": "Karnataka",
                    "district_city": "Vijayanagara",
                    "taluk": "Harapanahalli",
                    "government_level": "State Government",
                    "address": "Mini Vidhana Soudha, Main Road, Harapanahalli, Vijayanagara - 583131",
                    "latitude": 14.7932,
                    "longitude": 75.9841,
                    "phone": "08398-251222",
                    "official_url": "https://nadakacheri.karnataka.gov.in",
                    "verified": True
                },
                {
                    "name": "Government First Grade College Harapanahalli",
                    "name_kn": "ಸರ್ಕಾರಿ ಪ್ರಥಮ ದರ್ಜೆ ಕಾಲೇಜು, ಹರಪನಹಳ್ಳಿ",
                    "name_hi": "राजकीय प्रथम श्रेणी कॉलेज, हरपनहल्ली",
                    "category": "Central/State Universities & IITs",
                    "state": "Karnataka",
                    "district_city": "Vijayanagara",
                    "taluk": "Harapanahalli",
                    "government_level": "State Government",
                    "address": "Kottur Road, Harapanahalli, Vijayanagara - 583131",
                    "latitude": 14.7981,
                    "longitude": 75.9892,
                    "phone": "08398-252110",
                    "official_url": "https://gfgc.kar.nic.in",
                    "verified": True
                },
                {
                    "name": "Common Service Centre (CSC) Harapanahalli",
                    "name_kn": "ಸಿಎಸ್‌ಸಿ ಡಿಜಿಟಲ್ ಸೇವಾ ಕೇಂದ್ರ, ಹರಪನಹಳ್ಳಿ",
                    "name_hi": "कॉमन सर्विस सेंटर (सीएससी), हरपनहल्ली",
                    "category": "Common Service Centres (CSC)",
                    "state": "Karnataka",
                    "district_city": "Vijayanagara",
                    "taluk": "Harapanahalli",
                    "government_level": "Central Government",
                    "address": "Market Road, Harapanahalli, Vijayanagara - 583131",
                    "latitude": 14.7944,
                    "longitude": 75.9855,
                    "phone": "08398-253344",
                    "official_url": "https://csc.gov.in",
                    "verified": True
                },

                # 3. Kudligi Taluk
                {
                    "name": "Taluk Government Hospital Kudligi",
                    "name_kn": "ತಾಲೂಕು ಸಾರ್ವಜನಿಕ ಆಸ್ಪತ್ರೆ, ಕೂಡ್ಲಿಗಿ",
                    "name_hi": "तालुक सरकारी अस्पताल, कूडलिगी",
                    "category": "AIIMS & Central/State Hospitals",
                    "state": "Karnataka",
                    "district_city": "Vijayanagara",
                    "taluk": "Kudligi",
                    "government_level": "State Government",
                    "address": "Station Road, Kudligi Town, Vijayanagara - 583135",
                    "latitude": 14.9015,
                    "longitude": 76.3882,
                    "phone": "08391-220108",
                    "official_url": "https://vijayanagara.nic.in",
                    "verified": True
                },
                {
                    "name": "Tahsildar & Taluk Panchayat Kudligi",
                    "name_kn": "ತಹಶೀಲ್ದಾರ್ ಹಾಗೂ ತಾಲೂಕು ಪಂಚಾಯಿತಿ ಕಚೇರಿ, ಕೂಡ್ಲಿಗಿ",
                    "name_hi": "तहसीलदार एवं तालुक पंचायत कार्यालय, कूडलिगी",
                    "category": "State Secretariat & Collectorates",
                    "state": "Karnataka",
                    "district_city": "Vijayanagara",
                    "taluk": "Kudligi",
                    "government_level": "State Government",
                    "address": "Taluk Office Road, Kudligi, Vijayanagara - 583135",
                    "latitude": 14.8988,
                    "longitude": 76.3854,
                    "phone": "08391-220120",
                    "official_url": "https://nadakacheri.karnataka.gov.in",
                    "verified": True
                },
                {
                    "name": "Government Pre-University College Kudligi",
                    "name_kn": "ಸರ್ಕಾರಿ ಪದವಿ ಪೂರ್ವ ಕಾಲೇಜು, ಕೂಡ್ಲಿಗಿ",
                    "name_hi": "राजकीय पीयू कॉलेज, कूडलिगी",
                    "category": "Central/State Universities & IITs",
                    "state": "Karnataka",
                    "district_city": "Vijayanagara",
                    "taluk": "Kudligi",
                    "government_level": "State Government",
                    "address": "Bypass Road, Kudligi, Vijayanagara - 583135",
                    "latitude": 14.9042,
                    "longitude": 76.3910,
                    "phone": "08391-220450",
                    "official_url": "https://pue.karnataka.gov.in",
                    "verified": True
                },
                {
                    "name": "Grama One Citizen Center Kudligi",
                    "name_kn": "ಗ್ರಾಮ ಒನ್ ಕೇಂದ್ರ, ಕೂಡ್ಲಿಗಿ",
                    "name_hi": "ग्राम वन केंद्र, कूडलिगी",
                    "category": "Common Service Centres (CSC)",
                    "state": "Karnataka",
                    "district_city": "Vijayanagara",
                    "taluk": "Kudligi",
                    "government_level": "State Government",
                    "address": "Old Bus Stand Circle, Kudligi, Vijayanagara - 583135",
                    "latitude": 14.9002,
                    "longitude": 76.3871,
                    "phone": "08391-221345",
                    "official_url": "https://sevasindhu.karnataka.gov.in",
                    "verified": True
                },

                # 4. Huvina Hadagali Taluk
                {
                    "name": "Taluk General Hospital Huvina Hadagali",
                    "name_kn": "ತಾಲೂಕು ಸಾರ್ವಜನಿಕ ಆಸ್ಪತ್ರೆ, ಹೂವಿನ ಹಡಗಲಿ",
                    "name_hi": "तालुक सामान्य अस्पताल, हूविना हडगली",
                    "category": "AIIMS & Central/State Hospitals",
                    "state": "Karnataka",
                    "district_city": "Vijayanagara",
                    "taluk": "Huvina Hadagali",
                    "government_level": "State Government",
                    "address": "Main Road, Huvina Hadagali, Vijayanagara - 583219",
                    "latitude": 15.0194,
                    "longitude": 75.9589,
                    "phone": "08399-240122",
                    "official_url": "https://vijayanagara.nic.in",
                    "verified": True
                },
                {
                    "name": "Tahsildar & Mini Vidhana Soudha Huvina Hadagali",
                    "name_kn": "ತಹಶೀಲ್ದಾರ್ ಕಚೇರಿ (ಮಿನಿ ವಿಧಾನ ಸೌಧ), ಹೂವಿನ ಹಡಗಲಿ",
                    "name_hi": "तहसीलदार कार्यालय, हूविना हडगली",
                    "category": "State Secretariat & Collectorates",
                    "state": "Karnataka",
                    "district_city": "Vijayanagara",
                    "taluk": "Huvina Hadagali",
                    "government_level": "State Government",
                    "address": "Mini Vidhana Soudha, Hadagali, Vijayanagara - 583219",
                    "latitude": 15.0210,
                    "longitude": 75.9565,
                    "phone": "08399-240130",
                    "official_url": "https://nadakacheri.karnataka.gov.in",
                    "verified": True
                },
                {
                    "name": "Government First Grade College Huvina Hadagali",
                    "name_kn": "ಸರ್ಕಾರಿ ಪ್ರಥಮ ದರ್ಜೆ ಕಾಲೇಜು, ಹೂವಿನ ಹಡಗಲಿ",
                    "name_hi": "राजकीय प्रथम श्रेणी कॉलेज, हूविना हडगली",
                    "category": "Central/State Universities & IITs",
                    "state": "Karnataka",
                    "district_city": "Vijayanagara",
                    "taluk": "Huvina Hadagali",
                    "government_level": "State Government",
                    "address": "Near Malleshwara Temple Road, Hadagali, Vijayanagara - 583219",
                    "latitude": 15.0235,
                    "longitude": 75.9612,
                    "phone": "08399-241500",
                    "official_url": "https://gfgc.kar.nic.in",
                    "verified": True
                },

                # 5. Hagaribommanahalli Taluk
                {
                    "name": "Community Health Centre Hagaribommanahalli",
                    "name_kn": "ಸಮುದಾಯ ಆರೋಗ್ಯ ಕೇಂದ್ರ, ಹಗರಿಬೊಮ್ಮನಹಳ್ಳಿ",
                    "name_hi": "सामुदायिक स्वास्थ्य केंद्र, हगरीबोम्मनहल्ली",
                    "category": "AIIMS & Central/State Hospitals",
                    "state": "Karnataka",
                    "district_city": "Vijayanagara",
                    "taluk": "Hagaribommanahalli",
                    "government_level": "State Government",
                    "address": "Hospital Circle, Hagaribommanahalli, Vijayanagara - 583212",
                    "latitude": 15.0782,
                    "longitude": 76.1983,
                    "phone": "08397-238100",
                    "official_url": "https://vijayanagara.nic.in",
                    "verified": True
                },
                {
                    "name": "Tahsildar Office Hagaribommanahalli",
                    "name_kn": "ತಹಶೀಲ್ದಾರ್ ಕಚೇರಿ, ಹಗರಿಬೊಮ್ಮನಹಳ್ಳಿ",
                    "name_hi": "तहसीलदार कार्यालय, हगरीबोम्मनहल्ली",
                    "category": "State Secretariat & Collectorates",
                    "state": "Karnataka",
                    "district_city": "Vijayanagara",
                    "taluk": "Hagaribommanahalli",
                    "government_level": "State Government",
                    "address": "Taluk Office Building, Hagaribommanahalli, Vijayanagara - 583212",
                    "latitude": 15.0765,
                    "longitude": 76.1960,
                    "phone": "08397-238120",
                    "official_url": "https://nadakacheri.karnataka.gov.in",
                    "verified": True
                },
                {
                    "name": "Grama One Centre Hagaribommanahalli",
                    "name_kn": "ಗ್ರಾಮ ಒನ್ ಕೇಂದ್ರ, ಹಗರಿಬೊಮ್ಮನಹಳ್ಳಿ",
                    "name_hi": "ग्राम वन केंद्र, हगरीबोम्मनहल्ली",
                    "category": "Common Service Centres (CSC)",
                    "state": "Karnataka",
                    "district_city": "Vijayanagara",
                    "taluk": "Hagaribommanahalli",
                    "government_level": "State Government",
                    "address": "Near Bus Stand, Hagaribommanahalli, Vijayanagara - 583212",
                    "latitude": 15.0772,
                    "longitude": 76.1974,
                    "phone": "08397-238450",
                    "official_url": "https://sevasindhu.karnataka.gov.in",
                    "verified": True
                },

                # 6. Kottur Taluk
                {
                    "name": "Taluk General Hospital Kottur",
                    "name_kn": "ತಾಲೂಕು ಸಾರ್ವಜನಿಕ ಆಸ್ಪತ್ರೆ, ಕೊಟ್ಟೂರು",
                    "name_hi": "तालुक सामान्य अस्पताल, कोट्टूर",
                    "category": "AIIMS & Central/State Hospitals",
                    "state": "Karnataka",
                    "district_city": "Vijayanagara",
                    "taluk": "Kottur",
                    "government_level": "State Government",
                    "address": "Kottureshwara Temple Road, Kottur, Vijayanagara - 583134",
                    "latitude": 14.8214,
                    "longitude": 76.2185,
                    "phone": "08391-232120",
                    "official_url": "https://vijayanagara.nic.in",
                    "verified": True
                },
                {
                    "name": "Tahsildar & Taluk Office Kottur",
                    "name_kn": "ತಹಶೀಲ್ದಾರ್ ಹಾಗೂ ತಾಲೂಕು ಕಚೇರಿ, ಕೊಟ್ಟೂರು",
                    "name_hi": "तहसीलदार कार्यालय, कोट्टूर",
                    "category": "State Secretariat & Collectorates",
                    "state": "Karnataka",
                    "district_city": "Vijayanagara",
                    "taluk": "Kottur",
                    "government_level": "State Government",
                    "address": "Court Road, Kottur, Vijayanagara - 583134",
                    "latitude": 14.8235,
                    "longitude": 76.2160,
                    "phone": "08391-232130",
                    "official_url": "https://nadakacheri.karnataka.gov.in",
                    "verified": True
                },
                {
                    "name": "Government First Grade College Kottur",
                    "name_kn": "ಸರ್ಕಾರಿ ಪ್ರಥಮ ದರ್ಜೆ ಕಾಲೇಜು, ಕೊಟ್ಟೂರು",
                    "name_hi": "राजकीय प्रथम श्रेणी कॉलेज, कोट्टूर",
                    "category": "Central/State Universities & IITs",
                    "state": "Karnataka",
                    "district_city": "Vijayanagara",
                    "taluk": "Kottur",
                    "government_level": "State Government",
                    "address": "Ujjini Road, Kottur, Vijayanagara - 583134",
                    "latitude": 14.8180,
                    "longitude": 76.2220,
                    "phone": "08391-232500",
                    "official_url": "https://gfgc.kar.nic.in",
                    "verified": True
                },
                {
                    "name": "Common Service Centre (CSC) Kottur",
                    "name_kn": "ಸಿಎಸ್‌ಸಿ ಕೇಂದ್ರ, ಕೊಟ್ಟೂರು",
                    "name_hi": "कॉमन सर्विस सेंटर (सीएससी), कोट्टूर",
                    "category": "Common Service Centres (CSC)",
                    "state": "Karnataka",
                    "district_city": "Vijayanagara",
                    "taluk": "Kottur",
                    "government_level": "Central Government",
                    "address": "Car Street, Near Kottureshwara Temple, Kottur, Vijayanagara - 583134",
                    "latitude": 14.8220,
                    "longitude": 76.2172,
                    "phone": "08391-233111",
                    "official_url": "https://csc.gov.in",
                    "verified": True
                }
            ]

            for s_item in services_data:
                service_obj = PublicService(**s_item)
                db.session.add(service_obj)
            print(f"[Seed] Added {len(services_data)} verified public service centers across India & Karnataka/Vijayanagara.")

        # 4. Seed Official Documents & Ingest into RAG
        documents_dir = app.config.get('DOCUMENTS_DIR')
        if os.path.exists(documents_dir):
            doc_files = [
                {
                    "filename": "pm_surya_ghar_guidelines.txt",
                    "title": "PM Surya Ghar: Muft Bijli Yojana Guidelines",
                    "authority": "Ministry of New and Renewable Energy (MNRE), GoI",
                    "source_url": "https://pmsuryaghar.gov.in",
                    "publication_date": "2024-2026",
                    "jurisdiction": "Central / All India"
                },
                {
                    "filename": "pm_vishwakarma_scheme_order.txt",
                    "title": "PM Vishwakarma Scheme Guidelines & Benefits",
                    "authority": "Ministry of Micro, Small and Medium Enterprises (MSME), GoI",
                    "source_url": "https://pmvishwakarma.gov.in",
                    "publication_date": "2023-2026",
                    "jurisdiction": "Central / All India"
                },
                {
                    "filename": "pm_mudra_yojana_guidelines.txt",
                    "title": "Pradhan Mantri Mudra Yojana (PMMY) Operational Manual",
                    "authority": "Department of Financial Services, Ministry of Finance, GoI",
                    "source_url": "https://www.mudra.org.in",
                    "publication_date": "2024-2026",
                    "jurisdiction": "Central / All India"
                },
                {
                    "filename": "pm_kisan_samman_nidhi_manual.txt",
                    "title": "PM-Kisan Samman Nidhi Operational Manual",
                    "authority": "Ministry of Agriculture & Farmers Welfare, GoI",
                    "source_url": "https://pmkisan.gov.in",
                    "publication_date": "2024-2026",
                    "jurisdiction": "Central / All India"
                },
                {
                    "filename": "ayushman_bharat_pmjay_arogya_karnataka.txt",
                    "title": "Ayushman Bharat - Arogya Karnataka Health Assurance Manual",
                    "authority": "National Health Authority & SAST Karnataka",
                    "source_url": "https://sast.karnataka.gov.in",
                    "publication_date": "2024-2026",
                    "jurisdiction": "Central & Karnataka"
                },
                {
                    "filename": "karnataka_gruha_lakshmi_guidelines.txt",
                    "title": "Karnataka Gruha Lakshmi Scheme Guidelines",
                    "authority": "Dept of Women & Child Development, Karnataka",
                    "source_url": "https://sevasindhugs.karnataka.gov.in",
                    "publication_date": "2024-2026",
                    "jurisdiction": "Karnataka State"
                },
                {
                    "filename": "karnataka_yuva_nidhi_order.txt",
                    "title": "Karnataka Yuva Nidhi Scheme Government Order",
                    "authority": "Skill Development & Livelihood Dept, Karnataka",
                    "source_url": "https://sevasindhugs.karnataka.gov.in",
                    "publication_date": "2024-2026",
                    "jurisdiction": "Karnataka State"
                },
                {
                    "filename": "ssp_scholarship_guidelines.txt",
                    "title": "State Scholarship Portal (SSP) Post-Matric Guidelines",
                    "authority": "Center for e-Governance & Social Welfare Dept, Karnataka",
                    "source_url": "https://ssp.postmatric.karnataka.gov.in",
                    "publication_date": "2024-2026",
                    "jurisdiction": "Karnataka State"
                },
                {
                    "filename": "vijayanagara_district_citizen_services.txt",
                    "title": "Vijayanagara District Citizen Charter & Public Services Directory",
                    "authority": "District Administration Vijayanagara, Hosapete",
                    "source_url": "https://vijayanagara.nic.in",
                    "publication_date": "2024-2026",
                    "jurisdiction": "Vijayanagara District, Karnataka"
                }
            ]

            for d_info in doc_files:
                fpath = os.path.join(documents_dir, d_info["filename"])
                if os.path.exists(fpath):
                    existing = Document.query.filter_by(title=d_info["title"]).first()
                    if not existing:
                        doc_record = Document(
                            title=d_info["title"],
                            file_path=fpath,
                            source_url=d_info["source_url"],
                            authority=d_info["authority"],
                            publication_date=d_info["publication_date"],
                            jurisdiction=d_info["jurisdiction"],
                            verified=True
                        )
                        db.session.add(doc_record)
                        db.session.flush() # Get generated id
                        
                        # Ingest into RAG engine
                        chunk_count = rag_engine.ingest_document(
                            doc_id=doc_record.id,
                            title=doc_record.title,
                            file_path=fpath,
                            authority=doc_record.authority,
                            source_url=doc_record.source_url,
                            publication_date=doc_record.publication_date,
                            jurisdiction=doc_record.jurisdiction
                        )
                        doc_record.chunk_count = chunk_count
                        print(f"[Seed] Ingested document '{d_info['title']}' ({chunk_count} chunks) into RAG.")

        db.session.commit()
        print("[Seed] Database seeding and RAG vector store indexing completed successfully.")
