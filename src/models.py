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
    genres = db.Column(db.String)

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
    myId = db.Column(db.Integer)
    watchedEps = db.Column(db.Integer)
    startDate = db.Column(db.Date)
    endDate = db.Column(db.Date)
    score = db.Column(db.Integer)
    status = db.Column(db.Integer)
    rewatching = db.Column(db.Boolean)
    rewatchEps = db.Column(db.Integer)
    lastUpdate = db.Column(db.DateTime)

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