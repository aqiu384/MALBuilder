import unittest
import json
from unittests import BaseMalbTester


def decode_json(s):
    return json.loads(s.data.decode('utf-8'))


def flashcard_submission(result, watched=True):
    ret = {'anime_id': result['malId']}
    if watched:
        ret['status'] = 1
    else:
        ret['status'] = 10
    return ret


POPULARITY_SEARCH = {
    'search_metric': 'members'
}

RATINGS_SEARCH = {
    'search_metric': 'score'
}

INVALID_SEASON_SEARCH = {
    'search_metric': 'season'
}

SEASON_SEARCH = {
    'search_metric': 'season',
    'year': 2000,
    'season': 'Spring'
}


class FlashcardTest(BaseMalbTester.BaseMalbTest):
    """Tests for Anime Flashcards UC"""
    def test_popularity_flashcards(self):
        """Tests searching and adding anime flashcards by popularity"""
        self.login()

        s0 = decode_json(self.submit_to('/add_flashcard', POPULARITY_SEARCH))
        s1 = decode_json(self.submit_to('/add_flashcard', flashcard_submission(s0)))
        s2 = decode_json(self.submit_to('/add_flashcard', flashcard_submission(s1)))
        s3 = decode_json(self.submit_to('/add_flashcard', flashcard_submission(s2)))

        page = self.navigate_to('/updateanime').data.decode('utf-8')

        self.logout()

        self.assertEqual(s0['title'], 'Bleach')
        self.assertEqual(s1['title'], 'Elfen Lied')
        self.assertEqual(s2['title'], 'Fullmetal Alchemist')
        self.assertEqual(s3['title'], 'Neon Genesis Evangelion')

        self.assertIn('Bleach', page)
        self.assertIn('Elfen Lied', page)
        self.assertIn('Fullmetal Alchemist', page)
        self.assertNotIn('Neon Genesis Evangelion', page)

    def test_ratings_flashcards(self):
        """Tests searching and adding anime flashcards by rating"""
        self.login()

        s0 = decode_json(self.submit_to('/add_flashcard', RATINGS_SEARCH))
        s1 = decode_json(self.submit_to('/add_flashcard', flashcard_submission(s0)))
        s2 = decode_json(self.submit_to('/add_flashcard', flashcard_submission(s1)))
        s3 = decode_json(self.submit_to('/add_flashcard', flashcard_submission(s2)))

        page = self.navigate_to('/updateanime').data.decode('utf-8')

        self.logout()

        self.assertEqual(s0['title'], 'Sen to Chihiro no Kamikakushi')
        self.assertEqual(s1['title'], 'Rurouni Kenshin: Meiji Kenkaku Romantan - Tsuiokuhen')
        self.assertEqual(s2['title'], 'Hajime no Ippo')
        self.assertEqual(s3['title'], 'Mononoke Hime')

        self.assertIn('Sen to Chihiro no Kamikakushi', page)
        self.assertIn('Rurouni Kenshin: Meiji Kenkaku Romantan - Tsuiokuhen', page)
        self.assertIn('Hajime no Ippo', page)
        self.assertNotIn('Mononoke Hime', page)

    def test_season_flashcards(self):
        """Tests searching and adding anime flashcards by airing season"""
        self.login()

        e0 = self.submit_to('/add_flashcard', INVALID_SEASON_SEARCH).data.decode('utf-8')
        s0 = decode_json(self.submit_to('/add_flashcard', SEASON_SEARCH))
        s1 = decode_json(self.submit_to('/add_flashcard', flashcard_submission(s0)))
        s2 = decode_json(self.submit_to('/add_flashcard', flashcard_submission(s1)))
        s3 = decode_json(self.submit_to('/add_flashcard', flashcard_submission(s2)))

        page = self.navigate_to('/updateanime').data.decode('utf-8')

        self.logout()

        self.assertIn('<ul class="errors">', e0)
        self.assertEqual(s0['title'], 'FLCL')
        self.assertEqual(s1['title'], 'Gensoumaden Saiyuuki')
        self.assertEqual(s2['title'], 'Ayashi no Ceres')
        self.assertEqual(s3['title'], 'Love Hina')

        self.assertIn('FLCL', page)
        self.assertIn('Gensoumaden Saiyuuki', page)
        self.assertIn('Ayashi no Ceres', page)
        self.assertNotIn('Love Hina', page)

    def test_add_no_flashcards(self):
        """Tests adding flashcards as "Not Watched" does not have any effect"""
        self.login()

        s0 = decode_json(self.submit_to('/add_flashcard', POPULARITY_SEARCH))
        s1 = decode_json(self.submit_to('/add_flashcard', flashcard_submission(s0, False)))
        s2 = decode_json(self.submit_to('/add_flashcard', flashcard_submission(s1, False)))
        s3 = decode_json(self.submit_to('/add_flashcard', flashcard_submission(s2, False)))

        page = self.navigate_to('/updateanime').data.decode('utf-8')

        self.logout()

        self.assertEqual(s0['title'], 'Bleach')
        self.assertEqual(s1['title'], 'Elfen Lied')
        self.assertEqual(s2['title'], 'Fullmetal Alchemist')
        self.assertEqual(s3['title'], 'Neon Genesis Evangelion')

        self.assertNotIn('Bleach', page)
        self.assertNotIn('Elfen Lied', page)
        self.assertNotIn('Fullmetal Alchemist', page)
        self.assertNotIn('Neon Genesis Evangelion', page)

    def test_switch_flashcards(self):
        """Tests switching search criteria while adding flashcards"""
        self.login()

        s0 = decode_json(self.submit_to('/add_flashcard', POPULARITY_SEARCH))
        s1 = decode_json(self.submit_to('/add_flashcard', flashcard_submission(s0)))
        s2 = decode_json(self.submit_to('/add_flashcard', flashcard_submission(s1)))
        s3 = decode_json(self.submit_to('/add_flashcard', RATINGS_SEARCH))
        s4 = decode_json(self.submit_to('/add_flashcard', flashcard_submission(s3)))
        s5 = decode_json(self.submit_to('/add_flashcard', flashcard_submission(s4)))

        page = self.navigate_to('/updateanime').data.decode('utf-8')

        self.logout()

        self.assertEqual(s0['title'], 'Bleach')
        self.assertEqual(s1['title'], 'Elfen Lied')
        self.assertEqual(s2['title'], 'Fullmetal Alchemist')
        self.assertEqual(s3['title'], 'Sen to Chihiro no Kamikakushi')
        self.assertEqual(s4['title'], 'Rurouni Kenshin: Meiji Kenkaku Romantan - Tsuiokuhen')
        self.assertEqual(s5['title'], 'Hajime no Ippo')

        self.assertIn('Bleach', page)
        self.assertIn('Elfen Lied', page)
        self.assertNotIn('Fullmetal Alchemist', page)
        self.assertIn('Sen to Chihiro no Kamikakushi', page)
        self.assertIn('Rurouni Kenshin: Meiji Kenkaku Romantan - Tsuiokuhen', page)
        self.assertNotIn('Hajime no Ippo', page)

if __name__ == '__main__':
    unittest.main()