import src.dbsession as DB
import src.api.malsession as MAL


def authenticate(username, password):
    """Authenticates user through MAL credentials"""
    return MAL.authenticate(username, password)


def add_anime(anime_list, user_id, mal_key):
    """Bulk add anime to database"""
    return DB.add_anime(anime_list, user_id)


def update_anime(anime_list, user_id, mal_key):
    """Bulk update anime to database"""
    return DB.update_anime(anime_list, user_id)


def get_malb(user_id, fields):
    """Gets the users local MALB from the database"""
    return DB.parse_search_results(fields, DB.get_malb(user_id, fields))


def search_anime(user_id, filters, fields, sort_col='title', desc=False):
    """Searches anime in the database with the given filters and returns the given fields"""
    return DB.parse_search_results(fields, DB.search_anime(user_id, filters, fields, sort_col, desc))


def synchronize_with_mal(username, mal_key, user_id):
    """Gets master copy of users MAL and overwrites the local MALB with it"""
    DB.delete_malb(user_id)
    return DB.parse_mal_data(MAL.get_mal(username, mal_key))


def upload_aa_data(path):
    """Uploads AA formatted data to the database"""
    return DB.parse_aa_data(path)