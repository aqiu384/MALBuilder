class AaEntry():

    def __init__(self, malid, title):
        self.malid = int(malid)
        self.title = title
        # Add more later if necessary

class AaSession:
    QUERY_INPUTS = {
        # Place the correct inputs in here later
        'AIREDFROM': 'aired_from',
        'AIREDTO': 'aired_to',
        'VOLUMES': 'volumes',
        'CHAPTERS': 'chapters',
        'EPISODES': 'episodes',
        'LENGTH': 'length',
    }

    QUERY_OUTPUTS = {
        'COUNT': 'count',
        'IDI': 'id.i',
        'IDT': 'id.t',
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

    def searchanime(self, sparams, rparams):
        results = []
        results.append(AaEntry(1, 'Cowboy Bebop'))
        results.append(AaEntry(2, 'Berserk'))
        return results