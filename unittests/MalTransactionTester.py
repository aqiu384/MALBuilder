import unittest

from unittests import BaseMalbTester
from src import app
from src.malsession import delete_all_by_id

import src.malsession as malsession


VALID_UPDATE = {
    'edit_form-myScore_0': 8,
    'edit_form-myEpisodes_0': 1,
}

INVALID_UPDATE = {
    'edit_form-myScore_0': 11,
    'edit_form-myEpisodes_0': 90001,
}

ORIGINAL_UPDATE_DATA = {
    'edit_form-myScore_0': 0,
    'edit_form-myEpisodes_0': 0,
}

DEFAULT_SEARCH = {

}

DEFAULT_ADD = {
    'add_form-myStatus_0': 1,
    'add_form-myStatus_1': 1,
    'add_form-myStatus_2': 1
}

NOT_WATCHED_ADD = {
    'add_form-myStatus_0': 10,
    'add_form-myStatus_1': 10,
    'add_form-myStatus_2': 10
}

RESTORE_DEFAULT_ADD = [
    299,
    48,
    298,
    285,
    231,
    56
]


class MalTransactionTest(BaseMalbTester.BaseMalbTest):
    def setUp(self):
        app.config['MAL_TRANSACTIONS_ENABLED'] = True
        self.setUpHelper()

    def tearDown(self):
        BaseMalbTester.init_test_mal()

    def test_invalid_update_transaction(self):
        """Invalid update does not propagate to MyAnimeList"""
        self.login()
        self.navigate_to('/updateanime')
        self.submit_to('/updateanime', INVALID_UPDATE)
        self.navigate_to('/sync')
        self.logout()
        self.login()

        page = self.navigate_to('/updateanime').data.decode('utf-8')

        self.assertTrue('<option selected value="11">' not in page)
        self.assertTrue('My Episodes Watched: 9000' not in page)

    def test_default_add_transaction(self):
        """Test default add transaction completes on MyAnimeList"""
        self.login()
        self.navigate_to('searchanime')
        self.submit_to('/searchanime', DEFAULT_SEARCH)
        self.submit_to('/addanime', DEFAULT_ADD)
        self.navigate_to('/sync')
        self.logout()
        self.login()

        page = self.navigate_to('/updateanime').data.decode('utf-8')

        self.assertTrue('.hack//Liminality' in page, '.hack//Liminality not included in MAL transaction')
        self.assertTrue('.hack//Sign' in page, '.hack//Sign not included in MAL transaction')
        self.assertTrue('.hack//Tasogare no Udewa Densetsu' in page,
                        '.hack//Tasogare no Udewa Densetsu not included in MAL transaction')

    def test_not_watched_add_transaction(self):
        """Test entries labeled as Have not Seen are not included in the MAL transaction"""
        self.login()
        self.navigate_to('searchanime')
        self.submit_to('/searchanime', DEFAULT_SEARCH)
        self.submit_to('/addanime', NOT_WATCHED_ADD)
        self.navigate_to('/sync')
        self.logout()
        self.login()

        page = self.navigate_to('/updateanime').data.decode('utf-8')

        self.assertTrue('.hack//Liminality' not in page, '.hack//Liminality should not be included in MAL')
        self.assertTrue('.hack//Sign' not in page, '.hack//Sign should not be included in MAL')
        self.assertTrue('.hack//Tasogare no Udewa Densetsu' not in page,
                        '.hack//Tasogare no Udewa Densetsu should not be included in MAL')

    def test_multiple_default_add_transaction(self):
        """Test subsequent add transactions are also processed my MAL"""
        self.login()
        self.navigate_to('searchanime')
        self.submit_to('/searchanime', DEFAULT_SEARCH)
        self.submit_to('/addanime', DEFAULT_ADD)
        self.submit_to('/addanime', DEFAULT_ADD)
        self.navigate_to('/sync')
        self.logout()
        self.login()

        page = self.navigate_to('/updateanime').data.decode('utf-8')

        self.assertTrue('.hack//Liminality' in page, '.hack//Liminality not included in MAL transaction')
        self.assertTrue('.hack//Sign' in page, '.hack//Sign not included in MAL transaction')
        self.assertTrue('.hack//Tasogare no Udewa Densetsu' in page,
                        '.hack//Tasogare no Udewa Densetsu not included in MAL transaction')

        self.assertTrue('Area 88 (TV)' in page, 'Area 88 (TV) not included in MAL transaction')
        self.assertTrue('Argento Soma' in page, 'Argento Soma not included in MAL transaction')
        self.assertTrue('Asagiri no Miko' in page, 'Asagiri no Miko not included in MAL transaction')

    def test_remove(self):
        self.login()
        self.navigate_to('searchanime')
        self.submit_to('/searchanime', DEFAULT_SEARCH)
        self.submit_to('/addanime', DEFAULT_ADD)
        self.navigate_to('/sync')
        self.logout()
        self.login()

        delete_all_by_id('cXVldHphbGNvYXRsMzg0OnBhc3N3b3Jk', RESTORE_DEFAULT_ADD)
        user_data = malsession.get_mal_anime('quetzalcoatl384','cXVldHphbGNvYXRsMzg0OnBhc3N3b3Jk')

        self.assertNotIn('299', user_data)
        self.assertNotIn('48', user_data)
        self.assertNotIn('298', user_data)

    def test_disabled_remove(self):
        app.config['MAL_TRANSACTIONS_ENABLED'] = False

        delete_all_by_id('cXVldHphbGNvYXRsMzg0OnBhc3N3b3Jk', [1])
        user_data = malsession.get_mal_anime('quetzalcoatl384','cXVldHphbGNvYXRsMzg0OnBhc3N3b3Jk')
        self.assertIn('1', user_data)

        app.config['MAL_TRANSACTIONS_ENABLED'] = True

if __name__ == '__main__':
    unittest.main()