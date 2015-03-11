from src.constants import DEFAULT_DATE
from src import db


class User(db.Model):
    """Represents an MAL-authenticated user"""
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


class Anime(db.Model):
    """Lists AA details for anime"""
    __tablename__ = 'anime'
    __table_args__ = {"useexisting": True}

    malId = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, default=1)
    status = db.Column(db.Integer, default=1)
    title = db.Column(db.String, default='')
    engTitle = db.Column(db.String, default='')
    japTitle = db.Column(db.String, default='')
    imgLink = db.Column(db.String, default='')
    startDate = db.Column(db.Date, default=DEFAULT_DATE)
    endDate = db.Column(db.Date, default=DEFAULT_DATE)
    episodes = db.Column(db.Integer, default=1)
    duration = db.Column(db.Integer, default=1)
    description = db.Column(db.String, default='')
    score = db.Column(db.Float, default=0)
    favorites = db.Column(db.Integer, default=0)
    members = db.Column(db.Integer, default=0)
    scoreCount = db.Column(db.Integer, default=0)
    genres = db.Column(db.String, default='')

    def __init__(self, mal_id):
        self.malId = mal_id

    def __repr__(self):
        '<Anime {}, Title {}>'.format(self.malId, self.title)


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
    animeId = db.Column(db.Integer, primary_key=True)
    myId = db.Column(db.Integer, default=0)
    watchedEps = db.Column(db.Integer, default=0)
    myStartDate = db.Column(db.Date, default=DEFAULT_DATE)
    myEndDate = db.Column(db.Date, default=DEFAULT_DATE)
    myScore = db.Column(db.Integer, default=0)
    myStatus = db.Column(db.Integer, default=1)
    rewatching = db.Column(db.Boolean, default=False)
    rewatchEps = db.Column(db.Integer, default=0)
    lastUpdate = db.Column(db.DateTime, default=DEFAULT_DATE)

    def __init__(self, user_id, anime_id):
        self.userId = user_id
        self.animeId = anime_id

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