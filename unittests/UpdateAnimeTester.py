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
    'myEndDate': '03/02/1991'

}

VALID_INVALID_FORM_DATA = {
    'malId': 1,
    'myScore': 10,
    'myStatus': 1,
    'myEpisodes': 20,
    'myStartDate': '01/20/2001',
    'myEndDate': '3/4/15'

}

INVALID_FORM_DATA = {
    'malId': 1,
    'myScore': 10,
    'myStatus': 1,
    'myEpisodes': 20,
    'myStartDate': '01/20/91',
    'myEndDate': '555555'

}



OPTIONS_SCORE = {
    0: '<option selected value="0">0</option><option value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option><option value="6">6</option><option value="7">7</option><option value="8">8</option><option value="9">9</option><option value="10">10</option></select>',
    1: '<option value="0">0</option><option selected value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option><option value="6">6</option><option value="7">7</option><option value="8">8</option><option value="9">9</option><option value="10">10</option></select>',
    2: '<option value="0">0</option><option value="1">1</option><option selected value="2">2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option><option value="6">6</option><option value="7">7</option><option value="8">8</option><option value="9">9</option><option value="10">10</option></select>',
    3: '<option value="0">0</option><option value="1">1</option><option value="2">2</option><option selected value="3">3</option><option value="4">4</option><option value="5">5</option><option value="6">6</option><option value="7">7</option><option value="8">8</option><option value="9">9</option><option value="10">10</option></select>',
    4: '<option value="0">0</option><option value="1">1</option><option value="2">2</option><option value="3">3</option><option selected value="4">4</option><option value="5">5</option><option value="6">6</option><option value="7">7</option><option value="8">8</option><option value="9">9</option><option value="10">10</option></select>',
    5: '<option value="0">0</option><option value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option><option selected value="5">5</option><option value="6">6</option><option value="7">7</option><option value="8">8</option><option value="9">9</option><option value="10">10</option></select>',
    6: '<option value="0">0</option><option value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option><option selected value="6">6</option><option value="7">7</option><option value="8">8</option><option value="9">9</option><option value="10">10</option></select>',
    7: '<option value="0">0</option><option value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option><option value="6">6</option><option selected value="7">7</option><option value="8">8</option><option value="9">9</option><option value="10">10</option></select>',
    8: '<option value="0">0</option><option value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option><option value="6">6</option><option value="7">7</option><option selected value="8">8</option><option value="9">9</option><option value="10">10</option></select>',
    9: '<option value="0">0</option><option value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option><option value="6">6</option><option value="7">7</option><option value="8">8</option><option selected value="9">9</option><option value="10">10</option></select>',
    10: '<option value="0">0</option><option value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option><option value="6">6</option><option value="7">7</option><option value="8">8</option><option value="9">9</option><option selected value="10">10</option></select>',
    'none': '<option value="0">0</option><option value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option><option value="6">6</option><option value="7">7</option><option value="8">8</option><option value="9">9</option><option value="10">10</option></select>',
}

OPTIONS_STATUS = {
    1: '<option selected value="1">Watching</option><option value="2">Completed</option><option value="3">On hold</option><option value="4">Dropped</option><option value="6">Plan to watch</option><option value="10">Have not seen</option></select>',
    2: '<option value="1">Watching</option><option selected value="2">Completed</option><option value="3">On hold</option><option value="4">Dropped</option><option value="6">Plan to watch</option><option value="10">Have not seen</option></select>',
    3: '<option value="1">Watching</option><option value="2">Completed</option><option selected value="3">On hold</option><option value="4">Dropped</option><option value="6">Plan to watch</option><option value="10">Have not seen</option></select>',
    4: '<option value="1">Watching</option><option value="2">Completed</option><option value="3">On hold</option><option selected value="4">Dropped</option><option value="6">Plan to watch</option><option value="10">Have not seen</option></select>',
    6: '<option value="1">Watching</option><option value="2">Completed</option><option value="3">On hold</option><option value="4">Dropped</option><option selected value="6">Plan to watch</option><option value="10">Have not seen</option></select>',
    10: '<option value="1">Watching</option><option value="2">Completed</option><option value="3">On hold</option><option value="4">Dropped</option><option value="6">Plan to watch</option><option selected value="10">Have not seen</option></select>',
    'none': '<option value="1">Watching</option><option value="2">Completed</option><option value="3">On hold</option><option value="4">Dropped</option><option value="6">Plan to watch</option><option value="10">Have not seen</option></select>',
}


