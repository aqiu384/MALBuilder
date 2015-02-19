import json
import urllib.request as ureq
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
        'TITLE': 'title'
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
        url = "http://test.animeadvice.me/api/v1/animelist/?filters={\"$and\":["
        for word in sparams:
            if word == "title":
                url = url + "{\"title\":{\"$regex\":\"(?=.*" + sparams[word] + ")\",\"$options\":\"i\"},"
            else:
                url = url + "{\"" + word + "\":{\"$gte\":" + sparams[word] + ",\"$lte\":" + sparams[word] + "},"
        url = url[:-1]
        url = url + "}]}&fields=[\"title\"]" + "&limit=0&query_limit=50&group_limit=100&sort_type=max&format=json"
        #print(url)
        data = json.loads(ureq.urlopen(url).read().decode())
        #print(data)
        for entry in data['objects']:
            results.append(AaEntry(entry['_id']['i'],entry['title']))
        return results

    def convertToReadable(self, input):
        input = input.replace("%7B", "{")
        input = input.replace("%22", "\"")
        input = input.replace("%24", "$")
        input = input.replace("%3A", ":")
        input = input.replace("%5B", "[")
        input = input.replace("%7D", "}")
        input = input.replace("%5D", "]")
        input = input.replace("%2C", ",")
        print(input)