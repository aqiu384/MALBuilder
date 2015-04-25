import unittest
import json

from unittests import BaseMalbTester


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


def get_HTML_SCORE_STR(opt):
    if opt in OPTIONS_SCORE.keys():
        return 'My Score: <select class="checkbox-grid1" id="myScore" name="myScore">' + OPTIONS_SCORE[opt]
    else:
        return 'My Score: <select class="checkbox-grid1" id="myScore" name="myScore">' + OPTIONS_SCORE['none']


def get_HTML_STATUS_STR(opt):
    if opt in OPTIONS_STATUS.keys():
        return 'My Status: <select class="checkbox-grid1" id="myStatus" name="myStatus">' + OPTIONS_STATUS[opt]
    else:
        return 'My Status: <select class="checkbox-grid1" id="myStatus" name="myStatus">' + OPTIONS_STATUS['none']

UPDATE_DATA_STATUS = [
    {'malId': BaseMalbTester.COWBOY_BEBOP.malId, 'myStatus': 6},
    {'malId': BaseMalbTester.HONEY_AND_CLOVER.malId, 'myStatus': 4},
    {'malId': BaseMalbTester.MONSTER.malId, 'myStatus': 4}
]

UPDATE_DATA_SCORE = [
    {'malId': BaseMalbTester.COWBOY_BEBOP.malId, 'myStatus': 1, 'myScore': 8},
    {'malId': BaseMalbTester.HONEY_AND_CLOVER.malId, 'myStatus': 1, 'myScore': 1},
    {'malId': BaseMalbTester.MONSTER.malId, 'myStatus': 1, 'myScore': 3}
]

UPDATE_DATA_EPISODE = [
    {'malId': BaseMalbTester.COWBOY_BEBOP.malId, 'myStatus': 1, 'myEpisodes': 2},
    {'malId': BaseMalbTester.HONEY_AND_CLOVER.malId, 'myStatus': 1, 'myEpisodes': 5},
    {'malId': BaseMalbTester.MONSTER.malId, 'myStatus': 1, 'myEpisodes': 48}
]

UPDATE_DATA_INVALID_STATUS = [
    {'malId': BaseMalbTester.COWBOY_BEBOP.malId, 'myStatus': -2},
    {'malId': BaseMalbTester.HONEY_AND_CLOVER.malId, 'myStatus': 5},
    {'malId': BaseMalbTester.MONSTER.malId, 'myStatus': 5}
]

UPDATE_DATA_INVALID_SCORE = [
    {'malId': BaseMalbTester.COWBOY_BEBOP.malId, 'myStatus': 1, 'myScore': 11},
    {'malId': BaseMalbTester.HONEY_AND_CLOVER.malId, 'myStatus': 1, 'myScore': -3},
    {'malId': BaseMalbTester.MONSTER.malId, 'myStatus': 1, 'myScore': 42}
]

UPDATE_DATA_INVALID_EPISODE = [
    {'malId': BaseMalbTester.COWBOY_BEBOP.malId, 'myStatus': 1, 'myEpisodes': -1},
    {'malId': BaseMalbTester.HONEY_AND_CLOVER.malId, 'myStatus': 1, 'myEpisodes': 400},
    {'malId': BaseMalbTester.MONSTER.malId, 'myStatus': 1, 'myEpisodes': 600}
]


