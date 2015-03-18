import unittest
from xml.etree import ElementTree as ET

import src.malsession as malsession
from src.malsession import MalDefaultError


class testmalsession(unittest.TestCase):
    def test_authentication(self):
        session_data = malsession.authenticate('quetzalcoatl384', 'wrongpassword')
        self.assertIn('username', session_data.keys())
        self.assertNotIn('malId', session_data.keys())
        self.assertNotIn('malKey', session_data.keys())
        session_data = malsession.authenticate('wrongusername', 'password')
        self.assertIn('username', session_data.keys())
        self.assertNotIn('malId', session_data.keys())
        self.assertNotIn('malKey', session_data.keys())
        session_data = malsession.authenticate('quetzalcoatl384', 'password')
        self.assertIn('username', session_data.keys())
        self.assertIn('malId', session_data.keys())
        self.assertIn('malKey', session_data.keys())

    @unittest.skip("")
    def test_get_mal(self):
        session_data = malsession.authenticate('quetzalcoatl384', 'password')
        user_data = ET.tostring(malsession.get_mal('quetzalcoatl384',session_data['malKey'])).decode('utf-8')
        self.assertIn('<user_id>4448103</user_id>', user_data)
        self.assertIn('<user_name>quetzalcoatl384</user_name>', user_data)
        self.assertIn('user_watching>', user_data)
        self.assertIn('Neon Genesis Evangelion', user_data)

    def test_remove_and_add(self):
        session_data = malsession.authenticate('quetzalcoatl384', 'password')
        self.assertTrue(malsession.delete(session_data['malKey'], 31))
        # user_data = ET.tostring(malsession.get_mal('quetzalcoatl384',session_data['malKey'])).decode('utf-8')
        # self.assertNotIn('Neon Genesis Evangelion: Death', user_data)
        self.assertTrue(malsession.add(session_data['malKey'], 31, 2))
        #self.assertRaises(MalDefaultError, malsession.delete, session_data['malKey'], 123412341234)
        #self.assertRaises(MalDefaultError, malsession.delete, sessino_data['malKey'], 31)
        session_data = malsession.authenticate('quetzalcoatl384', 'password')
        # user_data = ET.tostring(malsession.get_mal('quetzalcoatl384',session_data['malKey'])).decode('utf-8')
        # self.assertIn('Neon Genesis Evangelion: Death', user_data)
        self.assertRaises(MalDefaultError, malsession.add, session_data['malKey'], 31, 2)
        self.assertRaises(MalDefaultError, malsession.add, session_data['malKey'], 31, 123412341234)





