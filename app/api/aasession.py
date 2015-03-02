import json
import urllib.request as ureq
import codecs
from time import mktime
from datetime import date, datetime

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


def aadatetotimestamp(d):
    return int(mktime(datetime(d.year, d.month, d.day).timetuple()))


def idifilter(filters):
    '''MAL anime ID filter'''
    if filters.get('idiStart') or filters.get('idiEnd'):
        start = filters.get('idiStart', 0)
        end = filters.get('idiEnd', 99999)
        return '{{"_id.i":{{"$gte":{},"$lte":{}}}}}'.format(start, end)
    return None


def idtfilter(filters):
    '''Medium type (manga/anime) filter'''
    if filters.get('idt'):
        type_list = list(filter(lambda x: x in AA_TYPE, filters['idt']))
        return '{{"_id.t":{{"$in":{}}}}}'.format(json.dumps(type_list, separators=(',', ':')))
    return None


def titlefilter(filters):
    '''Title keyword filter'''
    if filters.get('title'):
        return'{{"title":{{"$regex":"(?=.*{})","$options":"i"}}}}'.format(filters['title'])
    return None


def airedfromfilter(filters):
    '''Bounds starting air date'''
    if filters.get('airedFromStart') or filters.get('airedFromEnd'):
        start = filters.get('airedFromStart', date(1990, 1, 1))
        end = filters.get('airedFromEnd', date(2100, 1, 1))
        return '{{"aired_from":{{"$gte":{},"$lt":{}}}}}'.format(aadatetotimestamp(start), aadatetotimestamp(end))
    return None


def airedtofilter(filters):
    '''Bounds ending air date'''
    if filters.get('airedToStart') or filters.get('airedToEnd'):
        start = filters.get('airedToStart', date(1990, 1, 1))
        end = filters.get('airedToEnd', date(2100, 1, 1))
        return '{{"aired_to":{{"$gte":{},"$lt":{}}}}}'.format(aadatetotimestamp(start), aadatetotimestamp(end))
    return None


def episodesfilter(filters):
    '''Bounds total number of episodes (ignore long-running, still airing ones)'''
    if filters.get('episodesStart') or filters.get('episodesEnd'):
        start = filters.get('episodesStart', 0)
        end = filters.get('episodesEnd', 50000)
        return '{{"episodes":{{"$gte":{},"$lte":{}}}}}'.format(start, end)
    return None


def durationfilter(filters):
    '''Bounds length of each episode'''
    if filters.get('durationStart') or filters.get('durationEnd'):
        start = filters.get('durationStart', 0)
        end = filters.get('durationEnd', 50000)
        return '{{"duration":{{"$gte":{},"$lte":{}}}}}'.format(start, end)
    return None


def genrefilter(filters):
    '''May want to update later for logical and over all genres'''
    if filters.get('genresInclude') or filters.get('genresExclude'):
        include = list(filter(lambda x: x in AA_GENRE, filters.get('genresInclude')))
        exclude = list(filter(lambda x: x in AA_GENRE, filters.get('genresExclude')))
        exclude = list(filter(lambda x: x not in include, exclude))
        return '{{"genres":{{"$in":{},"$nin":{}}}}}'\
            .format(json.dumps(include, separators=(',', ':')), json.dumps(exclude, separators=(',', ':')))
    return None


def malscorefilter(filters):
    '''Bounds MAL average score'''
    if filters.get('malScoreStart') or filters.get('malScoreEnd'):
        start = filters.get('malScoreStart', 0)
        end = filters.get('malScoreEnd', 10)
        return '{{"members_score":{{"$gte":{},"$lte":{}}}}}'.format(start, end)
    return None


def membersfilter(filters):
    '''Bounds number of members who have watched this anime'''
    if filters.get('membersStart') or filters.get('membersEnd'):
        start = filters.get('membersStart', 0)
        end = filters.get('membersEnd', 9999999)
        return '{{"members":{{"$gte":{},"$lte":{}}}}}'.format(start, end)
    return None


