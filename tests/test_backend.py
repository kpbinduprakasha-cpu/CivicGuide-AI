import unittest
import json
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app import create_app
from app.models import db, User, Scheme, PublicService, Document, OTPVerification
from config import Config

class TestConfig(Config):
    TESTING = True
    DB_PATH = os.path.join(os.path.dirname(__file__), 'test_civicguide.db').replace('\\', '/')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'
    WTF_CSRF_ENABLED = False
    DEV_MODE_MOCK_EMAIL = True
    OTP_EXPIRY_SECONDS = 300
    OTP_RESEND_COOLDOWN_SECONDS = 60
    OTP_MAX_ATTEMPTS = 5

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

    def test_01_user_registration_and_otp_verification(self):
        """Test registration with 9 fields, User ID generation, compulsory OTP verification, and login."""
        # 1. Register new citizen
        reg_payload = {
            'full_name': 'Rahul Kumar',
            'age': 25,
            'mobile_number': '9876543210',
            'state': 'Karnataka',
            'sex': 'Male',
            'languages': ['English', 'Kannada', 'Hindi'],
            'email': 'rahul.kumar@example.com',
            'password': 'Password@123',
            'confirm_password': 'Password@123'
        }
        res = self.client.post('/api/auth/register', json=reg_payload)
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertIn('user_id', data)
        self.assertTrue(data['user_id'].startswith('rahul'))
        self.assertIn('dev_otp', data)
        user_id = data['user_id']
        otp_code = data['dev_otp']

        # 2. Verify account is not verified yet; login before OTP verification should be rejected (403)
        unverified_login = self.client.post('/api/auth/login', json={
            'user_id': user_id,
            'password': 'Password@123'
        })
        self.assertEqual(unverified_login.status_code, 403)
        self.assertTrue(unverified_login.get_json().get('needs_verification'))

        # 3. Test wrong OTP attempt
        bad_otp_res = self.client.post('/api/auth/verify-otp', json={
            'email': 'rahul.kumar@example.com',
            'otp': '000000'
        })
        self.assertEqual(bad_otp_res.status_code, 400)

        # 4. Verify with correct 6-digit OTP
        verify_res = self.client.post('/api/auth/verify-otp', json={
            'email': 'rahul.kumar@example.com',
            'otp': otp_code
        })
        self.assertEqual(verify_res.status_code, 200)
        verify_data = verify_res.get_json()
        self.assertIn('token', verify_data)
        self.assertEqual(verify_data['user']['user_id'], user_id)
        self.assertTrue(verify_data['user']['is_verified'])
        token = verify_data['token']

        # 5. Returning Login: Only needs User ID and Password (NO OTP on regular login!)
        login_res = self.client.post('/api/auth/login', json={
            'user_id': user_id,
            'password': 'Password@123'
        })
        self.assertEqual(login_res.status_code, 200)
        self.assertEqual(login_res.get_json()['user_id'], user_id)

        # 6. Access protected /me endpoint
        me_res = self.client.get('/api/auth/me', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(me_res.status_code, 200)
        user_info = me_res.get_json()['user']
        self.assertEqual(user_info['full_name'], 'Rahul Kumar')
        self.assertEqual(user_info['age'], 25)
        self.assertEqual(user_info['mobile_number'], '9876543210')
        self.assertEqual(user_info['state'], 'Karnataka')
        self.assertEqual(user_info['sex'], 'Male')
        self.assertIn('Kannada', user_info['languages'])

    def test_02_profile_update_and_change_password(self):
        """Test editing profile attributes and changing password."""
        # Setup verified user
        user = User(
            user_id='priya123',
            full_name='Priya Sharma',
            age=28,
            mobile_number='9123456780',
            state='Delhi',
            sex='Female',
            email='priya@example.com',
            is_verified=True
        )
        user.set_password('OldPassword@123')
        user.set_languages_list(['English', 'Hindi'])
        db.session.add(user)
        db.session.commit()

        # Login
        login_res = self.client.post('/api/auth/login', json={
            'user_id': 'priya123',
            'password': 'OldPassword@123'
        })
        token = login_res.get_json()['token']

        # Update profile
        update_res = self.client.put('/api/auth/profile', json={
            'full_name': 'Priya S. Sharma',
            'age': 29,
            'state': 'Maharashtra',
            'languages': ['English', 'Hindi', 'Marathi']
        }, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(update_res.status_code, 200)
        updated_user = update_res.get_json()['user']
        self.assertEqual(updated_user['full_name'], 'Priya S. Sharma')
        self.assertEqual(updated_user['age'], 29)
        self.assertEqual(updated_user['state'], 'Maharashtra')
        self.assertIn('Marathi', updated_user['languages'])

        # Change password
        pwd_res = self.client.put('/api/auth/change-password', json={
            'current_password': 'OldPassword@123',
            'new_password': 'NewPassword@2026',
            'confirm_password': 'NewPassword@2026'
        }, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(pwd_res.status_code, 200)

        # Login with old password must fail
        fail_login = self.client.post('/api/auth/login', json={
            'user_id': 'priya123',
            'password': 'OldPassword@123'
        })
        self.assertEqual(fail_login.status_code, 401)

        # Login with new password must succeed
        success_login = self.client.post('/api/auth/login', json={
            'user_id': 'priya123',
            'password': 'NewPassword@2026'
        })
        self.assertEqual(success_login.status_code, 200)

    def test_03_forgot_password_workflow(self):
        """Test forgot password request, OTP dispatch, reset verification, and login."""
        user = User(
            user_id='anil456',
            full_name='Anil Gowda',
            age=35,
            mobile_number='9845012345',
            state='Karnataka',
            sex='Male',
            email='anil@example.com',
            is_verified=True
        )
        user.set_password('AnilInitial@123')
        db.session.add(user)
        db.session.commit()

        # 1. Request forgot password OTP
        req_res = self.client.post('/api/auth/forgot-password', json={'email': 'anil@example.com'})
        self.assertEqual(req_res.status_code, 200)
        dev_otp = req_res.get_json()['dev_otp']
        self.assertTrue(bool(dev_otp))

        # 2. Reset password using 6-digit OTP
        reset_res = self.client.post('/api/auth/reset-password', json={
            'email': 'anil@example.com',
            'otp': dev_otp,
            'new_password': 'AnilBrandNew@2026',
            'confirm_password': 'AnilBrandNew@2026'
        })
        self.assertEqual(reset_res.status_code, 200)

        # 3. Login with newly reset password
        login_res = self.client.post('/api/auth/login', json={
            'user_id': 'anil456',
            'password': 'AnilBrandNew@2026'
        })
        self.assertEqual(login_res.status_code, 200)

    def test_04_schemes_directory(self):
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

    def test_05_public_services_and_taluks(self):
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

    def test_06_eligibility_evaluation(self):
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

    def test_07_admin_access_control(self):
        """Test that regular citizen cannot access admin endpoints and admin can."""
        # Create citizen
        citizen = User(
            user_id='citizen999',
            full_name='Regular Citizen',
            email='citizen999@example.com',
            is_verified=True,
            role='user'
        )
        citizen.set_password('Password@123')
        db.session.add(citizen)
        db.session.commit()

        login_res = self.client.post('/api/auth/login', json={
            'user_id': 'citizen999',
            'password': 'Password@123'
        })
        citizen_token = login_res.get_json()['token']

        # Citizen trying to access /api/admin/stats
        unauthorized_res = self.client.get('/api/admin/stats', headers={'Authorization': f'Bearer {citizen_token}'})
        self.assertEqual(unauthorized_res.status_code, 403)

        # Admin login
        admin_res = self.client.post('/api/auth/login', json={
            'user_id': 'admin',
            'password': 'Admin@CivicGuide2026'
        })
        admin_token = admin_res.get_json()['token']

        # Admin accessing /api/admin/stats
        authorized_res = self.client.get('/api/admin/stats', headers={'Authorization': f'Bearer {admin_token}'})
        self.assertEqual(authorized_res.status_code, 200)
        self.assertIn('users_count', authorized_res.get_json())

    def test_08_all_india_services_and_states(self):
        """Test All India states, central government services, and national schemes."""
        res = self.client.get('/api/public-services/states')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['country'], 'India')
        self.assertGreaterEqual(data['central_services_count'], 1)
        state_names = [s['state'] for s in data['states']]
        self.assertIn('Delhi', state_names)
        self.assertIn('Karnataka', state_names)

        # Test Central Government services filter
        res_central = self.client.get('/api/public-services?level=Central%20Government')
        self.assertEqual(res_central.status_code, 200)
        for svc in res_central.get_json()['services']:
            self.assertEqual(svc['government_level'], 'Central Government')

if __name__ == '__main__':
    unittest.main()
