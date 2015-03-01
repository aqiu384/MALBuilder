import unittest
import aasession
import json

from aasession import AaSession
class TestAAInterface(unittest.TestCase):
    def testFilters(self):
        output = aasession.idifilter((1, 1000))
        self.assertEquals("{\"_id.i\":{\"$gte\":1,\"$lte\":1000}}",output)
        output = aasession.idtfilter('TV`Movie`OVA`Manga')
        self.assertEquals("{\"_id.t\":{\"$in\":[\"TV\",\"Movie\",\"OVA\"]}}",output)
        output = aasession.titlefilter('Conan')
        self.assertEquals("{\"title\":{\"$regex\":\"(?=.*Conan)\",\"$options\":\"i\"}}",output)
        output = aasession.airedfromfilter((1326168599, 1426168599))
        self.assertEquals("{\"aired_from\":{\"$gte\":1326168599,\"$lt\":1426168599}}",output)
        output = aasession.airedtofilter((1326168599, 1426168599))
        self.assertEquals("{\"aired_to\":{\"$gte\":1326168599,\"$lt\":1426168599}}",output)
        output = aasession.episodesfilter((10, 20))
        self.assertEquals("{\"episodes\":{\"$gte\":10,\"$lte\":20}}",output)
        output = aasession.durationfilter((23, 45))
        self.assertEquals("{\"duration\":{\"$gte\":23,\"$lte\":45}}",output)
        output = aasession.genrefilter(('Music`Mystery`Parody`Hope', 'Police`Mystery`Parody`Hope'))
        self.assertEquals("{\"genres\":{\"$in\":[\"Music\",\"Mystery\",\"Parody\"],\"$nin\":[\"Police\"]}}",output)
        output = aasession.statusfilter('Not aired`Airing`Finished Airing`Not published')
        self.assertEquals("{\"status\":{\"$in\":[\"Not aired\",\"Airing\",\"Finished Airing\"]}}",output)
        output = aasession.malscorefilter((5.0, 6.0))
        self.assertEquals("{\"members_score\":{\"$gte\":5.0,\"$lte\":6.0}}",output)
        output = aasession.membersfilter((1000, 10000))
        self.assertEquals("{\"members\":{\"$gte\":1000,\"$lte\":10000}}",output)
    
        filters = {
            '_id.i': (1, 10000),
            '_id.t': 'TV`Movie`OVA`Special`ONA`Music',
            'title': 'Conan',
            'genres': ('Mystery`Police`Hope', 'Police`Music`Parody`Hope')
        }
        fields = ['title', 'aired_to', 'aired_from', 'death']
    
        output = aasession.fieldfilters(filters)
        #self.assertEquals("{\"$and\":[{\"_id.i\":{\"$gte\":1,\"$lte\":10000}},{\"_id.t\":{\"$in\":[\"TV\",\"Movie\",\"OVA\",\"Special\",\"ONA\",\"Music\"]}},{\"genres\":{\"$in\":[\"Mystery\",\"Police\"],\"$nin\":[\"Music\",\"Parody\"]}},{\"title\":{\"$regex\":\"(?=.*Conan)\",\"$options\":\"i\"}}]}",output)
        output = aasession.returncolumns(fields)
        self.assertEquals("[\"title\",\"aired_to\",\"aired_from\"]",output)

    def testSearch(self):
        filters = {
            '_id.i': (1, 10000),
            '_id.t': 'TV`Movie`OVA`Special`ONA`Music',
            'title': 'Conan',
            'genres': ('Mystery`Police`Hope', 'Police`Music`Parody`Hope')
        }
        fields = ['title', 'aired_to', 'aired_from', 'death']
        session = AaSession({
            'filters': filters,
            'fields': fields,
            'sort_col': 'aired_to',
            'sort_dir': -1,
            'result_count': 30
        })
        output = session.searchresults()
        self.assertIsNotNone(output)
        self.assertIn('Detective Conan Movie 15: Quarter of Silence', output['objects'][0]['title'])
        output = session.searchresults()
        self.assertIsNotNone(output)
        self.assertIn('Detective Conan Movie 05: Countdown to Heaven', output['objects'][0]['title'])