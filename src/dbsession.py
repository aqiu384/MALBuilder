from src import db
from src.constants import AA_GENRES, AA_STATUS, AA_TYPE, MAL_STATUS
from src.models import Anime, AnimeToGenre, UserToAnime, UserToTag
from datetime import datetime
from sqlalchemy import or_
import json


def parse_mal_date(my_date):
    """Parse MAL date"""
    if my_date == '0000-00-00':
        return None
    return datetime.strptime(my_date, "%Y-%m-%d").date()


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
    'genresInclude': lambda x: Anime.malId.in_(db.session.query(AnimeToGenre.animeId)
                                               .filter(or_(*[AnimeToGenre.genreId == xi for xi in x]))
                                               .subquery()),
    'genresExclude': lambda x: ~Anime.malId.in_(db.session.query(AnimeToGenre.animeId)
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
        ~Anime.malId.in_(db.session.query(UserToAnime.animeId)
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


def add_anime(anime_list, user_id):
    """Bulk add anime to database"""
    for anime in anime_list:
        utoa = UserToAnime(user_id, anime['malId'])
        utoa.myStatus = anime['status']

        if utoa.myStatus == 2:
            utoa.watchedEps = 100

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
        UserToAnime.animeId == Anime.malId,
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


def parse_mal_entry(user_id, anime):
    """Parses an MAL anime entry into DB user format"""
    anime_id = anime.find('series_animedb_id').text
    utoa = UserToAnime(user_id, anime_id)

    utoa.myId = int(anime.find('my_id').text)
    utoa.watchedEps = int(anime.find('my_watched_episodes').text)
    utoa.myStartDate = parse_mal_date(anime.find('my_start_date').text)
    utoa.myEndDate = parse_mal_date(anime.find('my_finish_date').text)
    utoa.myScore = float(anime.find('my_score').text)
    utoa.myStatus = int(anime.find('my_status').text)
    utoa.rewatching = anime.find('my_rewatching').text is 1
    utoa.rewatchEps = int(anime.find('my_rewatching_ep').text)
    utoa.lastUpdate = datetime.fromtimestamp(int(anime.find('my_last_updated').text)).date()

    tags = []
    for tag in anime.find('my_tags'):
        utot = UserToTag(user_id, anime_id, tag)
        tags.append(utot)

    return utoa, tags


def parse_mal_data(tree):
    """Parses all MAL entries into DB from the given XML"""
    user_id = tree.find('myinfo').find('user_id').text
    for anime in tree.findall('anime'):
        curr, tags = parse_mal_entry(user_id, anime)

        db.session.merge(curr)
        for tag in tags:
            db.session.merge(tag)

    db.session.commit()


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


ANIME_RESULTS_FIELDS = {
    'genres': lambda x: ', '.join(AA_GENRES[int(xi)] for xi in x.split('.')),
    'status': lambda x: AA_STATUS[x],
    'type': lambda x: AA_TYPE[x],
    'myStatus': lambda x: MAL_STATUS[x]
}


def parse_search_results(fields, results):
    my_results = []
    for result in results:
        my_results.append(SearchAnimeResult(fields, result))
    return my_results


class SearchAnimeResult():
    def __init__(self, fields, result):
        for i in range(len(fields)):
            setattr(self, fields[i], result[i])

    def get(self, field):
        return ANIME_RESULTS_FIELDS.get(field, lambda x: x)(getattr(self, field))
