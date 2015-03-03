import dbsession as DB
import api.malsession as MAL


def authenticate(username, password):
    return MAL.authenticate(username, password)


def search_anime(filters, fields):
    """Searches anime in the database with the given filters and returns the given fields"""
    return DB.search_anime(filters, fields)


def synchronize_with_mal(username, mal_key):
    """Gets master copy of users MAL and overwrites the local MALB with it"""
    return DB.parse_mal_data(MAL.get_mal(username, mal_key))


def upload_aa_data(path):
    """Uploads AA formatted data to the database"""
    return DB.parse_aa_data(path)