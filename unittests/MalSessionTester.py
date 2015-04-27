import unittest
import unittests.BaseMalbTester as BT
import src.malsession as malsession


class MalSessionTest(unittest.TestCase):
    """Test base functionality offered in MAL transaction layer"""
    def tearDown(self):
        BT.init_test_mal()

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
        expected = BT.COWBOY_BEBOP
        self.assertEqual(int(result.malId), expected.malId)
        self.assertEqual(int(result.myEpisodes), expected.myEpisodes)
        self.assertEqual(float(result.myScore), expected.myScore)
        self.assertEqual(int(result.myStatus), expected.myStatus)

        result = results[1]
        expected = BT.TRIGUN
        self.assertEqual(int(result.malId), expected.malId)
        self.assertEqual(int(result.myEpisodes), expected.myEpisodes)
        self.assertEqual(float(result.myScore), expected.myScore)
        self.assertEqual(int(result.myStatus), expected.myStatus)

        result = results[2]
        expected = BT.HONEY_AND_CLOVER
        self.assertEqual(int(result.malId), expected.malId)
        self.assertEqual(int(result.myEpisodes), expected.myEpisodes)
        self.assertEqual(float(result.myScore), expected.myScore)
        self.assertEqual(int(result.myStatus), expected.myStatus)

        result = results[3]
        expected = BT.MONSTER
        self.assertEqual(int(result.malId), expected.malId)
        self.assertEqual(int(result.myEpisodes), expected.myEpisodes)
        self.assertEqual(float(result.myScore), expected.myScore)
        self.assertEqual(int(result.myStatus), expected.myStatus)

        result = results[4]
        expected = BT.NARUTO
        self.assertEqual(int(result.malId), expected.malId)
        self.assertEqual(int(result.myEpisodes), expected.myEpisodes)
        self.assertEqual(float(result.myScore), expected.myScore)
        self.assertEqual(int(result.myStatus), expected.myStatus)

    def test_add_mal(self):
        malsession.add(BT.TEST_MALKEY, 90, {'myStatus': 1})
        malsession.add(BT.TEST_MALKEY, 91, {'myStatus': 1})
        malsession.add(BT.TEST_MALKEY, 92, {'myStatus': 1})

        mylist = malsession.get_mal_ids(BT.TEST_USERNAME, BT.TEST_MALKEY)
        self.assertIn('90', mylist)
        self.assertIn('91', mylist)
        self.assertIn('92', mylist)

    def test_delete_mal(self):
        malsession.delete(BT.TEST_MALKEY, BT.COWBOY_BEBOP.malId)
        malsession.delete(BT.TEST_MALKEY, BT.HONEY_AND_CLOVER.malId)
        malsession.delete(BT.TEST_MALKEY, BT.TRIGUN.malId)

        mylist = malsession.get_mal_ids(BT.TEST_USERNAME, BT.TEST_MALKEY)
        self.assertNotIn(BT.COWBOY_BEBOP.malId, mylist)
        self.assertNotIn(BT.HONEY_AND_CLOVER.malId, mylist)
        self.assertNotIn(BT.TRIGUN.malId, mylist)

    def test_update_mal(self):
        malsession.update(BT.TEST_MALKEY, BT.COWBOY_BEBOP.malId, {'myScore': 1})
        malsession.update(BT.TEST_MALKEY, BT.HONEY_AND_CLOVER.malId, {'myScore': 2})
        malsession.update(BT.TEST_MALKEY, BT.TRIGUN.malId, {'myScore': 3})

        mylist = [x.myScore for x in malsession.get_mal(BT.TEST_USERNAME, BT.TEST_MALKEY)]

        self.assertIn(1, mylist)
        self.assertIn(2, mylist)
        self.assertIn(3, mylist)






