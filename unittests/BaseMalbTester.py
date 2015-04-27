import unittest
import src.malb as MALB
import src.malsession as MAL

from src import app, db
from src.models import UserToAnime

TEST_USERNAME = 'quetzalcoatl384'
TEST_PASSWORD = 'password'
TEST_USERID = 4448103
TEST_MALKEY = 'cXVldHphbGNvYXRsMzg0OnBhc3N3b3Jk'

LOGIN_DATA = {
    'username': TEST_USERNAME,
    'password': TEST_PASSWORD,
}

COWBOY_BEBOP = UserToAnime(TEST_USERID, 1)
TRIGUN = UserToAnime(TEST_USERID, 6)
HONEY_AND_CLOVER = UserToAnime(TEST_USERID, 16)
MONSTER = UserToAnime(TEST_USERID, 19)
NARUTO = UserToAnime(TEST_USERID, 20)

COWBOY_BEBOP.myStatus = 2
COWBOY_BEBOP.myEpisodes = 26
COWBOY_BEBOP.myScore = 10

TRIGUN.myStatus = 2
TRIGUN.myEpisodes = 26
TRIGUN.myScore = 9

HONEY_AND_CLOVER.myStatus = 1
HONEY_AND_CLOVER.myEpisodes = 12
HONEY_AND_CLOVER.myScore = 7

MONSTER.myStatus = 1
MONSTER.myEpisodes = 35
MONSTER.myScore = 8

NARUTO.myStatus = 1
NARUTO.myEpisodes = 80
NARUTO.myScore = 5

TEST_MAL = [
    COWBOY_BEBOP,
    TRIGUN,
    HONEY_AND_CLOVER,
    MONSTER,
    NARUTO,
]

TEST_MALFIELDS = {
    'malId',
    'myStatus',
    'myEpisodes',
    'myScore'
}


def init_test_mal():
    temp = app.config['MAL_TRANSACTIONS_ENABLED']
    app.config['MAL_TRANSACTIONS_ENABLED'] = True
    MAL.delete_all_by_id(TEST_MALKEY, MAL.get_mal_ids(TEST_USERNAME, TEST_MALKEY))
    MAL.add_all(TEST_MALKEY, TEST_MAL, TEST_MALFIELDS)
    app.config['MAL_TRANSACTIONS_ENABLED'] = temp


class BaseMalbTest(unittest.TestCase):
    def setUp(self):
        app.config['MAL_TRANSACTIONS_ENABLED'] = False
        self.setUpHelper()

    def test_transmit(self):
        init_test_mal()

    def setUpHelper(self):
        """Configure test app and upload sample data"""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dev:uiuc@localhost/malb-test'
        self.app = app.test_client()
        self.TEST_USERNAME = TEST_USERNAME
        self.TEST_MALKEY = TEST_MALKEY
        self.TEST_MAL = TEST_MAL
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