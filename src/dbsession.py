from datetime import datetime
import json

from sqlalchemy import or_

from src import db
from src.models import Anime, AnimeToGenre, UserToAnime, UserToTag, SearchAnimeResult


AA_FILTERS = {
    'malIdStart': lambda x: Anime.malId >= x,
    'malIdEnd': lambda x: Anime.malId <= x,
    'type': lambda x: or_(*[Anime.type == xi for xi in x]),
    'status': lambda x: or_(*[Anime.status == xi for xi in x]),
    'title': lambda x: Anime.title == x,
    'startDateStart': lambda x: Anime.startDate >= x,
    'startDateEnd': lambda x: Anime.startDate <= x,
    'endDateStart': lambda x: Anime.endDate >= x,
    'endDateEnd': lambda x: Anime.endDate <= x,
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

MAL_FILTERS = {
    'join': lambda x: Anime.malId == UserToAnime.malId,
    'malIdStart': lambda x: Anime.malId >= x,
    'malIdEnd': lambda x: Anime.malId <= x,
    'type': lambda x: or_(*[Anime.type == xi for xi in x]),
    'showStatus': lambda x: or_(*[Anime.status == xi for xi in x]),
    'myStatus' : lambda x: or_(*[UserToAnime.myStatus == xi for xi in x]),
    'title': lambda x: Anime.title == x,
    'startDateStart': lambda x: Anime.startDate >= x,
    'startDateEnd': lambda x: Anime.startDate <= x,
    'endDateStart': lambda x: Anime.endDate >= x,
    'endDateEnd': lambda x: Anime.endDate <= x,
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
    'updateDateStart': lambda x: UserToAnime.myLastUpdate >= x,
    'updateDateEnd': lambda x: UserToAnime.myLastUpdate <= x,
    'genresInclude': lambda x: Anime.malId.in_(db.session.query(AnimeToGenre.malId)
                                               .filter(or_(*[AnimeToGenre.genreId == xi for xi in x]))
                                               .subquery()),
    'genresExclude': lambda x: ~Anime.malId.in_(db.session.query(AnimeToGenre.malId)
                                                .filter(or_(*[AnimeToGenre.genreId == xi for xi in x]))
                                                .subquery()),
}


def search_anime(user_id, filters, fields, sort_col, desc):
    """Search anime in anime database matching filters and return given fields"""
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

    return db.session.query(*my_fields).filter(*my_filters).order_by(sort_col).limit(30)

def search_mal(user_id, filters, fields, sort_col, desc):
    """Search anime join user_to_anime in db matching filters and returns the given fields"""
    my_fields = []
    for f in fields:
        if hasattr(Anime, f):
            my_fields.append(getattr(Anime, f))
        elif hasattr(UserToAnime, f):
            my_fields.append(getattr(UserToAnime,f))
    my_filters = [
        Anime.malId.in_(db.session.query(UserToAnime.malId)
                         .filter(UserToAnime.userId == user_id)
                         .subquery())
    ]

    #Joins two tables
    my_filters.append(MAL_FILTERS["join"]("dummy"))

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

    return db.session.query(*my_fields).filter(*my_filters).order_by(sort_col).limit(30)

def add_anime(anime_list, user_id):
    """Bulk add anime to database"""
    for anime in anime_list:
        utoa = UserToAnime(user_id, anime.malId)
        utoa.myStatus = anime.status

        if utoa.myStatus == 2:
            utoa.myEpisodes = 100

        db.session.merge(utoa)

    db.session.commit()


def synchronize_anime(anime_list):
    """Synchronize MAL download with database"""
    for anime in anime_list:
        db.session.merge(anime)

    db.session.commit()


def update_anime(anime_list, user_id):
    """Bulk update anime to database"""
    for anime_result in anime_list:
        utoa = UserToAnime(user_id, anime_result.malId)
        utoa.myScore = anime_result.myScore
        utoa.myEpisodes = anime_result.myEpisodes

        db.session.merge(utoa)

    db.session.commit()


def get_malb(user_id, fields, sort_col='title', desc=False):
    """Output MALB showing given fields"""
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

    return db.session.query(*my_fields).filter(*my_filters).order_by(sort_col).order_by(sort_col).all()


def delete_malb(user_id):
    """Deletes MALB for corresponding user"""
    return db.session.query(UserToAnime)\
        .filter(UserToAnime.userId == user_id)\
        .delete()


def parse_aa_entry(anime):
    """Parses an AA anime entry into DB anime format"""
    anime = anime['i']

    info = anime['11'][0]
    mal_id = info['a']
    curr = Anime(mal_id)
    curr.type = info.get('b')
    curr.status = info.get('c')
    curr.engTitle = info.get('d')
    curr.japTitle = info.get('e')
    curr.imgLink = info.get('f')

    info = anime['12'][0]
    curr.startDate = datetime.utcfromtimestamp(info.get('a', 0))
    curr.endDate = datetime.utcfromtimestamp(info.get('b', 0))
    # chapters 'c'
    # volumes 'd'
    curr.episodes = info.get('e')
    # length 'f'
    # rating 'g'
    curr.duration = info.get('h')

    temp = info.get('i')
    index = temp.find(' googletag')
    if index > -1:
        temp = temp[:index]

    curr.description = temp

    genres = []
    my_genres = ''
    for genre in anime['14']:
        atog = AnimeToGenre(mal_id, genre['a'])
        genres.append(atog)
        my_genres += str(genre['a']) + '.'

    curr.genres = my_genres[:-1]

    print(curr.genres)

    info = anime['15'][0]
    curr.score = info.get('a')
    curr.favorites = info.get('b')
    curr.members = info.get('c')
    curr.scoreCount = info.get('d')

    info = anime['2'][0]
    curr.title = info['a']

    return curr, genres


def parse_aa_data(filepath):
    """Parses all AA entries into DB from the given file"""
    with open(filepath, 'r') as file:
        for line in file:
            for anime in json.loads(line)['objects']:
                curr, genres = parse_aa_entry(anime)
                # print('{}\'s genres: {}'.format(curr.title, ', '.join([AA_GENRES[x.genreId] for x in genres])))

                db.session.add(curr)
                for genre in genres:
                    db.session.add(genre)

    db.session.commit()


def parse_search_results(fields, results):
    my_results = []
    for result in results:
        my_results.append(SearchAnimeResult(fields, result))
    return my_results