def statusfilter(filters):
    '''Staus filter (airing, finished, not yet released)'''
    if filters.get('statusInclude'):
        statuses = list(filter(lambda x: x in AA_STATUS, filters['statusInclude']))
        return '{{"status":{{"$in":{}}}}}'.format(json.dumps(statuses, separators=(',', ':')))
    return None


AA_FILTERS = [
    idifilter,
    idtfilter,
    titlefilter,
    airedfromfilter,
    airedtofilter,
    episodesfilter,
    durationfilter,
    genrefilter,
    malscorefilter,
    membersfilter,
    statusfilter
]


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


def fieldfilters(filter_list):
    '''Generate JSON list of filters to apply to query'''
    output = []
    for f in AA_FILTERS:
        query = f(filter_list)
        if query:
            output.append(query)
    if output:
        return '"$and":[{}]'.format(','.join(output))
    return ''


def returncolumns(columns):
    '''Generate JSON list of columns to be returned from query'''
    columns = filter(lambda x: x in AA_FIELD, columns)
    return ','.join('"{}"'.format(w) for w in columns)


def getquery(filters, fields, sort_col, sort_dir, result_count):
    """Search through AA with the following parameters"""
    return 'http://test.animeadvice.me/api/v1/animelist/?filters={{{}}}&fields=[{}]&sort={}&limit={}&format=json&offset='\
        .format(
            fieldfilters(filters),
            returncolumns(fields),
            '[["{:s}",{:d}]]'.format(sort_col, sort_dir),
            str(result_count)
        )


def search_results(query, offset):
    response = ureq.urlopen(query + str(offset))
    reader = codecs.getreader("utf-8")
    data = json.load(reader(response))
    return data


class AaSession:
    def __init__(self, query, fields, offset):
        self.query = query
        self.fields = fields
        self.offset = offset

    def search_results(self):
        response = ureq.urlopen(self.query + str(self.offset))
        reader = codecs.getreader("utf-8")
        data = json.load(reader(response))
        return data

if __name__ == '__main__':
    '''Turn these into unittests later'''
    print(idifilter({'idiStart': 1, 'idiEnd': 1000}))
    print(idtfilter({'idt': ['TV', 'Movie', 'OVA', 'Manga']}))
    print(titlefilter({'title': 'Conan'}))
    print(airedfromfilter({'airedFromStart': date(1990, 1, 1), 'airedFromEnd': date(2010, 1, 1)}))
    print(airedtofilter({'airedToStart': date(1990, 1, 1), 'airedToEnd': date(2010, 1, 1)}))
    print(episodesfilter({'episodesStart': 10, 'episodesEnd': 20}))
    print(durationfilter({'durationStart': 23, 'durationEnd': 45}))
    print(genrefilter({'genresInclude': ['Music', 'Mystery', 'Parody', 'Hope'],
                       'genresExclude': ['Police', 'Mystery', 'Parody', 'Hope']}))
    print(statusfilter({'statusInclude': ['Not aired', 'Airing', 'Finished Airing', 'Not Done']}))
    print(malscorefilter({'malScoreStart': 5.0, 'malScoreEnd': 6.0}))
    print(membersfilter({'membersStart': 1000, 'membersEnd': 10000}))

    my_filters = {
        'idiStart': 1, 'idiEnd': 99999,
        'idt': ['TV', 'Movie', 'OVA', 'Special', 'ONA', 'Music'],
        'title': 'Conan',
        'genresInclude': ['Mystery', 'Police', 'Hope'], 'genresExclude': ['Police', 'Music', 'Parody', 'Hope'],
    }
    my_fields = ['title', 'aired_to', 'aired_from', 'death']

    print(fieldfilters(my_filters))
    print(returncolumns(my_fields))

    session = AaSession({
        'filters': my_filters,
        'fields': my_fields,
        'sort_col': 'aired_to',
        'sort_dir': -1,
        'result_count': 30
    })

    session.searchresults()
    session.searchresults()