import urllib.parse as upar
import urllib.request as ureq
import urllib.error as uerror
import io
import gzip
import base64
from xml.etree import ElementTree as ET


def sendmalapi(url, data, headers):
    if data is not None:
        data = upar.urlencode(data).encode('utf-8')
    btes = ureq.urlopen(ureq.Request(url, data, headers)).read()
    return gzip.GzipFile(fileobj=io.BytesIO(btes), mode='rb')


def authenticate(username, password):
    headers = {
        'Host': 'myanimelist.net',
        'Accept': 'text/xml, text/*',
        'Accept-Charset': 'utf-8',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'api-taiga-32864c09ef538453b4d8110734ee355b'
    }

    encoded = base64.b64encode(bytes('{}:{}'.format(username, password), 'utf-8')).decode('utf-8')
    headers['Authorization'] = 'Basic {}'.format(encoded)

    result = {'username': username}

    try:
        url = 'http://myanimelist.net/api/account/verify_credentials.xml'
        doc = ET.parse(sendmalapi(url, None, headers))
        result['malId'] = int(doc.find('id').text)
        result['malKey'] = encoded
    except uerror.HTTPError as e:
        pass

    return result


class MalAuthError(Exception):
    pass


class MalDefaultError(Exception):
    pass


SENDERRORS = {
    401: MalAuthError("MAL Authentication failed.")
}


MAL_UPDATES = [
    'my_watched_episodes',
    'my_start_date',
    'my_finish_date',
    'my_score',
    'my_status',
    'my_rewatching',
    'my_rewatching_ep',
]


class MalSession:
    """Allows an authenticated MAL User to interact with the MAL API"""
    def __init__(self, username, mal_key):
        self.headers = {
            'Host': 'myanimelist.net',
            'Accept': 'text/xml, text/*',
            'Accept-Charset': 'utf-8',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'api-taiga-32864c09ef538453b4d8110734ee355b',
            'Authorization': 'Basic {}'.format(mal_key)
        }
        self.username = username

    def add(self, anime_id, watch_status):
        """Add the given anime by ID to the user's MAL with the following watch status"""
        url = 'http://myanimelist.net/api/animelist/add/{}.xml'.format(anime_id)
        data = '<?xml version="1.0" encoding="UTF-8"?><entry><status>{}</status></entry>'\
            .format(watch_status)
        try:
            doc = sendmalapi(url, {'data': data}, self.headers).read().decode('utf-8')
            return 'Created' in doc
        except uerror.HTTPError as e:
            if e.code == 501:
                raise MalDefaultError('Title already exists')
            else:
                raise MalDefaultError('Add transaction failed')

    def update(self, anime_id, entries):
        """Update the given anime with the following entry values"""
        url = 'http://myanimelist.net/api/animelist/update/{}.xml'.format(anime_id)
        data = '<?xml version="1.0" encoding="UTF-8"?><entry>'

        for key in entries:
            if key in MAL_UPDATES:
                data += '<{}>{}</{}>'.format(key, str(entries[key]), key)
        data += '</entry>'

        try:
            doc = sendmalapi(url, {'data': data}, self.headers).read().decode('utf-8')
            return 'Updated' in doc
        except uerror.HTTPError as e:
            raise MalDefaultError('Update transaction failed')

    def delete(self, animeid):
        """Delete the given anime by ID from the user's MAL"""
        url = 'http://myanimelist.net/api/animelist/delete/{}.xml'.format(animeid)
        try:
            doc = sendmalapi(url, None, self.headers).read().decode('utf-8')
            return 'Deleted' in doc
        except uerror.HTTPError as e:
            raise MalDefaultError('Delete transaction failed')

    def getmal(self):
        """Download a user's MAL from the MyAnimeList website"""
        url = 'http://myanimelist.net/malappinfo.php?u={}&status=all&type=anime'.format(self.username)
        try:
            doc = ET.parse(sendmalapi(url, None, self.headers))
            return doc
        except uerror.HTTPError as e:
            raise MalDefaultError('Get MAL transaction failed')


# if __name__ == '__main__':
#     session = MalSession('quetzalcoatl384', 'password')
#     assert session.delete(12355)
#     assert session.add(12355, 'WATCHING')
#     assert session.update(12355, {'score': 7, 'episode': 10})
#     session.getmal()
#     session.searchkeyword('neon')
#     session.searchanimeid(100)