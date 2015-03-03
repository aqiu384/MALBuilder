import unittest
import malb

from app import app, db
from datetime import date


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dev:uiuc@localhost/malb-test'
        self.app = app.test_client()
        db.create_all()

        malb.synchronize_with_mal('quetzalcoatl384', 'cXVldHphbGNvYXRsMzg0OnBhc3N3b3Jk')
        malb.upload_aa_data('../data/aaresults0.txt')

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @unittest.skip('Already demonstrated')
    def test_get_malb(self):
        results = malb.get_malb(4448103)
        self.assertEqual(7, len(results))

    def test_search_anime(self):
        results = malb.search_anime({}, ['title'])
        self.assertEquals(300, len(results))
        self.assertEquals('.hack//Liminality', results[0][0])
        self.assertEquals('.hack//Sign', results[1][0])
        self.assertEquals('.hack//Tasogare no Udewa Densetsu', results[2][0])

        results = malb.search_anime({
            'startDateStart': date(1999, 1, 1),
            'endDateEnd': date(2000, 1, 1)
        }, ['title', 'startDate'], sort_col='startDate')

        self.assertEquals(6, len(results))
        self.assertEquals('Seikai no Monshou', results[0][0])
        self.assertEquals(date(1999, 1, 2), results[0][1])
        self.assertEquals('Rurouni Kenshin: Meiji Kenkaku Romantan - Tsuiokuhen', results[1][0])
        self.assertEquals(date(1999, 2, 20), results[1][1])
        self.assertEquals('Power Stone', results[2][0])
        self.assertEquals(date(1999, 4, 3), results[2][1])

if __name__ == '__main__':
    unittest.main()