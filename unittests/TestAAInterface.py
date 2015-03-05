import unittest
import src.api.aasession as AA
from datetime import date


class testaainterface(unittest.TestCase):
    def test_filters(self):
        output = AA.idifilter({'idiStart': 1, 'idiEnd': 1000})
        self.assertEquals("{\"_id.i\":{\"$gte\":1,\"$lte\":1000}}", output)
        output = AA.idtfilter({'idt': ['TV', 'Movie', 'OVA', 'Manga']})
        self.assertEquals("{\"_id.t\":{\"$in\":[\"TV\",\"Movie\",\"OVA\"]}}", output)
        output = AA.titlefilter({'title': 'Conan'})
        self.assertEquals("{\"title\":{\"$regex\":\"(?=.*Conan)\",\"$options\":\"i\"}}", output)
        output = AA.airedfromfilter({'airedFromStart': date(1990, 1, 1), 'airedFromEnd': date(2010, 1, 1)})
        self.assertEquals("{\"aired_from\":{\"$gte\":631173600,\"$lt\":1262325600}}", output)
        output = AA.airedtofilter({'airedToStart': date(1990, 1, 1), 'airedToEnd': date(2010, 1, 1)})
        self.assertEquals("{\"aired_to\":{\"$gte\":631173600,\"$lt\":1262325600}}", output)
        output = AA.episodesfilter({'episodesStart': 10, 'episodesEnd': 20})
        self.assertEquals("{\"episodes\":{\"$gte\":10,\"$lte\":20}}", output)
        output = AA.durationfilter({'durationStart': 23, 'durationEnd': 45})
        self.assertEquals("{\"duration\":{\"$gte\":23,\"$lte\":45}}", output)
        output = AA.genrefilter({'genresInclude': ['Music', 'Mystery', 'Parody', 'Hope'],
                                 'genresExclude': ['Police', 'Mystery', 'Parody', 'Hope']})
        self.assertEquals("{\"genres\":{\"$in\":[\"Music\",\"Mystery\",\"Parody\"],\"$nin\":[\"Police\"]}}", output)
        output = AA.statusfilter({'statusInclude': ['Not aired', 'Airing', 'Finished Airing', 'Not Done']})
        self.assertEquals("{\"status\":{\"$in\":[\"Not aired\",\"Airing\",\"Finished Airing\"]}}", output)
        output = AA.malscorefilter({'malScoreStart': 5.0, 'malScoreEnd': 6.0})
        self.assertEquals("{\"members_score\":{\"$gte\":5.0,\"$lte\":6.0}}", output)
        output = AA.membersfilter({'membersStart': 1000, 'membersEnd': 10000})
        self.assertEquals("{\"members\":{\"$gte\":1000,\"$lte\":10000}}", output)

        my_filters = {
            'idiStart': 1, 'idiEnd': 99999,
            'idt': ['TV', 'Movie', 'OVA', 'Special', 'ONA', 'Music'],
            'title': 'Conan',
            'genresInclude': ['Mystery', 'Police', 'Hope'], 'genresExclude': ['Police', 'Music', 'Parody', 'Hope'],
        }
        my_fields = ['title', 'aired_to', 'aired_from', 'death']

        output = AA.fieldfilters(my_filters)
        # self.assertEquals("{\"$and\":[{\"_id.i\":{\"$gte\":1,\"$lte\":10000}},{\"_id.t\":{\"$in\":[\"TV\",\"Movie\",\"OVA\",\"Special\",\"ONA\",\"Music\"]}},{\"genres\":{\"$in\":[\"Mystery\",\"Police\"],\"$nin\":[\"Music\",\"Parody\"]}},{\"title\":{\"$regex\":\"(?=.*Conan)\",\"$options\":\"i\"}}]}", output)
        output = AA.returncolumns(my_fields)
        self.assertEquals("\"title\",\"aired_to\",\"aired_from\"", output)

    def test_search(self):
        my_filters = {
            'idiStart': 1, 'idiEnd': 99999,
            'idt': ['TV', 'Movie', 'OVA', 'Special', 'ONA', 'Music'],
            'title': 'Conan',
            'genresInclude': ['Mystery', 'Police', 'Hope'], 'genresExclude': ['Police', 'Music', 'Parody', 'Hope'],
        }
        my_fields = ['title', 'aired_to', 'aired_from', 'death']

        my_query = AA.getquery(my_filters, my_fields, 'aired_to', -1, 30)

        output = AA.search_results(my_query, 0)
        self.assertIsNotNone(output)
        self.assertIn('Detective Conan Movie 19: The Hellfire Sunflowers', output['objects'][0]['title'])
        output = AA.search_results(my_query, 30)
        self.assertIsNotNone(output)
        self.assertIn('Detective Conan Movie 10: Requiem of the Detectives', output['objects'][0]['title'])