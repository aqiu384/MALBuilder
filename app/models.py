from app import app, db
from datetime import datetime
from sqlalchemy import or_
import json
import xml.etree.ElementTree as ET


class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {"useexisting": True}

    malId = db.Column(db.Integer, primary_key=True)

    def __init__(self, mal_id):
        self.malId = mal_id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.malId)  # python 3

    def __repr__(self):
        return '<MAL ID: {:d}'.format(self.malId)


AA_TYPE = {
    5: 'Movie',
    9: 'Music',
    8: 'ONA',
    6: 'OVA',
    11: 'Special',
    4: 'TV'
}

AA_STATUS = {
    4: 'Currently Airing',
    2: 'Finished Airing',
    3: 'Not Yet Aired'
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
    31: 'Horror',
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
    21: 'Supernatural',
    42: 'Thriller',
    38: 'Vampire',
    0: 'Yaoi',
    2: 'Yuri'
}


MAL_STATUS = {
    1: 'Watching',
    2: 'Completed',
    3: 'On hold',
    4: 'Dropped',
    6: 'Plan to watch',
    10: 'Have not seen'
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
    'description': 'Description',
    'score': 'MAL rating',
    'favorites': 'MAL favorites count',
    'members': 'MAL member count',
    'scoreCount': 'MAL score count'
}


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
    'membersEnd': lambda x: Anime.members <= x
}

class Anime(db.Model):
    """Lists AA details for anime"""
    __tablename__ = 'anime'
    __table_args__ = {"useexisting": True}

    malId = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer)
    status = db.Column(db.Integer)
    title = db.Column(db.String)
    engTitle = db.Column(db.String)
    japTitle = db.Column(db.String)
    imgLink = db.Column(db.String)
    startDate = db.Column(db.Date)
    endDate = db.Column(db.Date)
    description = db.Column(db.String)
    score = db.Column(db.Float)
    favorites = db.Column(db.Integer)
    members = db.Column(db.Integer)
    scoreCount = db.Column(db.Integer)

    def __init__(self, mal_id, title=None, type=None, episodes=None, start=None, end=None, image=None):
        self.malId = mal_id
        self.title = title
        self.type = type
        self.image = image

    def __repr__(self):
        '<Anime {}, Title {}>'.format(self.malId, self.title)





def search_anime(filters, fields):
    my_fields = []
    for f in fields:
        if hasattr(Anime, f):
            my_fields.append(getattr(Anime, f))

    my_filters = []
    for f in AA_FILTERS:
        if filters.get(f):
            my_filters.append(AA_FILTERS[f](filters[f]))

    return db.session.query(*my_fields).filter(*my_filters).all()


class AnimeToGenre(db.Model):
    """Maps anime to their list of genres"""
    __tablename__ = 'anime_to_genre'
    __table_args__ = {"useexisting": True}

    animeId = db.Column(db.Integer, primary_key=True)
    genreId = db.Column(db.Integer, primary_key=True)

    def __init__(self, anime_id, genre_id):
        self.animeId = anime_id
        self.genreId = genre_id

    def __repr__(self):
        '<Anime {}, Genre {}>'.format(self.animeId, self.genreId)


class UserToAnime(db.Model):
    """Maps user to anime they have categorized"""
    __tablename__ = 'user_to_anime'
    __table_args__ = {"useexisting": True}

    userId = db.Column(db.Integer, primary_key=True)
    animeId = db.Column(db.Integer, db.ForeignKey("anime.malId"), primary_key=True)
    myId = db.Column(db.Integer)
    watchedEps = db.Column(db.Integer)
    startDate = db.Column(db.Date)
    endDate = db.Column(db.Date)
    score = db.Column(db.Integer)
    status = db.Column(db.Integer)
    rewatching = db.Column(db.Boolean)
    rewatchEps = db.Column(db.Integer)
    lastUpdate = db.Column(db.DateTime)

    def __init__(self, user_id, anime_id, status, watched, score):
        self.userId = user_id
        self.animeId = anime_id
        self.status = status
        self.watchedEps = watched
        self.score = score

    def __repr__(self):
        '<User {}, Anime {}>'.format(self.userId, self.animeId)


