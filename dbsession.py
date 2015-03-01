from app import app, db
from models import UserToAnime, Anime, AnimeToGenre
from API.malsession import MalSession
import time
import datetime
from sqlalchemy.orm import Load


def maldatetotimestamp(date):
    if date == '0000-00-00':
        return 0
    return int(time.mktime(datetime.datetime.strptime(date, '%Y-%m-%d').timetuple()))


class DbSession:
    def __init__(self, database):
        self.db = database

    def getanime(self, id):
        return Anime.query.filter_by(id=id).first()

    def getutoa(self, userid, animeid):
        return UserToAnime.query.filter_by(userid=userid, animeid=animeid)

    def getatog(self, anime, genre):
        return AnimeToGenre.query.filter_by(id=anime, genre=genre)

    def addanime(self, id, title, type, episodes, start, end, image):
        anime = Anime(id, title, type, episodes, start, end, image)
        self.db.session.add(anime)
        self.db.session.commit()

    def addusertoanime(self, userid, animeid, status):
        utoa = UserToAnime(userid, animeid, status)
        self.db.session.add(utoa)
        self.db.session.commit()

    def addanimetogenre(self, anime, genre):
        atog = AnimeToGenre(anime, genre)
        self.db.session.add(atog)
        self.db.session.commit()

    def deleteanime(self, id):
        return Anime.query.filter_by(id=id).delete(synchronize_session='fetch')

    def deleteusertoanime(self, userid, animeid):
        utoa = UserToAnime(userid, animeid)
        self.db.session.delete(utoa)
        self.db.session.commit()

    def deleteanimetogenre(self, anime, genre):
        atog = AnimeToGenre(anime, genre)
        self.db.session.delete(atog)
        self.db.session.commit()

    def synchronize_mal(self, mal):
        userid = int(mal.find('myinfo').find('user_id').text)
        print('User ID is {}'.format(userid))

        UserToAnime.query.filter_by(userid=userid).delete(synchronize_session=False)

        for entry in mal.findall('anime'):
            animeid = int(entry.find('series_animedb_id').text)
            print('Processing anime ID {}'.format(animeid))

            if Anime.query.filter_by(id=animeid).first() is None:
                anime = Anime(
                    animeid,
                    entry.find('series_title').text,
                    entry.find('series_type').text,
                    int(entry.find('series_episodes').text),
                    maldatetotimestamp(entry.find('series_start').text),
                    maldatetotimestamp(entry.find('series_end').text),
                    entry.find('series_image').text
                )
                self.db.session.add(anime)

            utoa = UserToAnime(
                userid,
                animeid,
                int(entry.find('my_status').text),
                int(entry.find('my_watched_episodes').text),
                int(entry.find('my_score').text)
            )
            self.db.session.add(utoa)

        self.db.session.commit()

    def get_mal(self):
        userid = 4448103

        query = UserToAnime.query.filter_by(userid=userid).join(Anime, UserToAnime.animeid == Anime.id)

        for anime in query.all():
            print(anime)




if __name__ == '__main__':
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dev:uiuc@localhost/pre-registration'
    myapp = app.test_client()
    db.drop_all()
    db.create_all()

    session = DbSession(db)
    session.addanime(1, 'Cowboy Bebop', 'Anime', 26, 1999, 2000, 'none')
    print(session.getanime(1))
    session.deleteanime(1)
    print(session.getanime(1))

    mal = MalSession('quetzalcoatl384', 'password')
    session.synchronize_mal(mal.getmal())
    session.get_mal()

    db.session.remove()
    db.drop_all()
