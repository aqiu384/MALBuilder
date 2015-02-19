import urllib2 as ureq
# import urllib.parse as upar
# import urllib.request as ureq
import io
import gzip

# Animestats to get overall member statistics
# Animelist to get actual series information

url = 'http://test.animeadvice.me/api/v1/animestats//?filters={"$and":[{"aired_from":{"$gte":1414994400,"$lt":1435035600}}]}&fields=["aired_from"]&limit=0&query_limit=50&group_limit=100&sort_type=max&skip=50&sort=[["weight",-1]]&group_sort=[["aired_from",1]]'
url2 = 'http://test.animeadvice.me/api/v1/animelist/?filters={"$and":[{"aired_from":{"$gte":1414994400,"$lt":1435035600}}]}&fields=[]&limit=0&query_limit=50&group_limit=100&sort_type=max&skip=50&sort=[["weight",-1]]&group_sort=[["aired_from",1]]'

print(ureq.urlopen(ureq.Request(url)).read())

#http://test.animeadvice.me/api/v1/animelist/?filters={"$and":[{"aired_from":{"$gte":1414994400,"$lt":1435035600}}]}&fields=[]&limit=0&query_limit=50&group_limit=100&sort_type=max&skip=50&sort=[["weight",-1]]&group_sort=[["aired_from",1]]
#http://test.animeadvice.me/api/v1/animelist/?filters={"$and":[{"aired_from":{"$gte":1414994400,"$lt":1435035600}}]}&fields=["count"]&limit=0&query_limit=50&group_limit=100&sort_type=max&skip=50&sort=[["weight",-1]]&group_sort=[["aired_from",1]]

#http://test.animeadvice.me/api/v1/animelist/?filters={"$and":[{"aired_from":{"$gte":1414994400,"$lt":1435035600}}]}&fields=["count","_id.i","_id.t","image","title"]&limit=0&query_limit=50&group_limit=100&sort_type=max&skip=50&sort=[["weight",-1]]&group_sort=[["aired_from",1]]
#http://test.animeadvice.me/api/v1/animelist/?filters={"$and":[{"aired_from":{"$gte":1414994400,"$lt":1435035600}}]}&fields=["related","aired_from","aired_to","volumes","chapters"]&limit=0&query_limit=50&group_limit=100&sort_type=max&skip=50&sort=[["weight",-1]]&group_sort=[["aired_from",1]]
#http://test.animeadvice.me/api/v1/animelist/?filters={"$and":[{"aired_from":{"$gte":1414994400,"$lt":1435035600}}]}&fields=["episodes","length","duration","genres","producers"]&limit=0&query_limit=50&group_limit=100&sort_type=max&skip=50&sort=[["weight",-1]]&group_sort=[["aired_from",1]]
#http://test.animeadvice.me/api/v1/animelist/?filters={"$and":[{"aired_from":{"$gte":1414994400,"$lt":1435035600}}]}&fields=["authors","serialization","weight","avg","members_score"]&limit=0&query_limit=50&group_limit=100&sort_type=max&skip=50&sort=[["weight",-1]]&group_sort=[["aired_from",1]]
#http://test.animeadvice.me/api/v1/animelist/?filters={"$and":[{"aired_from":{"$gte":1414994400,"$lt":1435035600}}]}&fields=["members","scores","status"]&limit=0&query_limit=50&group_limit=100&sort_type=max&skip=50&sort=[["weight",-1]]&group_sort=[["aired_from",1]]