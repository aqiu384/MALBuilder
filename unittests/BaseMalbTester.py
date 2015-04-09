import unittest
import src.malb as MALB

from src import app, db

LOGIN_DATA = {
    'username': 'quetzalcoatl384',
    'password': 'password'
}


class BaseMalbTest(unittest.TestCase):
    def setUp(self):
        app.config['MAL_TRANSACTIONS_ENABLED'] = False
        self.setUpHelper()

    def setUpHelper(self):
        """Configure test app and upload sample data"""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dev:uiuc@localhost/malb-test'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

        MALB.synchronize_with_mal('quetzalcoatl384', 'cXVldHphbGNvYXRsMzg0OnBhc3N3b3Jk', 4448103)
        MALB.upload_aa_data('../data/aaresults0.txt')

    def tearDown(self):
        """Remove all test data"""
        db.session.remove()
        db.drop_all()

    def login(self):
        """Login test user"""
        return self.app.post('/login', data=LOGIN_DATA, follow_redirects=True)

    def logout(self):
        """Logout test user"""
        return self.app.get('/logout', follow_redirects=True)

    def navigate_to(self, url):
        """Navigate to page"""
        return self.app.get(url, follow_redirects=True)

    def submit_to(self, url, data):
        """Submit data on page"""
        return self.app.post(url, data=data, follow_redirects=True)

if __name__ == '__main__':
    unittest.main()