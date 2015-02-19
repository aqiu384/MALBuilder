import urllib2 as ureq
# import urllib.request as ureq


class AaEntry():
    def __init__(self, malid, title):
        self.malid = int(malid)
        self.title = title
        # Add more later if necessary


class AaSession():
    def __init__(self, *args, **kwargs):
        self.QUERY_INPUTS = {
            # Place the correct inputs in here later
            'AIREDFROM': 'aired_from',
            'AIREDTO': 'aired_to',
            'VOLUMES': 'volumes',
            # 1-140
            'CHAPTERS': 'chapters',
            # 1-1200
            'EPISODES': 'episodes',
            # 1-1800
            'LENGTH': 'length',
            # 1-40000
        }
        self.QUERY_OUTPUTS = {
            'COUNT': 'count',
            'IDI': '_id.i',
            'IDT': '_id.t',
            'IMAGE': 'image',
            'TITLE': 'title',
            'RELATED': 'related',
            'AIREDFROM': 'aired_from',
            'AIREDTO': 'aired_to',
            'VOLUMES': 'volumes',
            'CHAPTERS': 'chapters',
            'EPISODES': 'episodes',
            'LENGTH': 'length',
            'DURATION': 'duration',
            'GENRES': 'genres',
            'PRODUCERS': 'producers',
            'AUTHORS': 'authors',
            'SERIALIZATION': 'serialization',
            'WEIGHT': 'weight',
            'AVG': 'avg',
            'MEMBERSSCORE': 'members_score',
            'MEMBERS': 'members',
            'SCORES': 'scores',
            'STATUS': 'status'
        }
        pass

    def searchanime(self, sparams, rparams):
        baseURL = 'http://test.animeadvice.me/api/v1/animelist/'
        # filtersURL = '?filters={"$and":[]}'
        # fieldsURL = '&fields=[]'
        tailURL = '&limit=0&query_limit=50&group_limit=100&sort_type=max&skip=50&sort=[["weight",-1]]&group_sort=[["aired_from",1]]'
        # print(ureq.urlopen(ureq.Request(url)).read())

        filters = ""
        for key, val in sparams.items():
            filters += '{"' + key + '":{"$gte":' + val + ',"$lt":' + val + '}},'
        filters = filters[:-1]

        fields = ""
        for metric in rparams:
            fields += '"' + metric + '",'
        fields = fields[:-1]

        if filters == "":
            filtersURL = '?filters={}'
        else:
            filtersURL = '?filters={"$and":[' + filters + ']}'

        if fields == "":
            fields = '"_id.i","title"'
        fieldsURL = '&fields=[' + fields + ']'

        url = baseURL + filtersURL + fieldsURL + tailURL
        print(filters)
        print(url)
        retVal = ureq.urlopen(ureq.Request(url)).read()
        print(retVal)

        results = []
        results.append(AaEntry(1, 'Cowboy Bebop'))
        results.append(AaEntry(2, 'Berserk'))
        return results