class UserToTag(db.Model):
    """Maps user and their anime to a tag they associated with it"""
    __tablename__ = 'user_to_tags'
    __table_args__ = {"useexisting": True}

    userId = db.Column(db.Integer, primary_key=True)
    animeId = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String, primary_key=True)

    def __init__(self, user_id, anime_id, tag):
        self.userId = user_id
        self.animeId = anime_id
        self.tag = tag

    def __repr__(self):
        '<User {}, Anime {}, Tag {}>'.format(self.userId, self.animeId, self.tag)


def parse_mal_entry(user_id, anime):
    """Parses an MAL anime entry into DB user format"""
    anime_id = anime.find('series_animedb_id').text
    utoa = UserToAnime(user_id, anime_id)

    utoa.myId = anime.find('my_id').text
    utoa.watchedEps = anime.find('my_watched_episodes').text
    utoa.startDate = anime.find('my_start_date').text
    utoa.endDate = anime.find('my_finish_date').text
    utoa.score = anime.find('my_score').text
    utoa.status = anime.find('my_status').text
    utoa.rewatching = anime.find('my_rewatching').text is 1
    utoa.rewatchEps = anime.find('my_rewatching_ep').text
    utoa.lastUpdate = anime.find('my_last_updated').text

    tags = []
    for tag in anime.find('my_tags'):
        utot = UserToTag(user_id, anime_id, tag)
        tags.append(utot)

    return utoa, tags


def parse_mal_data(data):
    """Parses all MAL entries into DB from the given XML"""
    root = ET.fromstring(data)
    user_id = root.find('myinfo').find('user_id').text
    print(user_id)
    for anime in root.findall('anime'):
        curr, tags = parse_mal_entry(user_id, anime)
        print(curr.watchedEps)


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
    curr.description = info.get('e')

    genres = []
    for genre in anime['14']:
        atog = AnimeToGenre(mal_id, genre['a'])
        genres.append(atog)

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


if __name__ == '__main__':
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    myapp = app.test_client()
    db.drop_all()
    db.create_all()

    parse_aa_data('../data/aaresults0.txt')
    # search_anime()

    sample_xml = '''<?xml version="1.0" encoding="UTF-8"?>
    <myanimelist>
        <myinfo>
            <user_id>189038</user_id>
            <user_name>domokun1134</user_name>
            <user_watching>11</user_watching>
            <user_completed>245</user_completed>
            <user_onhold>19</user_onhold>
            <user_dropped>40</user_dropped>
            <user_plantowatch>96</user_plantowatch>
            <user_days_spent_watching>80.32</user_days_spent_watching>
        </myinfo>
        <anime>
            <series_animedb_id>1</series_animedb_id>
                <series_title>Cowboy Bebop</series_title>
                <series_synonyms>; Cowboy Bebop</series_synonyms>
                <series_type>1</series_type>
                <series_episodes>26</series_episodes>
                <series_status>2</series_status>
                <series_start>1998-04-03</series_start>
                <series_end>1999-04-24</series_end>
                <series_image>
                http://cdn.myanimelist.net/images/anime/4/19644.jpg
                </series_image>
                <my_id>24473642</my_id>
                <my_watched_episodes>26</my_watched_episodes>
                <my_start_date>0000-00-00</my_start_date>
                <my_finish_date>2010-11-21</my_finish_date>
                <my_score>9</my_score>
                <my_status>2</my_status>
                <my_rewatching>0</my_rewatching>
                <my_rewatching_ep>0</my_rewatching_ep>
                <my_last_updated>1290352931</my_last_updated>
            <my_tags/>
        </anime>
    </myanimelist>'''

    parse_mal_data(sample_xml)

    # db.session.remove()
    # db.drop_all()
