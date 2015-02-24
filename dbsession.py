from app import db
from models import UserToAnime, Anime, AnimeToGenre

class DbSession:
    def __init__(self):
        self.db = db

    def animeindb(self, id):
        return Anime.query.filter_by(id=id).first() is not None

    def addanime(self, id, title, type, episodes, start, end, image):
        anime = Anime(id, title, type, episodes, start, end, image)
        self.db.session.add(anime)
        self.db.session.commit()