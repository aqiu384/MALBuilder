import urllib.parse as upar
import urllib.request as ureq
import urllib.error as uerror
import io
import gzip
import base64
from xml.etree import ElementTree as ET
from html.parser import HTMLParser


MAL_HEADERS = {
    'Host': 'myanimelist.net',
    'Accept': 'text/xml, text/*',
    'Accept-Charset': 'utf-8',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'api-taiga-32864c09ef538453b4d8110734ee355b'
}


def sendmalapi(url, data, headers):
    if data is not None:
        data = upar.urlencode(data).encode('utf-8')
    print('hello')
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

    print('hello')

    encoded = base64.b64encode(bytes('{}:{}'.format(username, password), 'utf-8')).decode('utf-8')
    headers['Authorization'] = 'Basic {}'.format(encoded)

    result = {'username': username}

    try:
        url = 'http://myanimelist.net/api/account/verify_credentials.xml'
        doc = ET.parse(sendmalapi(url, None, headers))
        result['malId'] = int(doc.find('id').text)
    except uerror.HTTPError as e:
        print('we have issues')

    print(result)
    return result


class MalAuthError(Exception):
    pass


class MalDefaultError(Exception):
    pass


SENDERRORS = {
    401: MalAuthError("MAL Authentication failed.")
}

WATCHSTATUS = {
    'WATCHING': '1',
    'COMPLETED': '2',
    'ONHOLD': '3',
    'DROPPED': '4',
    'PLANTOWATCH': '6'
}

MALENTRY = {
    'episode': int,
    'status': int,    # 1/watching, 2/completed, 3/onhold, 4/dropped, 6/plantowatch
    'score': int,
    'downloaded_episodes': int,
    'storage_type': int,  # (will be updated to accomodate strings soon)
    'storage_value': float,
    'times_rewatched': int,
    'rewatch_value': int,
    'date_start': int,   # mmddyyyy
    'date_finish': int,  # mmddyyyy
    'priority': int,
    'enable_discussion': int,     # 1=enable, 0=disable
    'enable_rewatching': int,     # 1=enable, 0=disable
    'comments': str,
    'fansub_group': str,
    'tags': str    # tags separated by commas
}

MALSEARCH = {
    'id': int,
    'title': str,
    'english': str,
    'synonyms': str,
    'episodes': int,
    'score': float,
    'type': str,
    'status': str,
    'start_date': str,  # yyyy-mm-dd
    'end_date': str,    # yyyy-mm-dd
    'synopsis': str,    # escaped with xml chars
    'image': str
}

MALLIST = {
    'series_animedb_id': int,
    'series_title': str,
    'series_synonyms': str,     # semicolon delimited
    'series_type': int,
    'series_episodes': int,     # 0 if not a series
    'series_status': int,       # their status
    'series_start': str,
    'series_end': str,          # 0000-00-00 if ongoing
    'series_image': str,
    'my_id': int,
    'my_watched_episodes': int,
    'my_start_date': str,
    'my_finish_date': str,
    'my_score': int,
    'my_status': int,
    'my_rewatching': int,
    'my_rewatching_ep': int,
    'my_last_updated>': int,    # 1424735818 looks like a timestamp
    'my_tags': str              # comma delimited
}

MALIDSEARCH = {
    1: 'title',
    3: 'description',
    7: 'genres',
    10: 'status',
    13: 'type',
    16: 'episodes',
    19: 'score',
    20: 'raters',
    23: 'ranked',
    26: 'popularity',
    29: 'members',
}

class MalHtmlParser(HTMLParser):
    def __init__(self):
        super(MalHtmlParser, self).__init__()
        self.counter = 0

    def handle_data(self, data):
        if self.counter in MALIDSEARCH:
            output = MALIDSEARCH[self.counter] + ': ' + data
            print(output)
        self.counter += 1