class UpdateAnimeTest(BaseMalbTester.BaseMalbTest):
    def test_update_status(self):
        """Test update status functionality through frontend"""
        # Login
        self.login()
        self.navigate_to('/updateanime')

        s0 = self.submit_to('/update_anime', UPDATE_DATA_STATUS[0]).status
        s1 = self.submit_to('/update_anime', UPDATE_DATA_STATUS[1]).status
        s2 = self.submit_to('/update_anime', UPDATE_DATA_STATUS[2]).status

        page = self.navigate_to('/updateanime').data.decode('utf-8')

        self.assertEqual(s0, '200 OK')
        self.assertEqual(s1, '200 OK')
        self.assertEqual(s2, '200 OK')

        self.assertIn('<option selected value="6">', page)
        self.assertIn('<option selected value="4">', page)

    def test_update_score(self):
        """Test update score functionality through frontend"""
        # Login
        self.login()
        self.navigate_to('/updateanime')

        s0 = self.submit_to('/update_anime', UPDATE_DATA_STATUS[0]).status
        s1 = self.submit_to('/update_anime', UPDATE_DATA_STATUS[1]).status
        s2 = self.submit_to('/update_anime', UPDATE_DATA_STATUS[2]).status

        page = self.navigate_to('/updateanime').data.decode('utf-8')

        self.assertEqual(s0, '200 OK')
        self.assertEqual(s1, '200 OK')
        self.assertEqual(s2, '200 OK')

    def test_update_episode(self):
        """Test update episode count functionality through frontend"""
        # Login
        self.login()
        self.navigate_to('/updateanime')

        s0 = self.submit_to('/update_anime', UPDATE_DATA_EPISODE[0]).status
        s1 = self.submit_to('/update_anime', UPDATE_DATA_EPISODE[1]).status
        s2 = self.submit_to('/update_anime', UPDATE_DATA_EPISODE[2]).status

        page = self.navigate_to('/updateanime').data.decode('utf-8')

        self.assertEqual(s0, '200 OK')
        self.assertEqual(s1, '200 OK')
        self.assertEqual(s2, '200 OK')

        self.assertIn('2', page)
        self.assertIn('5', page)
        self.assertIn('48', page)

    def test_update_invalid_status(self):
        """Test update invalid status functionality through frontend"""
        # Login
        self.login()
        self.navigate_to('/updateanime')

        s0 = self.submit_to('/update_anime', UPDATE_DATA_INVALID_STATUS[0]).status
        s1 = self.submit_to('/update_anime', UPDATE_DATA_INVALID_STATUS[1]).status
        s2 = self.submit_to('/update_anime', UPDATE_DATA_INVALID_STATUS[2]).status

        page = self.navigate_to('/updateanime').data.decode('utf-8')

        self.assertEqual(s0, '400 BAD REQUEST')
        self.assertEqual(s1, '400 BAD REQUEST')
        self.assertEqual(s2, '400 BAD REQUEST')

        self.assertIn('<option selected value="2">', page)
        self.assertIn('<option selected value="1">', page)

    def test_update_invalid_score(self):
        """Test update invalid score functionality through frontend"""
        # Login
        self.login()
        self.navigate_to('/updateanime')

        s0 = self.submit_to('/update_anime', UPDATE_DATA_INVALID_SCORE[0]).status
        s1 = self.submit_to('/update_anime', UPDATE_DATA_INVALID_SCORE[1]).status
        s2 = self.submit_to('/update_anime', UPDATE_DATA_INVALID_SCORE[2]).status

        page = self.navigate_to('/updateanime').data.decode('utf-8')

        self.assertEqual(s0, '400 BAD REQUEST')
        self.assertEqual(s1, '400 BAD REQUEST')
        self.assertEqual(s2, '400 BAD REQUEST')

        self.assertIn('<option selected value="10">', page)
        self.assertIn('<option selected value="7">', page)
        self.assertIn('<option selected value="8">', page)

    def test_update_invalid_episode(self):
        """Test update invalid episode functionality through frontend"""
        # Login
        self.login()
        self.navigate_to('/updateanime')

        s0 = self.submit_to('/update_anime', UPDATE_DATA_INVALID_EPISODE[0]).status
        s1 = self.submit_to('/update_anime', UPDATE_DATA_INVALID_EPISODE[1]).status
        s2 = self.submit_to('/update_anime', UPDATE_DATA_INVALID_EPISODE[2]).status

        page = self.navigate_to('/updateanime').data.decode('utf-8')

        self.assertEqual(s0, '400 BAD REQUEST')
        self.assertEqual(s1, '400 BAD REQUEST')
        self.assertEqual(s2, '400 BAD REQUEST')

        self.assertIn('26', page)
        self.assertIn('12', page)
        self.assertIn('35', page)

if __name__ == '__main__':
    unittest.main()