def get_HTML_SCORE_STR(num, opt):
    if opt in OPTIONS_SCORE.keys():
        return 'My Score: <select class="checkbox-grid1" id="edit_form-myScore_' + str(num) + '" name="edit_form-myScore_' + str(num) + '">' + OPTIONS_SCORE[opt]
    else:
        return 'My Score: <select class="checkbox-grid1" id="edit_form-myScore_' + str(num) + '" name="edit_form-myScore_' + str(num) + '">' + OPTIONS_SCORE['none']


def get_HTML_STATUS_STR(num, opt):
    if opt in OPTIONS_STATUS.keys():
        return 'My Status: <select class="checkbox-grid1" id="edit_form-myStatus_' + str(num) + '" name="edit_form-myStatus_' + str(num) + '">' + OPTIONS_STATUS[opt]
    else:
        return 'My Status: <select class="checkbox-grid1" id="edit_form-myStatus_' + str(num) + '" name="edit_form-myStatus_' + str(num) + '">' + OPTIONS_STATUS['none']

UPDATE_DATA_STATUS = {
    'edit_form-myStatus_0': 6,
    'edit_form-myStatus_1': 4,
    'edit_form-myStatus_2': 4,
}

UPDATE_DATA_SCORE = {
    'edit_form-myScore_0': 8,
    'edit_form-myScore_1': 1,
    'edit_form-myScore_2': 3,
}

UPDATE_DATA_EPISODE = {
    'edit_form-myEpisodes_0': 2,
    'edit_form-myEpisodes_1': 5,
    'edit_form-myEpisodes_2': 48,
}

UPDATE_DATA_INVALID_STATUS = {
    'edit_form-myStatus_0': -2,
    'edit_form-myStatus_1': 5,
    'edit_form-myStatus_2': 5,
}

UPDATE_DATA_INVALID_SCORE = {
    'edit_form-myScore_0': 11,
    'edit_form-myScore_1': -3,
    'edit_form-myScore_2': 42,
}

UPDATE_DATA_INVALID_EPISODE = {
    'edit_form-myEpisodes_0': -1,
    'edit_form-myEpisodes_1': 400,
    'edit_form-myEpisodes_2': 600,
}

UPDATE_DATA_VALID_START_DATE = {
    'edit_form-startDateStart_0': '12/12/2010',
    'edit_form-startDateStart_1': '02/01/1992',
    'edit_form-startDateStart_2': '11/06/2009',
}