class MalSession:
    '''Represents a user's login session through the MAL api'''
    def __init__(self, username, password):
        self.headers = {
            'Host': 'myanimelist.net',
            'Accept': 'text/xml, text/*',
            'Accept-Charset': 'utf-8',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'api-taiga-32864c09ef538453b4d8110734ee355b'
        }

        encoded = base64.b64encode(bytes('{}:{}'.format(username, password), 'utf-8')).decode('utf-8')
        self.headers['Authorization'] = 'Basic {}'.format(encoded)

        self.username = username
        self.userid = self.authenticate()
        print(self.userid)

    def sendmalapi(self, url, data):
        '''Send query through the main MAL api'''
        if data is not None:
            data = upar.urlencode(data).encode('utf-8')
        btes = ureq.urlopen(ureq.Request(url, data, self.headers)).read()
        return gzip.GzipFile(fileobj=io.BytesIO(btes), mode='rb')

    def authenticate(self):
        '''Authenticate the user's MAL credentials'''
        try:
            url = 'http://myanimelist.net/api/account/verify_credentials.xml'
            doc = ET.parse(self.sendmalapi(url, None))
            return int(doc.find('id').text)
        except uerror.HTTPError as e:
            if e.code == 401:
                raise MalAuthError('MAL Authentication failed')

    def add(self, animeid, watchstatus):
        '''Add the given anime by ID to the user's MAL with the following watch status'''
        url = 'http://myanimelist.net/api/animelist/add/{}.xml'.format(animeid)
        data = '<?xml version="1.0" encoding="UTF-8"?><entry><status>{}</status></entry>'\
            .format(WATCHSTATUS[watchstatus])
        try:
            doc = self.sendmalapi(url, {'data': data}).read().decode('utf-8')
            return 'Created' in doc
        except uerror.HTTPError as e:
            if e.code == 501:
                raise MalDefaultError('Title already exists')
            else:
                raise MalDefaultError('Add transaction failed')

    def update(self, animeid, entries):
        '''Update the given anime with the following entry values'''
        url = 'http://myanimelist.net/api/animelist/update/{}.xml'.format(animeid)
        data = '<?xml version="1.0" encoding="UTF-8"?><entry>'

        for key in entries:
            if key in MALENTRY and isinstance(entries[key], MALENTRY[key]):
                data += '<{}>{}</{}>'.format(key, str(entries[key]), key)
        data += '</entry>'

        try:
            doc = self.sendmalapi(url, {'data': data}).read().decode('utf-8')
            return 'Updated' in doc
        except uerror.HTTPError as e:
            raise MalDefaultError('Update transaction failed')

    def delete(self, animeid):
        '''Delete the given anime by ID from the user's MAL'''
        url = 'http://myanimelist.net/api/animelist/delete/{}.xml'.format(animeid)
        try:
            doc = self.sendmalapi(url, None).read().decode('utf-8')
            return 'Deleted' in doc
        except uerror.HTTPError as e:
            raise MalDefaultError('Delete transaction failed')

    def getmal(self):
        '''Download a user's MAL from the MyAnimeList website'''
        url = 'http://myanimelist.net/malappinfo.php?u={}&status=all&type=anime'.format(self.username)
        try:
            doc = ET.parse(self.sendmalapi(url, None))
            return doc
        except uerror.HTTPError as e:
            raise MalDefaultError('Get MAL transaction failed')

    def searchkeyword(self, keyword):
        '''Gets a list of anime from the MyAnimeList website by keyword'''
        url = 'http://myanimelist.net/api/anime/search.xml?{}'.format(upar.urlencode({'q': keyword}))
        try:
            doc = ET.parse(self.sendmalapi(url, None))
            anime = doc.getElementsByTagName('entry')
            print(len(anime))
        except uerror.HTTPError as e:
            raise MalDefaultError('Search MAL keyword transaction failed')


if __name__ == '__main__':
    session = MalSession('quetzalcoatl384', 'password')
    assert session.delete(12355)
    assert session.add(12355, 'WATCHING')
    assert session.update(12355, {'score': 7, 'episode': 10})
    session.getmal()
    session.searchkeyword('neon')
    session.searchanimeid(100)