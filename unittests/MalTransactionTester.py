import unittest

from unittests import BaseMalbTester
from src import app
from src.malsession import delete_all_by_id


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

RESTORE_DEFAULT_ADD = [
    299,
    48,
    298
]


class MalTransactionTest(BaseMalbTester.BaseMalbTest):
    def setUp(self):
        app.config['MAL_TRANSACTIONS_ENABLED'] = True
        self.setUpHelper()

    def test_valid_update_transaction(self):
        """Test update transaction complete on MyAnimeList"""
        # Login
        self.login()
        self.navigate_to('/updateanime')
        self.submit_to('/updateanime', VALID_UPDATE)
        self.navigate_to('/sync')
        self.logout()
        self.login()

        page = self.navigate_to('/updateanime').data.decode('utf-8')

        self.assertTrue('<option selected value="8">' in page)
        self.assertTrue('My Episodes Watched: 1' in page)

        self.submit_to('/updateanime', ORIGINAL_UPDATE_DATA)

    def test_invalid_update_transaction(self):
        """Invalid update does not propagate to MyAnimeList"""
        self.login()
        self.navigate_to('/updateanime')
        self.submit_to('/updateanime', INVALID_UPDATE)
        self.navigate_to('/sync')
        self.logout()
        self.login()

        page = self.navigate_to('/updateanime').data.decode('utf-8')
        print(page)

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

        self.assertTrue('.hack//Liminality' in page)
        self.assertTrue('.hack//Sign' in page)
        self.assertTrue('.hack//Tasogare no Udewa Densetsu' in page)

        delete_all_by_id('cXVldHphbGNvYXRsMzg0OnBhc3N3b3Jk', RESTORE_DEFAULT_ADD)

if __name__ == '__main__':
    unittest.main()