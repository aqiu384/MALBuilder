from datetime import date, datetime


ANIME_RESULTS_FIELDS = {
    'genres': lambda x: ', '.join(AA_GENRES[int(xi)] for xi in x.split('.')),
    'status': lambda x: AA_STATUS[x],
    'type': lambda x: AA_TYPE[x],
    'myStatus': lambda x: MAL_STATUS[x],
    # 'myStatus2': lambda x: MAL_STATUS2[x],
    'episodes': lambda x: 9001 if x == 0 else x
}


MAL_UPDATES = {
    'myEpisodes': 'episode',
    'myStartDate': 'date_start',
    'myEndDate': 'date_finish',
    'myScore': 'score',
    'myStatus': 'status',
    # 'myStatus2': lambda x: MAL_STATUS2[x],
}


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

USER_ATTRS = {
    'myEpisodes': 'Watched Episodes',
    'myStartDate': 'Watch Start Date',
    'myEndDate': 'Watch End Date',
    'myScore': 'My Score',
    'myStatus': 'Smy Status',
    'myRewatchEps': 'Episodes Rewatched',
    'myLastUpdate': 'Last Updated'
}

ANIME_USER_ATTRS = {
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
    'genres': 'Genres',
    'myEpisodes': 'Watched Episodes',
    'myStartDate': 'Watch Start Date',
    'myEndDate': 'Watch End Date',
    'myScore': 'My Score',
    'myStatus': 'Smy Status',
    'myRewatchEps': 'Episodes Rewatched',
    'myLastUpdate': 'Last Updated'
}

AA_GENRES = {
    10: 'Action',
    11: 'Adventure',
    44: 'Cars',
    17: 'Comedy',
    43: 'Dementia',
    24: 'Demons',
    7: 'Doujinshi',
    26: 'Drama',
    9: 'Ecchi',
    12: 'Fantasy',
    35: 'Game',
    6: 'Gender Bender',
    23: 'Harem',
    1: 'Hentai',
    27: 'Historical',
    21: 'Horror',
    29: 'Josei',
    14: 'Kids',
    32: 'Magic',
    33: 'Martial Arts',
    15: 'Mecha',
    8: 'Military',
    39: 'Music',
    20: 'Mystery',
    36: 'Parody',
    30: 'Police',
    22: 'Psychological',
    3: 'Romance',
    34: 'Samurai',
    4: 'School',
    16: 'Sci-Fi',
    13: 'Seinen',
    5: 'Shoujo',
    40: 'Shoujo Ai',
    19: 'Shounen',
    18: 'Shounen Ai',
    28: 'Slice of Life',
    41: 'Space',
    37: 'Sports',
    25: 'Super Power',
    2: 'Supernatural',
    42: 'Thriller',
    38: 'Vampire',
    0: 'Yaoi',
    31: 'Yuri'
}

AA_STATUS = {
    4: 'Currently Airing',
    2: 'Finished Airing',
    3: 'Not Yet Aired'
}

AA_TYPE = {
    5: 'Movie',
    9: 'Music',
    8: 'ONA',
    6: 'OVA',
    11: 'Special',
    4: 'TV'
}

MAL_STATUS = {
    1: 'Watching',
    2: 'Completed',
    3: 'On hold',
    4: 'Dropped',
    6: 'Plan to watch',
    10: 'Have not seen'
}

MAL_STATUS2 = {
    'Watching': 1,
    'Completed': 2,
    'On hold': 3,
    'Dropped': 4,
    'Plan to watch': 6,
    'Have not seen': 10
}

MAL_SCORE = {
    0: '0',
    1: '1',
    2: '2',
    3: '3',
    4: '4',
    5: '5',
    6: '6',
    7: '7',
    8: '8',
    9: '9',
    10: '10',
}

DEFAULT_DATE = date(1, 1, 1)
DATE_FORMAT = '%m/%d/%Y'


def date_to_string(my_date):
    if my_date:
        return my_date.strftime(DATE_FORMAT)
    return None


def date_from_string(my_string):
    if my_string:
        return datetime.strptime(my_string, DATE_FORMAT).date()
    return None