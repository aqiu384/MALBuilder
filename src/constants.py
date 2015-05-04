from datetime import date, datetime


# Maps annime fields to functions results field in printable format
ANIME_RESULTS_FIELDS = {
    'genres': lambda x: ', '.join(AA_GENRES[int(xi)] for xi in x.split('.')),
    'status': lambda x: AA_STATUS[x],
    'type': lambda x: AA_TYPE[x],
    'myStatus': lambda x: MAL_STATUS[x],
    'episodes': lambda x: 9001 if x == 0 else x
}

# Maps MAL fields to MyAnimeList fields
MAL_UPDATES = {
    'myEpisodes': 'episode',
    'myStartDate': 'date_start',
    'myEndDate': 'date_finish',
    'myScore': 'score',
    'myStatus': 'status',
}

# Maps MAL fields to printable name
ANIME_ATTRS = {
    'malId': 'MAL ID',
    'type': 'Medium type',
    'status': 'Airing status',
    'title': 'Title',
    'engTitle': 'English title',
    'japTitle': 'Japanese title',
    'imgLink': 'Image thumbnail',
    'startDate': 'Start date',
    'endDate': 'End date',
    'episodes': 'Episodes',
    'duration': 'Duration',
    'description': 'Description',
    'score': 'MAL rating',
    'favorites': 'MAL favorites count',
    'members': 'MAL member count',
    'scoreCount': 'MAL score count',
    'genres': 'Genres'
}

# Maps MAL User fields to printable name
USER_ATTRS = {
    'myEpisodes': 'Watched Episodes',
    'myStartDate': 'Watch Start Date',
    'myEndDate': 'Watch End Date',
    'myScore': 'My Score',
    'myStatus': 'Smy Status',
    'myRewatchEps': 'Episodes Rewatched',
    'myLastUpdate': 'Last Updated'
}

# Combines MAL and User fields
ANIME_USER_ATTRS = ANIME_ATTRS.copy()
ANIME_USER_ATTRS.update(USER_ATTRS)

# Maps AnimeAdvice genre IDs to printable genre name
AA_GENRES = {
    4: 'Action',
    5: 'Adventure',
    29: 'Cars',
    6: 'Comedy',
    35: 'Dementia',
    9: 'Demons',
    44: 'Doujinshi',
    1: 'Drama',
    25: 'Ecchi',
    10: 'Fantasy',
    31: 'Game',
    33: 'Gender Bender',
    27: 'Harem',
    42: 'Hentai',
    14: 'Historical',
    11: 'Horror',
    28: 'Josei',
    41: 'Kids',
    18: 'Magic',
    23: 'Martial Arts',
    36: 'Mecha',
    13: 'Military',
    20: 'Music',
    0: 'Mystery',
    37: 'Parody',
    19: 'Police',
    2: 'Psychological',
    21: 'Romance',
    32: 'Samurai',
    26: 'School',
    7: 'Sci-Fi',
    3: 'Seinen',
    22: 'Shoujo',
    39: 'Shoujo Ai',
    16: 'Shounen',
    40: 'Shounen Ai',
    15: 'Slice of Life',
    8: 'Space',
    17: 'Sports',
    24: 'Super Power',
    12: 'Supernatural',
    30: 'Thriller',
    34: 'Vampire',
    38: 'Yaoi',
    43: 'Yuri'
}

# Maps AnimeAdvice airing status to printable status
AA_STATUS = {
    4: 'Currently Airing',
    2: 'Finished Airing',
    3: 'Not Yet Aired'
}

# Maps AnimeAdvice medium type to printable type
AA_TYPE = {
    2: 'Movie',
    9: 'Music',
    8: 'ONA',
    3: 'OVA',
    7: 'Special',
    1: 'TV'
}

# Maps MyAnimeList watch status to printable status
MAL_STATUS = {
    1: 'Watching',
    2: 'Completed',
    3: 'On hold',
    4: 'Dropped',
    6: 'Plan to watch',
    10: 'Have not seen'
}

# Reverse map of MAL Status
MAL_STATUS2 = {v: k for k, v in MAL_STATUS.items()}

# Maps Authentic MAL scores to their string representation
MAL_SCORE = {x: str(x) for x in range(11)}

# Default date and format for MAL
DEFAULT_DATE = date(1, 1, 1)
DATE_FORMAT = '%m/%d/%Y'


def date_to_string(my_date):
    """
    Converts date object to MAL date string

    :param my_date: Date object
    :return: MAL date string
    """
    if my_date:
        return my_date.strftime(DATE_FORMAT)
    return None


def date_from_string(my_string):
    """
    Creates date object from MAL date string

    :param my_string: MAL date string
    :return: Date object
    """
    if my_string:
        return datetime.strptime(my_string, DATE_FORMAT).date()
    return None