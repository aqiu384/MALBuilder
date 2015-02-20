import json
import urllib.request as ureq
class AaEntry():
    def __init__(self=None,  malid=None,  title=None, data=None):
        self.malid = malid
        self.title = title
        self.data = data
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
        #'IDI': '_id.i',
        #'IDT': '_id.t',
        'ID': "_id",
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
        if "title" not in rparams:
            rparams.append("title")

        url = "http://test.animeadvice.me/api/v1/animelist/?filters={\"$and\":["
        for word in sparams:
            if word == "title":
                url = url + "{\"title\":{\"$regex\":\"(?=.*" + sparams[word] + ")\",\"$options\":\"i\"},"
            else:
                url = url + "{\"" + word + "\":{\"$gte\":" + sparams[word] + ",\"$lte\":" + sparams[word] + "},"
        url = url[:-1]
        url = url + "}]}&fields=["
        for i in range(len(rparams)):
            url = url + "\"" + rparams[i] + "\","
        url = url[:-1]
        url = url + "]&limit=0&query_limit=50&group_limit=100&sort_type=max&format=json"
        data = json.loads(ureq.urlopen(url).read().decode())

        #print(data)
        for entry in data['objects']:
            AAEntryDict = {}
            for field in rparams:
                if entry.get(field)!= None:
                    AAEntryDict[field] = entry[field]
                else:
                    AAEntryDict[field] = "N/A"
            results.append(AaEntry(entry['_id']['i'],entry['title'], AAEntryDict))
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
