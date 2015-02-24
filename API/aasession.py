import json
import urllib.request as ureq
import codecs

AA_STATUS = [
    'Not aired',
    'Airing',
    'Finished Airing',
    # 'Not published',
    # 'Publishing',
    # 'Finished Publishing'
]

AA_TYPE = [
    'TV',
    'Movie',
    'OVA',
    'Special',
    'ONA',
    'Music',
    # 'Doujin',
    # 'Manhwa',
    # 'Manhua',
    # 'Novel',
    # 'One Shot',
    # 'Manga'
]

AA_GENRE = [
    'Action',
    'Adventure',
    'Cars',
    'Comedy',
    'Dementia',
    'Demons',
    'Doujinshi',
    'Drama',
    'Ecchi',
    'Fantasy',
    'Game',
    'Gender Bender',
    'Harem',
    'Hentai',
    'Historical',
    'Horror',
    'Josei',
    'Kids',
    'Magic',
    'Martial Arts',
    'Mecha',
    'Military',
    'Music',
    'Mystery',
    'Parody',
    'Police',
    'Psychological',
    'Romance',
    'Samurai',
    'School',
    'Sci-Fi',
    'Seinen',
    'Shoujo',
    'Shoujo Ai',
    'Shounen',
    'Shounen Ai',
    'Slice of Life',
    'Space',
    'Sports',
    'Super Power',
    'Supernatural',
    'Thriller',
    'Vampire',
    'Yaoi',
    'Yuri'
]

AA_FIELD = {
    'count': int,
    # '_id': str,
    'image': str,
    'title': str,
    'related': str,     # probably list
    'aired_from': int,  # unix timestamp
    'aired_to': int,
    'volumes': int,
    'chapters': int,
    'episodes': int,
    'length': int,
    'duration': int,
    'genres': str,      # list genres
    'producers': str,   # list producers
    'authors': str,     # list authors
    'serialization': str,
    'weight': float,
    'avg': float,
    'members_score': float,
    'members': float,
    'scores': float,
    'status': str,
    'resource_uri': str
}

AA_FIELD_TO_TYPE = {
    # 'count': int,
    '_id.i': (int, int),
    '_id.t': str,
    # 'image': str,
    'title': str,
    # 'related': str,     # probably list
    'aired_from': (int, int),  # unix timestamp
    'aired_to': (int, int),
    # 'volumes': int,
    # 'chapters': int,
    'episodes': (int, int),
    # 'length': int,
    'duration': (int, int),
    'genres': (str, str),   # list genres
    # 'producers': str,   # list producers
    # 'authors': str,     # list authors
    # 'serialization': str,
    # 'weight': float,
    # 'avg': float,
    'members_score': (float, float),
    'members': (int, int),
    # 'scores': float,
    'status': str,
    # 'resource_uri': str
}


def idifilter(bounds):
    '''MAL anime ID filter'''
    begin, end = bounds
    return '{{"_id.i":{{"$gte":{},"$lte":{}}}}}'.format(begin, end)


def idtfilter(types):
    '''Medium type (manga/anime) filter'''
    types = list(filter(lambda x: x in AA_TYPE, types.split('`')))
    return '{{"_id.t":{{"$in":{}}}}}'.format(json.dumps(types, separators=(',', ':')))


def titlefilter(keyword):
    '''Title keyword filter'''
    return'{{"title":{{"$regex":"(?=.*{})","$options":"i"}}}}'.format(keyword)


def airedfromfilter(bounds):
    '''Bounds starting air date'''
    begin, end = bounds
    return '{{"aired_from":{{"$gte":{},"$lt":{}}}}}'.format(begin, end)


def airedtofilter(bounds):
    '''Bounds ending air date'''
    begin, end = bounds
    return '{{"aired_to":{{"$gte":{},"$lt":{}}}}}'.format(begin, end)


def episodesfilter(bounds):
    '''Bounds total number of episodes (ignore long-running, still airing ones)'''
    begin, end = bounds
    return '{{"episodes":{{"$gte":{},"$lte":{}}}}}'.format(begin, end)


def durationfilter(bounds):
    '''Bounds length of each episode'''
    begin, end = bounds
    return '{{"duration":{{"$gte":{},"$lte":{}}}}}'.format(begin, end)


