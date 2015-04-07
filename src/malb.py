import src.dbsession as DB
import src.aasession as AA
import src.malsession as MAL


def authenticate(username, password):
    """Authenticates user through MAL credentials"""
    return MAL.authenticate(username, password)


def add_anime(utoa_list, mal_key):
    """Bulk add anime to database"""
    DB.add_anime(utoa_list)
    MAL.add_all(mal_key, utoa_list)


def update_anime(anime_list, mal_key):
    """Bulk update anime to database"""
    DB.update_anime(anime_list)
    MAL.update_all(mal_key, anime_list)


def get_malb(user_id, fields):
    """Gets the users local MALB from the database"""
    return DB.get_malb(user_id, fields)

def get_season_dates(date, season):
    """Gets the start timeframe given a season"""
    return DB.get_season_dates(date, season)


def search_anime(user_id, filters, fields, sort_col='title', desc=False):
    """Searches anime in the database with the given filters and returns the given fields"""
    return DB.search_anime(user_id, filters, fields, sort_col, desc)


def search_mal(user_id, filters, fields, sort_col='title', desc=False):
    """Searches anime join user_to_anime in the database with the given filters and returns the given fields"""
    return DB.search_mal(user_id, filters, fields, sort_col, desc)


def synchronize_with_mal(username, mal_key, user_id):
    """Gets master copy of users MAL and overwrites the local MALB with it"""
    DB.delete_malb(user_id)
    return DB.add_anime(MAL.get_mal(username, mal_key))


def upload_aa_data(path):
    """Uploads AA formatted data to the database"""
    return DB.import_aa_data(AA.parse_aa_data(path))