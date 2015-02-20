import requests
from requests.auth import HTTPBasicAuth
from xml.etree import ElementTree
import urllib

proxies = {
    "http": "http://localhost:8000",
    "https": "http://localhost:8000",
}
headers = {
    'User-Agent': 'api-taiga-32864c09ef538453b4d8110734ee355b',
    'Content-Type': 'application/x-www-form-urlencoded'
}

watchStatus = {
    'WATCHING': '1',
    'COMPLETED': '2',
    'ONHOLD': '3',
    'DROPPED': '4',
    'PLANTOWATCH': '6'
}
testusername = 'Bill900'
testpassword = 'testpw'
xml = '<?xml version="1.0" encoding="UTF-8" ?><entry><status>2</status></entry>'
auth = HTTPBasicAuth(testusername, testpassword)

# not xml
searchURL = 'http://myanimelist.net/api/anime/search.xml?q='  #[]
addURL = 'http://myanimelist.net/api/animelist/add/'  #[id].xml
deleteURL = 'http://myanimelist.net/api/animelist/delete/'  #[id].xml
updateURL = 'http://myanimelist.net/api/animelist/update/'  #[id].xml
# no auth needed for ajax
searchAjaxURL = 'http://myanimelist.net/includes/ajax.inc.php?id='
searchAjaxMagicNumber = '&t=64'


class MalSession:
    def __init__(self, username, password):
        self.username = username
        self.password = password

        # Authenticate username with password through MAL
        # if username != password:
        #     raise Exception('Invalid MAL credentials')

    def searchtitle(self, title):
        r = requests.post(searchURL + title, auth=auth, headers=headers)
        print(r.text)
        if (r.text).find(title):
            print("Success!")
        else:
            print("Fail")

            # def searchkey(self, keywords):
            #     try:
            #         if keywords == "":
            #             raise IndexError
            #         keywords = keywords.split(',')
            #         search = ""
            #         for key in keywords:
            #             key = key.strip()
            #             search += key + ','
            #         search = search[:-1]
            #         print('Search for "{}" returned:'.format(search))
            # do searching
            # except(IndexError):
            #     print('Usage: searchkey [keyword(s),]')
            # return ""

    def searchid(self, id):
        r = requests.post(searchAjaxURL + str(id) + searchAjaxMagicNumber, headers=headers)
        print(r.text)

    def encodeStatus(self, status):
        test = {
            "data": {
                "entry": {"status": status}
            }
        }
        return urllib.urlencode(test)

    def add(self, id, status):
        data = self.encodeStatus(status)
        r = requests.post(addURL + str(id) + '.xml', auth=auth, headers=headers, data=data)
        print(r.text)
        if (r.text).find("This anime is already on your list.") != -1:
            print("Failed: This anime is already on your list.")
        elif r.status_code == '201':
            print("Added")

    def update(self, id, metric, status):
        r = requests.post(updateURL + str(id) + '.xml', auth=auth, headers=headers)
        print(r.text)

    def delete(self, id):
        r = requests.post(deleteURL + str(id) + '.xml', auth=auth, headers=headers)
        print(r.text)
        if r.text.find("Deleted"):
            print("Deleted")
        else:
            print("Fail to delete")
