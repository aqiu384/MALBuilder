import unittest
import unittests.BaseMalbTester as BaseTester
import src.malsession as malsession


class MalSessionTest(unittest.TestCase):
    """Test base functionality offered in MAL transaction layer"""
    def test_authentication(self):
        """Test authentication of user through MAL website"""
        session0 = malsession.authenticate('quetzalcoatl384', 'wrongpassword')
        session1 = malsession.authenticate('wrongusername', 'password')
        session2 = malsession.authenticate('quetzalcoatl384', 'password')

        self.assertIn('username', session0.keys())
        self.assertNotIn('malId', session0.keys())
        self.assertNotIn('malKey', session0.keys())

        self.assertIn('username', session1.keys())
        self.assertNotIn('malId', session1.keys())
        self.assertNotIn('malKey', session1.keys())

        self.assertIn('username', session2.keys())
        self.assertIn('malId', session2.keys())
        self.assertIn('malKey', session2.keys())

    def test_get_mal(self):
        """Test retrieval of sample user quetzalcoatl384 MAL from MyAnimeList"""
        session_data = malsession.authenticate('quetzalcoatl384', 'password')
        results = malsession.get_mal('quetzalcoatl384', session_data['malKey'])

        self.assertEqual(len(results), 5, 'quetzalcoatl384 should have 5 anime in list')

        result = results[0]
        expected = BaseTester.COWBOY_BEBOP
        self.assertEqual(int(result.malId), expected.malId)
        self.assertEqual(int(result.myEpisodes), expected.myEpisodes)
        self.assertEqual(float(result.myScore), expected.myScore)
        self.assertEqual(int(result.myStatus), expected.myStatus)

        result = results[1]
        expected = BaseTester.TRIGUN
        self.assertEqual(int(result.malId), expected.malId)
        self.assertEqual(int(result.myEpisodes), expected.myEpisodes)
        self.assertEqual(float(result.myScore), expected.myScore)
        self.assertEqual(int(result.myStatus), expected.myStatus)

        result = results[2]
        expected = BaseTester.HONEY_AND_CLOVER
        self.assertEqual(int(result.malId), expected.malId)
        self.assertEqual(int(result.myEpisodes), expected.myEpisodes)
        self.assertEqual(float(result.myScore), expected.myScore)
        self.assertEqual(int(result.myStatus), expected.myStatus)

        result = results[3]
        expected = BaseTester.MONSTER
        self.assertEqual(int(result.malId), expected.malId)
        self.assertEqual(int(result.myEpisodes), expected.myEpisodes)
        self.assertEqual(float(result.myScore), expected.myScore)
        self.assertEqual(int(result.myStatus), expected.myStatus)

        result = results[4]
        expected = BaseTester.NARUTO
        self.assertEqual(int(result.malId), expected.malId)
        self.assertEqual(int(result.myEpisodes), expected.myEpisodes)
        self.assertEqual(float(result.myScore), expected.myScore)
        self.assertEqual(int(result.myStatus), expected.myStatus)





