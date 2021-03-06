from sqlalchemy import or_

from src import db
from src.models import Anime, AnimeToGenre, UserToAnime, SearchAnimeResult
from src.constants import date_from_string


# AnimeAdvice filters to apply to query
AA_FILTERS = {
    'malIdStart': lambda x: Anime.malId >= x,
    'malIdEnd': lambda x: Anime.malId <= x,
    'type': lambda x: or_(*[Anime.type == xi for xi in x]),
    'status': lambda x: or_(*[Anime.status == xi for xi in x]),
    'title': lambda x: Anime.title == x,
    'startDateStart': lambda x: Anime.startDate >= date_from_string(x),
    'startDateEnd': lambda x: Anime.startDate <= date_from_string(x),
    'endDateStart': lambda x: Anime.endDate >= date_from_string(x),
    'endDateEnd': lambda x: Anime.endDate <= date_from_string(x),
    'anichartDateStart': lambda x: Anime.startDate >= x,
    'anichartDateEnd': lambda x: Anime.startDate <= x,
    'scoreStart': lambda x: Anime.score >= x,
    'scoreEnd': lambda x: Anime.score <= x,
    'membersStart': lambda x: Anime.members >= x,
    'membersEnd': lambda x: Anime.members <= x,
    'genresInclude': lambda x: Anime.malId.in_(db.session.query(AnimeToGenre.malId)
                                               .filter(or_(*[AnimeToGenre.genreId == xi for xi in x]))
                                               .subquery()),
    'genresExclude': lambda x: ~Anime.malId.in_(db.session.query(AnimeToGenre.malId)
                                                .filter(or_(*[AnimeToGenre.genreId == xi for xi in x]))
                                                .subquery()),
}

# MyAnimeList filters to apply to query
MAL_FILTERS = {
    'join': lambda x: Anime.malId == UserToAnime.malId,
    'malIdStart': lambda x: Anime.malId >= x,
    'malIdEnd': lambda x: Anime.malId <= x,
    'type': lambda x: or_(*[Anime.type == xi for xi in x]),
    'showStatus': lambda x: or_(*[Anime.status == xi for xi in x]),
    'myStatus': lambda x: or_(*[UserToAnime.myStatus == xi for xi in x]),
    'title': lambda x: Anime.title == x,
    'startDateStart': lambda x: Anime.startDate >= date_from_string(x),
    'startDateEnd': lambda x: Anime.startDate <= date_from_string(x),
    'endDateStart': lambda x: Anime.endDate >= date_from_string(x),
    'endDateEnd': lambda x: Anime.endDate <= date_from_string(x),
    'scoreStart': lambda x: Anime.score >= x,
    'scoreEnd': lambda x: Anime.score <= x,
    'membersStart': lambda x: Anime.members >= x,
    'membersEnd': lambda x: Anime.members <= x,
    'episodeGreaterThan': lambda x: Anime.episodes >= x,
    'episodeLessThan': lambda x: Anime.episodes <= x,
    'episodeWatchedStart': lambda x: UserToAnime.myEpisodes >= x,
    'episodeWatchedEnd': lambda x: UserToAnime.myEpisodes <= x,
    'myWatchDateStart': lambda x: UserToAnime.myStartDate >= x,
    'myWatchDateEnd': lambda x: UserToAnime.myEndDate <= x,
    'myScoreStart': lambda x: UserToAnime.myScore >= x,
    'myScoreEnd': lambda x: UserToAnime.myScore <= x,
    'rewatchEpisodesStart': lambda x: UserToAnime.myRewatchEps >= x,
    'rewatchEpisodesEnd': lambda x: UserToAnime.myRewatchEps <= x,
    'updateDateStart': lambda x: UserToAnime.myLastUpdate >= date_from_string(x),
    'updateDateEnd': lambda x: UserToAnime.myLastUpdate <= date_from_string(x),
    'genresInclude': lambda x: Anime.malId.in_(db.session.query(AnimeToGenre.malId)
                                               .filter(or_(*[AnimeToGenre.genreId == xi for xi in x]))
                                               .subquery()),
    'genresExclude': lambda x: ~Anime.malId.in_(db.session.query(AnimeToGenre.malId)
                                                .filter(or_(*[AnimeToGenre.genreId == xi for xi in x]))
                                                .subquery()),
}


def search_anime(user_id, filters, fields, sort_col, desc):
    """
    Search anime in anime database matching filters and return given fields

    :param user_id: User's MAL ID
    :param filters: Filters to apply to search
    :param fields: Columns to return in results
    :param sort_col: Sort column
    :param desc: Should sort descending
    :return: List of Search Anime results
    """
    my_fields = []
    for f in fields:
        if hasattr(Anime, f):
            my_fields.append(getattr(Anime, f))

    my_filters = [
        ~Anime.malId.in_(db.session.query(UserToAnime.malId)
                         .filter(UserToAnime.userId == user_id)
                         .subquery())
    ]
    for f in AA_FILTERS:
        if filters.get(f):
            my_filters.append(AA_FILTERS[f](filters[f]))

    if not hasattr(Anime, sort_col):
        sort_col = 'title'

    sort_col = getattr(Anime, sort_col)

    if desc:
        sort_col = sort_col.desc()

    results = db.session.query(*my_fields).filter(*my_filters).order_by(sort_col).limit(30)
    return parse_search_results(fields, results)


