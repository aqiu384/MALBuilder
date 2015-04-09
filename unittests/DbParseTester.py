import unittest
import src.malb as MALB

from datetime import date


class TestCase(unittest.TestCase):
    @unittest.skip
    def test_get_malb(self):
        results = MALB.get_malb(4448103. ['title'])
        self.assertEqual(4, len(results))

        self.assertEqual('Neon Genesis Evangelion', results[0][0])
        self.assertEqual('Neon Genesis Evangelion: Death & Rebirth', results[1][0])
        self.assertEqual('One Piece', results[2][0])
        self.assertEqual('Prince of Tennis', results[3][0])

    @unittest.skip
    def test_search_anime(self):
        results = MALB.search_anime({}, ['title'])
        self.assertEquals(300, len(results))
        self.assertEquals('.hack//Liminality', results[0][0])
        self.assertEquals('.hack//Sign', results[1][0])
        self.assertEquals('.hack//Tasogare no Udewa Densetsu', results[2][0])

        results = MALB.search_anime({
            'startDateStart': date(1999, 1, 1),
            'endDateEnd': date(2000, 1, 1)
        }, ['title', 'startDate'], sort_col='startDate')

        self.assertEquals(6, len(results))
        self.assertEquals('Seikai no Monshou', results[0][0])
        self.assertEquals(date(1999, 1, 2), results[0][1])
        self.assertEquals('Rurouni Kenshin: Meiji Kenkaku Romantan - Tsuiokuhen', results[1][0])
        self.assertEquals(date(1999, 2, 20), results[1][1])
        self.assertEquals('Power Stone', results[2][0])
        self.assertEquals(date(1999, 4, 3), results[2][1])

        results = MALB.search_anime({
            'genresInclude': [9],
            'genresExclude': [17]
        }, ['title'])

        self.assertEqual(5, len(results))
        self.assertEqual('Elfen Lied', results[0][0])
        self.assertEqual('Ikkitousen', results[1][0])
        self.assertEqual('Kiddy Grade', results[2][0])
        self.assertEqual('Vandread', results[3][0])
        self.assertEqual('Vandread: The Second Stage', results[4][0])

if __name__ == '__main__':
    unittest.main()