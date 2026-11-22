import os
from sqlalchemy import inspect, text
from ..models import db, User, Scheme, PublicService, Document
from ..rag.rag_engine import rag_engine
from .all_india_schemes_data import ALL_INDIA_SCHEMES
from .all_india_services_data import ALL_PUBLIC_SERVICES

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
            services_data = ALL_PUBLIC_SERVICES
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