def genrefilter(pairs):
    '''May want to update later for logical and over all genres'''
    include, exclude = pairs
    include = list(filter(lambda x: x in AA_GENRE, include.split('`')))
    exclude = list(filter(lambda x: x in AA_GENRE, exclude.split('`')))
    exclude = list(filter(lambda x: x not in include, exclude))
    return '{{"genres":{{"$in":{},"$nin":{}}}}}'\
           .format(json.dumps(include, separators=(',', ':')), json.dumps(exclude, separators=(',', ':')))


def malscorefilter(bounds):
    '''Bounds MAL average score'''
    begin, end = bounds
    return '{{"members_score":{{"$gte":{},"$lte":{}}}}}'.format(begin, end)


def membersfilter(bounds):
    '''Bounds number of members who have watched this anime'''
    begin, end = bounds
    return '{{"members":{{"$gte":{},"$lte":{}}}}}'.format(begin, end)


def statusfilter(statuses):
    '''Staus filter (airing, finished, not yet released)'''
    statuses = list(filter(lambda x: x in AA_STATUS, statuses.split('`')))
    return '{{"status":{{"$in":{}}}}}'.format(json.dumps(statuses, separators=(',', ':')))


AA_FIELD_TO_QUERY = {
    '_id.i': idifilter,
    '_id.t': idtfilter,
    'title': titlefilter,
    'aired_from': airedfromfilter,  # unix timestamp
    'aired_to': airedtofilter,
    'episodes': episodesfilter,
    'duration': durationfilter,
    'genres': genrefilter,   # list genres
    'members_score': malscorefilter,
    'members': membersfilter,
    'status': statusfilter,
}


def fieldfilters(filters):
    '''Generate JSON list of filters to apply to query'''
    output = []
    for f in filters:
        if f in AA_FIELD_TO_QUERY:
            output.append(AA_FIELD_TO_QUERY[f](filters[f]))
    return '{{"$and":[{}]}}'.format(','.join(output))


def returncolumns(columns):
    '''Generate JSON list of columns to be returned from query'''
    columns = filter(lambda x: x in AA_FIELD, columns)
    return '[{}]'.format(','.join('"{}"'.format(w) for w in columns))


class AaSession:
    def search(self, params):
        '''Search through AA with the following parameters'''
        url = 'http://test.animeadvice.me/api/v1/animelist/?filters={}&fields={}&sort={}&limit={}&offset='\
            .format(
                fieldfilters(params['filters']),
                returncolumns(params['fields']),
                '[["{:s}",{:d}]]'.format(params['sort_col'], params['sort_dir']),
                str(params['result_count'])
            )
        url += str(0)

        response = ureq.urlopen(url)
        reader = codecs.getreader("utf-8")
        data = json.load(reader(response))
        with open('data.txt', 'wt') as out:
            json.dump(data, out, indent=4, separators=(',', ': '))
        return True

if __name__ == '__main__':
    '''Turn these into unittests later'''
    print(idifilter((1, 1000)))
    print(idtfilter('TV`Movie`OVA`Manga'))
    print(titlefilter('Conan'))
    print(airedfromfilter((1326168599, 1426168599)))
    print(airedtofilter((1326168599, 1426168599)))
    print(episodesfilter((10, 20)))
    print(durationfilter((23, 45)))
    print(genrefilter(('Music`Mystery`Parody`Hope', 'Police`Mystery`Parody`Hope')))
    print(statusfilter('Not aired`Airing`Finished Airing`Not published'))
    print(malscorefilter((5.0, 6.0)))
    print(membersfilter((1000, 10000)))

    filters = {
        '_id.i': (1, 10000),
        '_id.t': 'TV`Movie`OVA`Special`ONA`Music',
        'title': 'Conan',
        'genres': ('Mystery`Police`Hope', 'Police`Music`Parody`Hope')
    }
    fields = ['title', 'aired_to', 'aired_from', 'death']

    print(fieldfilters(filters))
    print(returncolumns(fields))

    session = AaSession()
    print(session.search({
        'filters': filters,
        'fields': fields,
        'sort_col': 'aired_to',
        'sort_dir': -1,
        'result_count': 30
    }))