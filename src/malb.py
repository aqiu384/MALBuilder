import src.dbsession as DB
import src.aasession as AA
import src.malsession as MAL


def authenticate(username, password):
    """
    "Authenticates user through MAL credentials

    :param username: MyAnimeList username
    :param password: MyAnimeList password
    :return: MyAnimeList API authentication response
    """
    return MAL.authenticate(username, password)


def add_anime(utoa_list, mal_key):
    """
    Bulk add anime to database

    :param utoa_list: List of User to Anime to add
    :param mal_key: MyAnimeList authentication key
    :return: None
    """
    DB.add_anime(utoa_list)
    MAL.add_all(mal_key, utoa_list)


def update_anime(anime_list, mal_key):
    """
    Bulk update anime to database

    :param anime_list: List of User to Anime to update
    :param mal_key: MyAnimeList authentication key
    :return: None
    """
    DB.update_anime(anime_list)
    MAL.update_all(mal_key, anime_list)


def delete_anime(utoa, mal_key):
    """
    Delete a single MALB entry for user

    :param utoa: UtoA object containing User ID and Anime ID
    :param mal_key: User's MAL login key
    :return: None
    """
    DB.delete_anime(utoa)
    MAL.delete(mal_key, utoa.malId)


def get_malb(user_id, fields):
    """
    Gets the users local MALB from the database

    :param user_id: User's MAL ID
    :param fields: The info columns to get for the MAL
    :return: The user's MAL with the given columns
    """
    return DB.get_malb(user_id, fields)


def get_season_dates(date, season):
    """
    Gets the start timeframe given a season

    :param date: Year to process
    :param season: Airing season
    :return: The date bounds for the corresponding year and season
    """
    return DB.get_season_dates(date, season)


def search_anime(user_id, filters, fields, sort_col='title', desc=False):
    """
    Searches anime in the database with the given filters and returns the given fields

    :param user_id: User's MAL ID
    :param filters: Search filters to apply
    :param fields: Columns to return in search
    :param sort_col: Column to sort by
    :param desc: Should sort desc or not
    :return: The corresponding Search Results list
    """
    return DB.search_anime(user_id, filters, fields, sort_col, desc)


def search_mal(user_id, filters, fields, sort_col='title', desc=False):
    """
    Searches anime currently existing in the User's MAL with the given filters and returns the given fields

    :param user_id: User's MAL ID
    :param filters: Search filters to apply
    :param fields: Columns to return in search
    :param sort_col: Column to sort by
    :param desc: Should sort desc or not
    :return: The corresponding Search Results list
    """
    return DB.search_mal(user_id, filters, fields, sort_col, desc)


def get_anime_info(anime_id, fields):
    """
    Get field info for the anime with the given ID

    :param anime_id: ID of anime to be searched
    :param fields: Field info to be returned
    :return: Anime Result containing anime info
    """
    return DB.get_anime_info(anime_id, fields)


def synchronize_with_mal(username, mal_key, user_id):
    """
    Gets master copy of users MAL and overwrites the local MALB with it

    :param username: MyAnimeList username
    :param mal_key: MyAnimeList authentication key
    :param user_id: User's MAL ID
    :return: None
    """
    DB.delete_malb(user_id)
    DB.add_anime(MAL.get_mal(username, mal_key))


def upload_aa_data(path):
    """
    Uploads AA formatted data to the database

    :param path: Path to JSON file containing AA data
    :return: None
    """
    DB.import_aa_data(AA.parse_aa_data(path))