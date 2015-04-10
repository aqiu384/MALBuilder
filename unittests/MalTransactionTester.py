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

INVALID_ADD = {
    'add_form-myStatus_0': -1
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
        user_data = malsession.get_mal_anime('quetzalcoatl384','cXVldHphbGNvYXRsMzg0OnBhc3N3b3Jk')

        self.assertTrue('.hack//Liminality' in page)
        self.assertTrue('.hack//Sign' in page)
        self.assertTrue('.hack//Tasogare no Udewa Densetsu' in page)

        self.assertIn('299', user_data)
        self.assertIn('48', user_data)
        self.assertIn('298', user_data)

        delete_all_by_id('cXVldHphbGNvYXRsMzg0OnBhc3N3b3Jk', RESTORE_DEFAULT_ADD)

    def test_invalid_status_add_transaction(self):
        """Test invalid add transation completes on MyAnimeList"""
        self.login()
        user_data = malsession.get_mal('quetzalcoatl384','cXVldHphbGNvYXRsMzg0OnBhc3N3b3Jk')

        self.navigate_to('searchanime')
        self.submit_to('/searchanime', DEFAULT_SEARCH)
        self.submit_to('/addanime', INVALID_ADD)

        page = self.navigate_to('/sync').data.decode('utf-8')
        user_data_after = malsession.get_mal('quetzalcoatl384','cXVldHphbGNvYXRsMzg0OnBhc3N3b3Jk')

        self.assertEquals(user_data, user_data_after)
        self.assertFalse('A Kite' in page)

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

    def test_disabled_add(self):
        app.config['MAL_TRANSACTIONS_ENABLED'] = False

        malsession.add('cXVldHphbGNvYXRsMzg0OnBhc3N3b3Jk', '299', 1)
        malsession.add('cXVldHphbGNvYXRsMzg0OnBhc3N3b3Jk', '48', 1)
        malsession.add('cXVldHphbGNvYXRsMzg0OnBhc3N3b3Jk', '298', 1)

        user_data = malsession.get_mal_anime('quetzalcoatl384','cXVldHphbGNvYXRsMzg0OnBhc3N3b3Jk')

        self.assertNotIn('299', user_data)
        self.assertNotIn('48', user_data)
        self.assertNotIn('298', user_data)

        app.config['MAL_TRANSACTIONS_ENABLED'] = True
        #delete_all_by_id('cXVldHphbGNvYXRsMzg0OnBhc3N3b3Jk', RESTORE_DEFAULT_ADD)

    def test_disabled_remove(self):
        app.config['MAL_TRANSACTIONS_ENABLED'] = False

        delete_all_by_id('cXVldHphbGNvYXRsMzg0OnBhc3N3b3Jk', [22])
        user_data = malsession.get_mal_anime('quetzalcoatl384','cXVldHphbGNvYXRsMzg0OnBhc3N3b3Jk')
        self.assertIn('22', user_data)

        app.config['MAL_TRANSACTIONS_ENABLED'] = True
if __name__ == '__main__':
    unittest.main()