def search_mal(user_id, filters, fields, sort_col, desc):
    """
    Search anime in User's MAL matching filters and return given fields

    :param user_id: User's MAL ID
    :param filters: Filters to apply to search
    :param fields: Columns to return in results
    :param sort_col: Sort column
    :param desc: Should sort descending
    :return: List of Search Anime results
    """
    my_fields = []
    for f in fields:
        if hasattr(Anime, f):
            my_fields.append(getattr(Anime, f))
        elif hasattr(UserToAnime, f):
            my_fields.append(getattr(UserToAnime, f))

    my_filters = [
        Anime.malId.in_(db.session.query(UserToAnime.malId)
                        .filter(UserToAnime.userId == user_id)
                        .subquery()),
        MAL_FILTERS["join"]("dummy")
    ]

    for f in MAL_FILTERS:
        if filters.get(f):
            my_filters.append(MAL_FILTERS[f](filters[f]))

    if not hasattr(Anime, sort_col):
        if not hasattr(UserToAnime, sort_col):
            sort_col = getattr(Anime, 'title')
        else:
            sort_col = getattr(UserToAnime, sort_col)
    else:
        sort_col = getattr(Anime, sort_col)

    if desc:
        sort_col = sort_col.desc()

    results = db.session.query(*my_fields).filter(*my_filters).order_by(sort_col).limit(30)
    return parse_search_results(fields, results)


def get_anime_info(anime_id, fields):
    """
    Get field info for the anime with the given ID

    :param anime_id: ID of anime to be searched
    :param fields: Field info to be returned
    :return: Anime Result containing anime info
    """
    my_fields = []
    for f in fields:
        try:
            my_fields.append(getattr(Anime, f))
        except AttributeError:
            pass

    my_filters = [Anime.malId == anime_id]

    results = db.session.query(*my_fields).filter(*my_filters).limit(1)
    return parse_search_results(fields, results)


def add_anime(utoa_list):
    """
    Bulk add anime to database

    :param utoa_list: List of anime to add
    :return: None
    """
    for utoa in utoa_list:
        db.session.add(utoa)

    db.session.commit()


def update_anime(utoa_list):
    """
    Bulk update anime to database

    :param utoa_list: List of anime to update
    :return: None
    """
    for utoa in utoa_list:
        db.session.merge(utoa)

    db.session.commit()


def delete_anime(utoa):
    """
    Delete a single MALB entry for user

    :param utoa: UtoA object containing User ID and Anime ID
    :return: None
    """
    db.session.query(UserToAnime)\
        .filter(UserToAnime.userId == utoa.userId, UserToAnime.malId == utoa.malId)\
        .delete()
    db.session.commit()


def get_malb(user_id, fields, sort_col='title', desc=False):
    """
    Output MALB showing given fields

    :param user_id: User's MAL ID
    :param fields: Columns to return in results
    :param sort_col: Sort column
    :param desc: Should sort descending
    :return: List of Search Anime results
    """
    my_fields = []
    for f in fields:
        try:
            my_fields.append(getattr(UserToAnime, f))
        except AttributeError:
            try:
                my_fields.append(getattr(Anime, f))
            except AttributeError:
                pass

    my_filters = [
        UserToAnime.userId == user_id,
        UserToAnime.myStatus != 10,
        UserToAnime.malId == Anime.malId,
    ]

    try:
        sort_col = getattr(Anime, sort_col)
    except AttributeError:
        sort_col = getattr(Anime, 'title')

    if desc:
        sort_col = sort_col.desc()

    results = db.session.query(*my_fields).filter(*my_filters).order_by(sort_col).order_by(sort_col).all()
    return parse_search_results(fields, results)


def delete_malb(user_id):
    """
    Deletes MALB for corresponding user

    :param user_id: User's MAL ID
    :return: None
    """
    return db.session.query(UserToAnime)\
        .filter(UserToAnime.userId == user_id)\
        .delete()


def import_aa_data(anime_list):
    """
    Imports list of (Anime, AtoG) tuples into database

    :param anime_list: List of Anime results to import
    :return: None
    """
    for anime, atog in anime_list:
        db.session.add(anime)
        for genre in atog:
            db.session.add(genre)

    db.session.commit()


def parse_search_results(fields, results):
    """
    Parse DB search results into Search Anime format

    :param fields: Fields to return
    :param results: Results to parse
    :return: List of Search Anime parsed results
    """
    my_results = []
    for result in results:
        my_results.append(SearchAnimeResult(fields, result))
    return my_results


def get_season_dates(date, season):
    """
    Get tuple of bounds for the given year and season

    :param date: Year anime aired
    :param season: Season anime aired
    :return: Tuple of dates representing season bounds
    """
    start_date_start = date
    start_date_end = date
    if season == "Spring":
        start_date_start = date.replace(month=4)
        start_date_end = date.replace(month=6, day=30)
    elif season == "Summer":
        start_date_start = date.replace(month=7)
        start_date_end = date.replace(month=9, day=30)
    elif season == "Fall":
        start_date_start = date.replace(month=10)
        start_date_end = date.replace(month=12, day=31)
    elif season == "Winter":
        start_date_start = date.replace(month=1)
        start_date_end = date.replace(month=3, day=31)
    return start_date_start, start_date_end


