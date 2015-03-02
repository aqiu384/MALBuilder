import urllib.request as ureq
import codecs
import json
import time

url = 'http://list.animeadvice.me/api/query/?query={"i":{"fields":["2","11","12","14","15"],"query":[{"parent":10,"fields":[{"fid":"a","or":true,"filter":[1]}],"include":true}]}}&sort=["i",[["11.a",1]]]&limit=30&skip='
offset = 0

# 10338

while offset < 10400:
    with open('aaresults{}.txt'.format(int(offset / 300)), 'a') as my_file:
        response = ureq.urlopen(url + str(offset))
        reader = codecs.getreader("utf-8")
        my_data = json.load(reader(response))
        json.dump(my_data, my_file, sort_keys=True, separators=(',', ':'))
        my_file.write('\n')
    print(offset)
    offset += 30
    time.sleep(5)