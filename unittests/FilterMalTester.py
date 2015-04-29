import unittest

from unittests import BaseMalbTester


TITLE_DATA = {
    'my_form-fields': ['engTitle', 'startDate'],
    'my_form-submit': 'test',
    'my_form-title': 'Monster'
}

STATUS_DATA = {
    'my_form-fields': ['engTitle', 'startDate'],
    'my_form-submit': 'test',
    'my_form-myStatus': ['2']
}

INCLUDE_GENRE_DATA = {
    'my_form-fields': ['engTitle', 'startDate'],
    'my_form-submit': 'test',
    'my_form-genresInclude': ['4', '6']
}

EXCLUDE_GENRE_DATA = {
    'my_form-fields': ['engTitle', 'startDate'],
    'my_form-submit': 'test',
    'my_form-genresInclude': ['4', '6'],
    'my_form-genresExclude': ['5']
}

NO_DATA = {
    'my_form-fields': ['engTitle', 'startDate'],
    'my_form-submit': 'test',
    'my_form-genresInclude': ['5'],
    'my_form-genresExclude': ['5']
}


class FilterMalTest(BaseMalbTester.BaseMalbTest):
    # test_update_through_backend(self):
    #   pass

    def test_filter_title(self):
        """Test filtering mal based on title through frontend"""
        # Login
        response = self.login()
        self.assertTrue('Filter' in response.data.decode('utf-8'))

        # Fill out form and submit
        response = self.submit_to('/', TITLE_DATA)
        self.assertTrue('2004-04-07' in response.data.decode('utf-8'))

        # Logout
        response = self.logout()
        self.assertTrue('Please' in response.data.decode('utf-8'))

    def test_filter_status(self):
        """Test filtering mal based on status through frontend"""
        # Login
        response = self.login()
        self.assertTrue('Filter' in response.data.decode('utf-8'))

        # Fill out form and submit
        response = self.submit_to('/', STATUS_DATA)
        self.assertTrue('1998-04-03' in response.data.decode('utf-8'))

        # Logout
        response = self.logout()
        self.assertTrue('Please' in response.data.decode('utf-8'))

    def test_filter_include_genre(self):
        """Test filtering mal based on including genres through frontend"""
        # Login
        response = self.login()
        self.assertTrue('Filter' in response.data.decode('utf-8'))

        # Fill out form and submit
        response = self.submit_to('/', INCLUDE_GENRE_DATA)
        self.assertTrue('Cowboy Bebop' in response.data.decode('utf-8'))
        self.assertTrue('Trigun' in response.data.decode('utf-8'))

        # Logout
        response = self.logout()
        self.assertTrue('Please' in response.data.decode('utf-8'))

    def test_filter_exclude_genre(self):
        """Test filtering mal based on excluding genres through frontend"""
        # Login
        response = self.login()
        self.assertTrue('Filter' in response.data.decode('utf-8'))

        # Fill out form and submit
        response = self.submit_to('/', EXCLUDE_GENRE_DATA)
        self.assertFalse('Cowboy Bebop' in response.data.decode('utf-8'))
        self.assertTrue('Trigun' in response.data.decode('utf-8'))

        # Logout
        response = self.logout()
        self.assertTrue('Please' in response.data.decode('utf-8'))

    def test_filter_no_data(self):
        """Test filtering mal with bad data through frontend"""
        # Login
        response = self.login()
        self.assertTrue('Filter' in response.data.decode('utf-8'))

        # Fill out form and submit
        response = self.submit_to('/', NO_DATA)
        self.assertFalse('Cowboy Bebop' in response.data.decode('utf-8'))
        self.assertFalse('Trigun' in response.data.decode('utf-8'))

        # Logout
        response = self.logout()
        self.assertTrue('Please' in response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()