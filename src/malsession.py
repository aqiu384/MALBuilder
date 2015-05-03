import urllib.parse as upar
import urllib.request as ureq
import urllib.error as uerror
import io
import gzip
import base64
from src import mal_transaction
from xml.etree import ElementTree as ET
from src.models import UserToAnime
from datetime import datetime
from src.constants import MAL_UPDATES


class MalAuthError(Exception):
    """Represents an MAL Authentication error"""
    pass


class MalDefaultError(Exception):
    """Represents an MAL Default error"""
    pass


def send_mal(url, data, mal_key):
    """
    Send query to MAL

    :param url: MyAnimeList URL to post query to
    :param data: Data to append to request
    :param mal_key: MyAnimeList authentication key
    :return: MyAnimeList API response
    """
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
    """
    Authenticate user with password through MAL credentials

    :param username: MyAnimeList username
    :param password: MyAnimeList password
    :return: MyAnimeList authentication result
    """
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
    """
    Parse MAL date

    :param my_date: MyAnimeList date to parse
    :return: Date in MALB format
    """
    if my_date == '0000-00-00':
        return None
    return datetime.strptime(my_date, "%Y-%m-%d").date()


def parse_mal_entry(user_id, anime):
    """
    Parses an MAL anime entry into DB User to Anime format

    :param user_id: MAL User ID
    :param anime: MAL anime entry
    :return: User to Anime representing parsed result
    """
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
    """
    Download a user's MAL from the MyAnimeList website

    :param username: MAL username
    :param mal_key: MyAnimeList authentication key
    :return: User to Anime list containing user's MAL
    """
    url = 'http://myanimelist.net/malappinfo.php?u={}&status=all&type=anime'.format(username)

    try:
        tree = ET.parse(send_mal(url, None, mal_key)).getroot()
    except uerror.HTTPError as e:
        raise MalDefaultError('Get MAL transaction failed')

    utoa_list = []
    user_id = tree.find('myinfo').find('user_id').text

    for anime in tree.findall('anime'):
        entry = parse_mal_entry(user_id, anime)
        utoa_list.append(entry)

    return utoa_list


def get_mal_ids(username, mal_key):
    """
    Download a user's MAL and return a list of anime IDs from the MyAnimeList website

    :param username: MAL username
    :param mal_key: MyAnimeList authentication key
    :return: User to Anime list containing user's MAL IDs
    """
    return [x.malId for x in get_mal(username, mal_key)]


def add_all(mal_key, utoa_list, fields=None):
    """
    Bulk add all anime to MAL

    :param mal_key: MyAnimeList authentication key
    :param utoa_list: Anime to add
    :param fields: Data fields to send in
    :return: None
    """
    if not fields:
        fields = ['malId', 'myStatus']
    for anime in utoa_list:
        add(mal_key, anime.malId, anime.getFields(fields))


@mal_transaction
def add(mal_key, anime_id, entries):
    """
    Add the given anime by ID to the user's MAL with the following data fields

    :param mal_key: MyAnimeList authentication key
    :param anime_id: Anime's MyAnimeList ID
    :param entries: Field: value entries to append to add
    :return: None
    """
    if entries['myStatus'] == 10:
        return False

    url = 'http://myanimelist.net/api/animelist/add/{}.xml'.format(anime_id)
    data = '<?xml version="1.0" encoding="UTF-8"?><entry>'

    for key in entries:
        if key in MAL_UPDATES:
            data += '<{}>{}</{}>'.format(MAL_UPDATES[key], str(entries[key]), MAL_UPDATES[key])
    data += '</entry>'

    try:
        doc = send_mal(url, {'data': data}, mal_key).read().decode('utf-8')
        return 'Created' in doc
    except uerror.HTTPError as e:
        if e.code == 501:
            return False
        else:
            raise MalDefaultError('Add transaction failed')


def update_all(mal_key, utoa_list):
    """
    Bulk update all anime and send to MAL

    :param mal_key: MyAnimeList authentication key
    :param utoa_list: Anime to add
    :return: None
    """
    for anime in utoa_list:
        update(mal_key, anime.malId, anime.__dict__)


@mal_transaction
def update(mal_key, anime_id, entries):
    """
    Update the given anime with the following entry values

    :param mal_key: MyAnimeList authentication key
    :param anime_id: Anime's MyAnimeList ID
    :param entries: Field: value entries to append to update
    :return: None
    """
    url = 'http://myanimelist.net/api/animelist/update/{}.xml'.format(anime_id)
    data = '<?xml version="1.0" encoding="UTF-8"?><entry>'

    for key in entries:
        if key in MAL_UPDATES:
            data += '<{}>{}</{}>'.format(MAL_UPDATES[key], str(entries[key]).replace('/', ''), MAL_UPDATES[key])
    data += '</entry>'

    try:
        doc = send_mal(url, {'data': data}, mal_key).read().decode('utf-8')
        return 'Updated' in doc
    except uerror.HTTPError as e:
        raise MalDefaultError('Update transaction failed')


def delete_all_by_id(mal_key, id_list):
    """
    Bulk delete all anime from MAL by ID

    :param mal_key: MyAnimeList authentication key
    :param id_list: List of anime by IDs to delete
    :return: None
    """
    for anime_id in id_list:
        delete(mal_key, anime_id)


def delete_all(mal_key, utoa_list):
    """
    Bulk delete all anime from MAL in User to Anime list

    :param mal_key: MyAnimeList authentication key
    :param utoa_list: List of User to Anime to delete
    :return: None
    """
    for anime in utoa_list:
        delete(mal_key, anime.malId)


@mal_transaction
def delete(mal_key, anime_id):
    """
    Delete the given anime by ID from the user's MAL

    :param mal_key: MyAnimeList authentication key
    :param anime_id: Anime ID to delete
    :return: None
    """
    url = 'http://myanimelist.net/api/animelist/delete/{}.xml'.format(anime_id)
    try:
        doc = send_mal(url, None, mal_key).read().decode('utf-8')
        return 'Deleted' in doc
    except uerror.HTTPError as e:
        raise MalDefaultError('Delete transaction failed')