import unittest
import json
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app import create_app
from app.models import db, User, Scheme, PublicService, Document
from config import Config

class TestConfig(Config):
    TESTING = True
    DB_PATH = os.path.join(os.path.dirname(__file__), 'test_civicguide.db').replace('\\', '/')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'
    WTF_CSRF_ENABLED = False

class CivicGuideBackendTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        # Clean test db file
        test_db = os.path.join(os.path.dirname(__file__), 'test_civicguide.db')
        if os.path.exists(test_db):
            try:
                os.remove(test_db)
            except Exception:
                pass

    def test_01_user_registration_and_login(self):
        """Test registration, uniqueness checks, and login authentication."""
        # 1. Register new citizen
        reg_payload = {
            'full_name': 'Basavaraj Patil',
            'email': 'basavaraj@example.com',
            'username': 'basavaraj_vjy',
            'password': 'Password@123',
            'confirm_password': 'Password@123',
            'preferred_language': 'kn'
        }
        res = self.client.post('/api/auth/register', json=reg_payload)
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertIn('token', data)
        self.assertEqual(data['user']['username'], 'basavaraj_vjy')
        token = data['token']

        # 2. Duplicate registration rejection
        res_dup = self.client.post('/api/auth/register', json=reg_payload)
        self.assertEqual(res_dup.status_code, 409)

        # 3. Login
        login_res = self.client.post('/api/auth/login', json={
            'identifier': 'basavaraj_vjy',
            'password': 'Password@123'
        })
        self.assertEqual(login_res.status_code, 200)
        self.assertIn('token', login_res.get_json())

        # 4. Access protected /me
        me_res = self.client.get('/api/auth/me', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(me_res.status_code, 200)
        self.assertEqual(me_res.get_json()['user']['email'], 'basavaraj@example.com')

    def test_02_schemes_directory(self):
        """Test government schemes list and filters."""
        res = self.client.get('/api/schemes')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertGreaterEqual(data['count'], 1)
        
        # Test category filter
        res_cat = self.client.get('/api/schemes?category=Agriculture')
        self.assertEqual(res_cat.status_code, 200)
        for s in res_cat.get_json()['schemes']:
            self.assertEqual(s['category'], 'Agriculture')

    def test_03_public_services_and_taluks(self):
        """Test Vijayanagara 6 taluks public services."""
        res = self.client.get('/api/public-services/taluks')
        self.assertEqual(res.status_code, 200)
        taluks = [t['name'] for t in res.get_json()['taluks']]
        expected_taluks = ['Hosapete', 'Harapanahalli', 'Kudligi', 'Huvina Hadagali', 'Hagaribommanahalli', 'Kottur']
        for et in expected_taluks:
            self.assertIn(et, taluks)

        # Test filter by taluk
        res_hp = self.client.get('/api/public-services?taluk=Hosapete')
        self.assertEqual(res_hp.status_code, 200)
        for svc in res_hp.get_json()['services']:
            self.assertEqual(svc['taluk'], 'Hosapete')

    def test_04_eligibility_evaluation(self):
        """Test scheme eligibility rule engine."""
        payload = {
            'age': 32,
            'state': 'Karnataka',
            'district': 'Vijayanagara',
            'gender': 'female',
            'ration_card_type': 'BPL',
            'occupation': 'homemaker',
            'annual_income': 100000,
            'language': 'en'
        }
        res = self.client.post('/api/eligibility/check', json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertGreaterEqual(data['count'], 1)
        
        # Check Gruha Lakshmi evaluation
        gl = [r for r in data['results'] if 'Gruha Lakshmi' in r['scheme_name']]
        self.assertTrue(len(gl) > 0)
        self.assertEqual(gl[0]['status'], 'Possibly Eligible')

    def test_05_chat_and_rag_synthesis(self):
        """Test AI chatbot retrieval with RAG context."""
        chat_payload = {
            'question': 'How can I apply for Gruha Lakshmi Scheme?',
            'language': 'en'
        }
        res = self.client.post('/api/chat', json=chat_payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn('answer', data)
        self.assertIn('sources', data)

    def test_06_admin_access_control(self):
        """Test that regular citizen cannot access admin endpoints and admin can."""
        # Citizen login
        reg_res = self.client.post('/api/auth/register', json={
            'full_name': 'Regular Citizen',
            'email': 'reg@example.com',
            'username': 'reg_citizen',
            'password': 'Password@123',
            'confirm_password': 'Password@123'
        })
        citizen_token = reg_res.get_json()['token']

        # Citizen trying to access /api/admin/stats
        unauthorized_res = self.client.get('/api/admin/stats', headers={'Authorization': f'Bearer {citizen_token}'})
        self.assertEqual(unauthorized_res.status_code, 403)

        # Admin login
        admin_res = self.client.post('/api/auth/login', json={
            'identifier': 'admin',
            'password': 'Admin@CivicGuide2026'
        })
        admin_token = admin_res.get_json()['token']

        # Admin accessing /api/admin/stats
        authorized_res = self.client.get('/api/admin/stats', headers={'Authorization': f'Bearer {admin_token}'})
        self.assertEqual(authorized_res.status_code, 200)
        self.assertIn('users_count', authorized_res.get_json())

    def test_07_all_india_services_and_states(self):
        """Test All India states, central government services, and national schemes."""
        # 1. Test states endpoint
        res = self.client.get('/api/public-services/states')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['country'], 'India')
        self.assertGreaterEqual(data['central_services_count'], 1)
        state_names = [s['state'] for s in data['states']]
        self.assertIn('Delhi', state_names)
        self.assertIn('Karnataka', state_names)

        # 2. Test Central Government services filter
        res_central = self.client.get('/api/public-services?level=Central%20Government')
        self.assertEqual(res_central.status_code, 200)
        for svc in res_central.get_json()['services']:
            self.assertEqual(svc['government_level'], 'Central Government')

        # 3. Test Central Government schemes filter
        res_schemes = self.client.get('/api/schemes?level=Central%20Government')
        self.assertEqual(res_schemes.status_code, 200)
        scheme_names = [s['name'] for s in res_schemes.get_json()['schemes']]
        self.assertTrue(any('PM Surya Ghar' in name for name in scheme_names))
        self.assertTrue(any('PM-Kisan' in name for name in scheme_names))

if __name__ == '__main__':
    unittest.main()
