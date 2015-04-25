import unittest
import json
from unittests import BaseMalbTester


def decode_json(s):
    return json.loads(s.data.decode('utf-8'))


VALID_FORM_DATA = {
    'malId': 1,
    'myScore': 10,
    'myStatus': 1,
    'myEpisodes': 20,
    'myStartDate': '01/20/2001',
    'myEndDate': '03/02/1991',
}

VALID_INVALID_FORM_DATA = {
    'malId': 1,
    'myScore': 10,
    'myStatus': 1,
    'myEpisodes': 20,
    'myStartDate': '01/20/2001',
    'myEndDate': '3/4/15',
}

INVALID_FORM_DATA = {
    'malId': 1,
    'myScore': 10,
    'myStatus': 1,
    'myEpisodes': 20,
    'myStartDate': '01/20/91',
    'myEndDate': '555555',
}

UPDATE_DATA_STATUS = {
    'malId': 1,
    'myScore': 10,
    'myStatus': 4,
    'myEpisodes': 20,
    'myStartDate': '01/20/2001',
    'myEndDate': '03/02/1991',
}

UPDATE_DATA_SCORE = {
    'malId': 1,
    'myScore': 8,
    'myStatus': 1,
    'myEpisodes': 20,
    'myStartDate': '01/20/2001',
    'myEndDate': '03/02/1991',
}

UPDATE_DATA_EPISODE = {
    'malId': 1,
    'myScore': 10,
    'myStatus': 1,
    'myEpisodes': 10,
    'myStartDate': '01/20/2001',
    'myEndDate': '03/02/1991',
}

UPDATE_DATA_INVALID_STATUS = {
    'malId': 1,
    'myScore': 10,
    'myStatus': -2,
    'myEpisodes': 20,
    'myStartDate': '01/20/2001',
    'myEndDate': '03/02/1991',
}

UPDATE_DATA_INVALID_SCORE = {
    'malId': 1,
    'myScore': -3,
    'myStatus': 1,
    'myEpisodes': 20,
    'myStartDate': '01/20/2001',
    'myEndDate': '03/02/1991',
}

UPDATE_DATA_INVALID_EPISODE = {
    'malId': 1,
    'myScore': 10,
    'myStatus': 1,
    'myEpisodes': 666,
    'myStartDate': '01/20/2001',
    'myEndDate': '03/02/1991',
}


class UpdateAnimeTest(BaseMalbTester.BaseMalbTest):
    def test_update_status(self):
        """Test update status functionality through frontend"""
        # Login
        self.login()
        self.navigate_to('/updateanime')

        s0 = self.submit_to('/update_anime', UPDATE_DATA_STATUS)

        self.assertEqual(s0._status_code, 200)

    def test_update_score(self):
        """Test update score functionality through frontend"""
        # Login
        self.login()
        self.navigate_to('/updateanime')

        s0 = self.submit_to('/update_anime', UPDATE_DATA_SCORE)

        self.assertEqual(s0._status_code, 200)

    def test_update_episode(self):
        """Test update episode count functionality through frontend"""
        # Login
        self.login()
        self.navigate_to('/updateanime')

        s0 = self.submit_to('/update_anime', UPDATE_DATA_EPISODE)

        self.assertEqual(s0._status_code, 200)

    def test_update_invalid_status(self):
        """Test update invalid status functionality through frontend"""
        # Login
        self.login()
        self.navigate_to('/updateanime')

        s0 = self.submit_to('/update_anime', UPDATE_DATA_INVALID_STATUS)

        self.assertEqual(s0._status_code, 400)

    def test_update_invalid_score(self):
        """Test update invalid score functionality through frontend"""
        # Login
        self.login()
        self.navigate_to('/updateanime')

        s0 = self.submit_to('/update_anime', UPDATE_DATA_INVALID_SCORE)

        self.assertEqual(s0._status_code, 400)

    def test_update_invalid_episode(self):
        """Test update invalid episode functionality through frontend"""
        # Login
        self.login()
        self.navigate_to('/updateanime')

        s0 = self.submit_to('/update_anime', UPDATE_DATA_INVALID_EPISODE)

        self.assertEqual(s0._status_code, 400)

    def test_start_valid_date(self):
        """Test update start date"""
        self.login()
        self.navigate_to('/update_anime')

        s0 = self.submit_to('/update_anime', VALID_FORM_DATA)
        # print(s0._status_code)
        # print(s0.data)
        # print(type(s0))
        # print(dir(s0))
        page = self.navigate_to('/updateanime').data.decode('utf-8')

        self.logout()
        self.assertEqual(s0._status_code, 200)
        self.assertIn('01/20/2001', page)

    def test_end_valid_date(self):
        """Test update end date"""
        self.login()
        self.navigate_to('/update_anime')

        s0 = self.submit_to('/update_anime', VALID_FORM_DATA)
        page = self.navigate_to('/updateanime').data.decode('utf-8')

        self.logout()
        self.assertEqual(s0._status_code, 200)
        self.assertIn('03/02/1991', page)

    def test_start_invalid_date(self):
        """Test update invalid start date"""
        self.login()
        self.navigate_to('/update_anime')

        s0 = self.submit_to('/update_anime', INVALID_FORM_DATA)
        page = self.navigate_to('/updateanime').data.decode('utf-8')

        self.logout()
        self.assertEqual(s0._status_code, 400)
        self.assertNotIn('01/20/91', page)

    def test_end_invalid_date(self):
        """Test update invalid end date"""
        self.login()
        self.navigate_to('/update_anime')

        s0 = self.submit_to('/update_anime', INVALID_FORM_DATA)
        page = self.navigate_to('/updateanime').data.decode('utf-8')

        self.logout()

        self.assertEqual(s0._status_code, 400)
        self.assertNotIn('3/4/15', page)

    def test_start_valid_end_invalid_date(self):
        """Test update invalid end date"""
        self.login()
        self.navigate_to('/update_anime')

        s0 = self.submit_to('/update_anime', VALID_INVALID_FORM_DATA)
        page = self.navigate_to('/updateanime').data.decode('utf-8')

        self.logout()

        self.assertEqual(s0._status_code, 400)
        self.assertNotIn('555555', page)

if __name__ == '__main__':
    unittest.main()