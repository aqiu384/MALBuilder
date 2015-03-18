import urllib.parse as upar
import urllib.request as ureq
import urllib.error as uerror
import io
import gzip
import base64
from xml.etree import ElementTree as ET
from src.models import UserToAnime
from datetime import datetime


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


def parse_mal_date(my_date):
    """Parse MAL date"""
    if my_date == '0000-00-00':
        return None
    return datetime.strptime(my_date, "%Y-%m-%d").date()


def parse_mal_entry(user_id, anime):
    """Parses an MAL anime entry into DB user format"""
    anime_id = anime.find('series_animedb_id').text
    utoa = UserToAnime(user_id, anime_id)

    utoa.myId = int(anime.find('my_id').text)
    utoa.myEpisodes = int(anime.find('my_watched_episodes').text)
    utoa.myStartDate = parse_mal_date(anime.find('my_start_date').text)
    utoa.myEndDate = parse_mal_date(anime.find('my_finish_date').text)
    utoa.myScore = float(anime.find('my_score').text)
    utoa.myStatus = int(anime.find('my_status').text)
    utoa.myRewatching = anime.find('my_rewatching').text is 1
    utoa.myRewatchEps = int(anime.find('my_rewatching_ep').text)
    utoa.myLastUpdate = datetime.fromtimestamp(int(anime.find('my_last_updated').text)).date()

    return utoa


def get_mal(username, mal_key):
    """Download a user's MAL from the MyAnimeList website"""
    url = 'http://myanimelist.net/malappinfo.php?u={}&status=all&type=anime'.format(username)

    try:
        tree = ET.parse(send_mal(url, None, mal_key)).getroot()
    except uerror.HTTPError as e:
        raise MalDefaultError('Get MAL transaction failed')

    utoa_list = []
    user_id = tree.find('myinfo').find('user_id').text

    for anime in tree.findall('anime'):
        utoa_list.append(parse_mal_entry(user_id, anime))

    return utoa_list


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