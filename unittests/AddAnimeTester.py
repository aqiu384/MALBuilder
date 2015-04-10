import unittest

from unittests import BaseMalbTester

DEFAULT_SEARCH = {

}

START_DATE_SEARCH = {
    'my_form-startDateStart': '01/01/2001',
    'my_form-startDateEnd': '01/01/2002',
    'my_form-fields': [
        'genres',
        'japTitle',
        'engTitle',
        'score',
        'episodes',
        'description',
        'malId',
        'type',
        'endDate',
        'scoreCount',
        'imgLink',
        'members',
        'favorites',
        'title',
        'startDate',
        'status',
        'duration'
    ]
}

DEFAULT_ADD = {
    'add_form-myStatus_0': 1,
    'add_form-myStatus_1': 1,
    'add_form-myStatus_2': 1
}

DEFAULT_ADD_DIFFERENT_STATUSES = {
    'add_form-myStatus_0': 3,
    'add_form-myStatus_1': 4,
    'add_form-myStatus_2': 6
}

START_DATE_ADD = {
    'add_form-myStatus_22': 1,
    'add_form-myStatus_23': 1,
    'add_form-myStatus_24': 1
}

# Do not execute out of app/data!
# fernet frame


class AddAnimeTest(BaseMalbTester.BaseMalbTest):
    """Test combined UC Search Anime and Add Anime functionality"""
    def test_default_search(self):
        """Test default search produces expected results in add format"""
        self.login()
        self.navigate_to('/searchanime')

        page = self.submit_to('/searchanime', DEFAULT_SEARCH).data.decode('utf-8')

        self.assertTrue('<form name="addanime" method="POST" id="addanimeform">' in page, 'Add form not found')
        self.assertEqual(page.count('<div class="well">'), 30, 'Form does not contain 30 anime')

        self.assertTrue('.hack//Liminality' in page, '.hack//Liminality not found in form')
        self.assertTrue('.hack//Sign' in page, '.hack//Sign not found in form')
        self.assertTrue('.hack//Tasogare no Udewa Densetsu' in page,
                        '.hack//Tasogare no Udewa Densetsu not found in form')

        self.assertTrue('Animal Yokochou' in page, 'Animal Yokochou not found in form')
        self.assertTrue('Appleseed (Movie)' in page, 'Appleseed (Movie) not found in form')
        self.assertTrue('Arc the Lad' in page, 'Arc the Lad not found in form')

    def test_start_date_search(self):
        """Test search by start date"""
        self.login()
        self.navigate_to('/searchanime')

        page = self.submit_to('/searchanime', START_DATE_SEARCH).data.decode('utf-8')

        self.assertTrue('<form name="addanime" method="POST" id="addanimeform">' in page, 'Add form not found')
        self.assertEqual(page.count('<div class="well">'), 26, 'Form does not contain 25 anime')

        self.assertTrue('Bakuten Shoot Beyblade' in page, 'Bakuten Shoot Beyblade not found in form')
        self.assertTrue('Comic Party' in page, 'Comic Party not found in form')
        self.assertTrue('Cowboy Bebop: Tengoku no Tobira' in page,
                        'Cowboy Bebop: Tengoku no Tobira not found in form')

        self.assertTrue('Shaman King' in page, 'Shaman King not found in form')
        self.assertTrue('Shin Shirayuki-hime Densetsu Pretear' in page,
                        'Shin Shirayuki-hime Densetsu Pretear not found in form')
        self.assertTrue('Vandread: The Second Stage' in page, 'Vandread: The Second Stage not found in form')

    def test_default_search_and_add(self):
        """Test adding anime from default search results"""
        self.login()
        self.navigate_to('searchanime')
        self.submit_to('/searchanime', DEFAULT_SEARCH).data.decode('utf-8')
        self.submit_to('/addanime', DEFAULT_ADD).data.decode('utf-8')

        page = self.navigate_to('/updateanime').data.decode('utf-8')

        self.assertTrue('.hack//Liminality' in page, '.hack//Liminality not added')
        self.assertTrue('.hack//Sign' in page, '.hack//Sign not added')
        self.assertTrue('.hack//Tasogare no Udewa Densetsu' in page,
                        '.hack//Tasogare no Udewa Densetsu not added')

        self.assertTrue('Animal Yokochou' not in page, 'Animal Yokochou not found in form')
        self.assertTrue('Appleseed (Movie)' not in page, 'Appleseed (Movie) should not have added')
        self.assertTrue('Arc the Lad' not in page, 'Arc the Lad should not have added')

    def test_default_add_with_different_statuses(self):
        """Test adding anime with different watch statuses"""
        self.login()
        self.navigate_to('searchanime')
        self.submit_to('/searchanime', DEFAULT_SEARCH)
        self.submit_to('/addanime', DEFAULT_ADD_DIFFERENT_STATUSES)

        page = self.navigate_to('/updateanime').data.decode('utf-8')

        self.assertTrue('.hack//Liminality' in page, '.hack//Liminality not added')
        self.assertTrue('.hack//Sign' in page, '.hack//Sign not added')
        self.assertTrue('.hack//Tasogare no Udewa Densetsu' in page,
                        '.hack//Tasogare no Udewa Densetsu not added')

        self.assertTrue('On hold' in page, '.hack//Liminality is not On hold')
        self.assertTrue('Dropped' in page, '.hack//Sign is not Dropped')
        self.assertTrue('Plan to watch' in page, '.hack//Tasogare no Udewa Densetsu is not Plan to watch')

    def test_start_date_search_and_add(self):
        """Test adding anime from search by date results"""
        self.login()
        self.navigate_to('/searchanime')
        self.navigate_to('searchanime')
        self.submit_to('/searchanime', START_DATE_SEARCH)
        self.submit_to('/addanime', START_DATE_ADD)

        page = self.navigate_to('/updateanime').data.decode('utf-8')

        self.assertTrue('Bakuten Shoot Beyblade' not in page, 'Bakuten Shoot Beyblade should not have added')
        self.assertTrue('Comic Party' not in page, 'Comic Party should not have added')
        self.assertTrue('Cowboy Bebop: Tengoku no Tobira' not in page,
                        'Cowboy Bebop: Tengoku no Tobira should not have added')

        self.assertTrue('Shaman King' in page, 'Shaman King not added')
        self.assertTrue('Shin Shirayuki-hime Densetsu Pretear' in page,
                        'Shin Shirayuki-hime Densetsu Pretear not added')
        self.assertTrue('Vandread: The Second Stage' in page, 'Vandread: The Second Stage not added')

if __name__ == '__main__':
    unittest.main()