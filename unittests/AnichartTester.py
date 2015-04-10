import unittest

from unittests import BaseMalbTester


SPRING_2002_DATA = {
    'my_form-startDateStart': 2002,
    'my_form-submit': 'test',
    'my_form-season': 'Spring'
}

SUMMER_2002_DATA = {
    'my_form-startDateStart': 2002,
    'my_form-submit': 'test',
    'my_form-season': 'Summer'
}

FALL_2002_DATA = {
    'my_form-startDateStart': 2002,
    'my_form-submit': 'test',
    'my_form-season': 'Fall'
}

WINTER_2002_DATA = {
    'my_form-startDateStart': 2002,
    'my_form-submit': 'test',
    'my_form-season': 'Winter'
}

BAD_DATA = {
    'my_form-startDateStart': 9999,
    'my_form-submit': 'test',
    'my_form-season': 'Not a Season'
}


class AnichartTest(BaseMalbTester.BaseMalbTest):
    # test_update_through_backend(self):
    #   pass

    def test_anichart_fall(self):
        """Test anichart functionality through frontend"""
        # Login
        response = self.login()
        self.assertTrue('Filter' in response.data.decode('utf-8'))

        # Go to "Anichart" page
        response = self.navigate_to('/anichart')
        self.assertTrue('season' in response.data.decode('utf-8'))

        # Fill out form and submit (Naruto is already on test list of anime)
        response = self.submit_to('/anichart', FALL_2002_DATA)
        self.assertTrue('Naruto' not in response.data.decode('utf-8'))

        # Logout
        response = self.logout()
        self.assertTrue('Please' in response.data.decode('utf-8'))

    def test_anichart_spring(self):
        """Test anichart functionality through frontend"""
        # Login
        response = self.login()
        self.assertTrue('Filter' in response.data.decode('utf-8'))

        # Go to "Anichart" page
        response = self.navigate_to('/anichart')
        self.assertTrue('season' in response.data.decode('utf-8'))

        # Fill out form and submit
        response = self.submit_to('/anichart', SPRING_2002_DATA)
        self.assertTrue('Tokyo Underground' in response.data.decode('utf-8'))

        # Logout
        response = self.logout()
        self.assertTrue('Please' in response.data.decode('utf-8'))

    def test_anichart_summer(self):
        """Test anichart functionality through frontend"""
        # Login
        response = self.login()
        self.assertTrue('Filter' in response.data.decode('utf-8'))

        # Go to "Anichart" page
        response = self.navigate_to('/anichart')
        self.assertTrue('season' in response.data.decode('utf-8'))

        # Fill out form and submit
        response = self.submit_to('/anichart', SUMMER_2002_DATA)
        self.assertTrue('Witch Hunter Robin' in response.data.decode('utf-8'))

        # Logout
        response = self.logout()
        self.assertTrue('Please' in response.data.decode('utf-8'))

    def test_anichart_winter(self):
        """Test anichart functionality through frontend"""
        # Login
        response = self.login()
        self.assertTrue('Filter' in response.data.decode('utf-8'))

        # Go to "Anichart" page
        response = self.navigate_to('/anichart')
        self.assertTrue('season' in response.data.decode('utf-8'))

        # Fill out form and submit
        response = self.submit_to('/anichart', WINTER_2002_DATA)
        self.assertTrue('Full Metal Panic!' in response.data.decode('utf-8'))

        # Logout
        response = self.logout()
        self.assertTrue('Please' in response.data.decode('utf-8'))

    def test_anichart_bad_data(self):
        """Test anichart functionality through frontend"""
        # Login
        response = self.login()
        self.assertTrue('Filter' in response.data.decode('utf-8'))

        # Go to "Anichart" page
        response = self.navigate_to('/anichart')
        self.assertTrue('season' in response.data.decode('utf-8'))

        # Fill out form and submit
        response = self.submit_to('/anichart', BAD_DATA)
        self.assertTrue('No results' in response.data.decode('utf-8'))

        # Logout
        response = self.logout()
        self.assertTrue('Please' in response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()