class UpdateAnimeTest(BaseMalbTester.BaseMalbTest):

    def test_update_status(self):
        """Test update status functionality through frontend"""
        # Login
        self.login()
        self.navigate_to('/updateanime')

        page = self.submit_to('/updateanime', UPDATE_DATA_STATUS).data.decode('utf-8')

        self.assertTrue(get_HTML_STATUS_STR(0, 6) in page)
        self.assertTrue(get_HTML_STATUS_STR(1, 4) in page)
        self.assertTrue(get_HTML_STATUS_STR(2, 4) in page)

    def test_update_score(self):
        """Test update score functionality through frontend"""
        # Login
        self.login()
        self.navigate_to('/updateanime')

        page = self.submit_to('/updateanime', UPDATE_DATA_SCORE).data.decode('utf-8')

        self.assertTrue(get_HTML_SCORE_STR(0, 8) in page)
        self.assertTrue(get_HTML_SCORE_STR(1, 1) in page)
        self.assertTrue(get_HTML_SCORE_STR(2, 3) in page)

    def test_update_episode(self):
        """Test update episode count functionality through frontend"""
        # Login
        self.login()
        self.navigate_to('/updateanime')

        page = self.submit_to('/updateanime', UPDATE_DATA_EPISODE).data.decode('utf-8')

        # page html element position is REALLY important
        self.assertTrue('<input id="edit_form-myEpisodes_0" name="edit_form-myEpisodes_0" placeholder="1-26" type="text" value="2">' in page)
        self.assertTrue('<input id="edit_form-myEpisodes_1" name="edit_form-myEpisodes_1" placeholder="1-24" type="text" value="5">' in page)
        self.assertTrue('<input id="edit_form-myEpisodes_2" name="edit_form-myEpisodes_2" placeholder="1-74" type="text" value="48">' in page)

    def test_update_invalid_status(self):
        """Test update invalid status functionality through frontend"""
        # Login
        self.login()
        self.navigate_to('/updateanime')
        self.submit_to('/updateanime', UPDATE_DATA_STATUS).data.decode('utf-8')

        page = self.submit_to('/updateanime', UPDATE_DATA_INVALID_STATUS).data.decode('utf-8')

        # options are empty
        self.assertTrue(get_HTML_STATUS_STR(0, -2) in page)
        self.assertTrue(get_HTML_STATUS_STR(1, 5) in page)
        self.assertTrue(get_HTML_STATUS_STR(2, 5) in page)

    def test_update_invalid_score(self):
        """Test update invalid score functionality through frontend"""
        # Login
        self.login()
        self.navigate_to('/updateanime')
        self.submit_to('/updateanime', UPDATE_DATA_SCORE)

        page = self.submit_to('/updateanime', UPDATE_DATA_INVALID_SCORE).data.decode('utf-8')

        # option are empty
        self.assertTrue(get_HTML_SCORE_STR(0, 11) in page)
        self.assertTrue(get_HTML_SCORE_STR(1, -3) in page)
        self.assertTrue(get_HTML_SCORE_STR(2, 42) in page)

    def test_update_invalid_episode(self):
        """Test update invalid episode functionality through frontend"""
        # Login
        self.login()
        self.navigate_to('/updateanime')
        self.submit_to('/updateanime', UPDATE_DATA_EPISODE).data.decode('utf-8')

        page = self.submit_to('/updateanime', UPDATE_DATA_INVALID_EPISODE).data.decode('utf-8')

        # old values lingering
        self.assertTrue('<input id="edit_form-myEpisodes_0" name="edit_form-myEpisodes_0" placeholder="1-26" type="text" value="-1">' in page)
        self.assertTrue('<input id="edit_form-myEpisodes_1" name="edit_form-myEpisodes_1" placeholder="1-24" type="text" value="400">' in page)
        self.assertTrue('<input id="edit_form-myEpisodes_2" name="edit_form-myEpisodes_2" placeholder="1-74" type="text" value="600">' in page)

    def test_start_valid_date(self):
        """Test update start date"""
        self.login()
        self.navigate_to('/update_anime')

        s0 = self.submit_to('/update_anime', VALID_FORM_DATA)
        print(s0.data)
        print(type(s0))
        print(dir(s0))

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
#        self.assertEqual(s0._status_code, 200)
        self.assertNotIn('01/20/91', page)

    def test_end_invalid_date(self):
        """Test update invalid end date"""
        self.login()
        self.navigate_to('/update_anime')

        s0 = self.submit_to('/update_anime', INVALID_FORM_DATA)


        page = self.navigate_to('/updateanime').data.decode('utf-8')

        self.logout()
#        self.assertEqual(s0._status_code, 200)
        self.assertNotIn('3/4/15', page)

    def test_start_valid_end_invalid_date(self):
        """Test update invalid end date"""
        self.login()
        self.navigate_to('/update_anime')

        s0 = self.submit_to('/update_anime', VALID_INVALID_FORM_DATA)


        page = self.navigate_to('/updateanime').data.decode('utf-8')

        self.logout()
#        self.assertEqual(s0._status_code, 200)
#        self.assertIn('01/20/2001', page)
        self.assertNotIn('555555', page)

if __name__ == '__main__':
    unittest.main()