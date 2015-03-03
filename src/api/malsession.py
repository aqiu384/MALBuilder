import urllib.parse as upar
import urllib.request as ureq
import urllib.error as uerror
import io
import gzip
import base64
from xml.etree import ElementTree as ET


class MalAuthError(Exception):
    pass


class MalDefaultError(Exception):
    pass


SENDERRORS = {
    401: MalAuthError("MAL Authentication failed.")
}


def send_mal(url, data, mal_key):
    """Send query to MAL"""
    if data:
        data = upar.urlencode(data).encode('utf-8')

    headers = {
        'Host': 'myanimelist.net',
        'Accept': 'text/xml, text/*',
        'Accept-Charset': 'utf-8',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'api-taiga-32864c09ef538453b4d8110734ee355b',
        'Authorization': 'Basic {}'.format(mal_key)
    }

    my_bytes = ureq.urlopen(ureq.Request(url, data, headers)).read()
    return gzip.GzipFile(fileobj=io.BytesIO(my_bytes), mode='rb')


def authenticate(username, password):
    """Authenticate user with password through MAL credentials"""
    mal_key = base64.b64encode(bytes('{}:{}'.format(username, password), 'utf-8')).decode('utf-8')
    result = {'username': username}

    try:
        url = 'http://myanimelist.net/api/account/verify_credentials.xml'
        doc = ET.parse(send_mal(url, None, mal_key))
        result['malId'] = int(doc.find('id').text)
        result['malKey'] = mal_key
    except uerror.HTTPError as e:
        pass

    return result


def get_mal(username, mal_key):
    """Download a user's MAL from the MyAnimeList website"""
    url = 'http://myanimelist.net/malappinfo.php?u={}&status=all&type=anime'.format(username)
    try:
        doc = ET.parse(send_mal(url, None, mal_key))
        return doc.getroot()
    except uerror.HTTPError as e:
        raise MalDefaultError('Get MAL transaction failed')


def add(mal_key, anime_id, watch_status):
    """Add the given anime by ID to the user's MAL with the following watch status"""
    url = 'http://myanimelist.net/api/animelist/add/{}.xml'.format(anime_id)
    data = '<?xml version="1.0" encoding="UTF-8"?><entry><status>{}</status></entry>'\
        .format(watch_status)
    try:
        doc = send_mal(url, {'data': data}, mal_key).read().decode('utf-8')
        return 'Created' in doc
    except uerror.HTTPError as e:
        if e.code == 501:
            raise MalDefaultError('Title already exists')
        else:
            raise MalDefaultError('Add transaction failed')


MAL_UPDATES = [
    'my_watched_episodes',
    'my_start_date',
    'my_finish_date',
    'my_score',
    'my_status',
    'my_rewatching',
    'my_rewatching_ep',
]


def update(mal_key, anime_id, entries):
    """Update the given anime with the following entry values"""
    url = 'http://myanimelist.net/api/animelist/update/{}.xml'.format(anime_id)
    data = '<?xml version="1.0" encoding="UTF-8"?><entry>'

    for key in entries:
        if key in MAL_UPDATES:
            data += '<{}>{}</{}>'.format(key, str(entries[key]), key)
    data += '</entry>'

    try:
        doc = send_mal(url, {'data': data}, mal_key).read().decode('utf-8')
        return 'Updated' in doc
    except uerror.HTTPError as e:
        raise MalDefaultError('Update transaction failed')


def delete(mal_key, anime_id):
    """Delete the given anime by ID from the user's MAL"""
    url = 'http://myanimelist.net/api/animelist/delete/{}.xml'.format(anime_id)
    try:
        doc = send_mal(url, None, mal_key).read().decode('utf-8')
        return 'Deleted' in doc
    except uerror.HTTPError as e:
        raise MalDefaultError('Delete transaction failed')