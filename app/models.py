from app import db


WATCH_STATUS = {
    1: 'Currently watching',
    2: 'Completed',
    3: 'On Hold',
    4: 'Dropped',
    5: 'Plan to watch',
    6: 'Have not watched'
}


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     nickname = db.Column(db.String(64), index=True, unique=True)
#     email = db.Column(db.String(120), index=True, unique=True)
#     posts = db.relationship('Post', backref='author', lazy='dynamic')
#
#     def __repr__(self):
#         return '<User %r>' % self.nickname
#
#
# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     body = db.Column(db.String(140))
#     timestamp = db.Column(db.DateTime)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#
#     def __repr__(self):
#         return '<Post %r>' % self.body


class UserToAnime(db.Model):
    __tablename__ = 'usertoanime'
    __table_args__ = {"useexisting": True}

    userid = db.Column(db.Integer, primary_key=True)
    animeid = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer)
    episode = db.Column(db.Integer)
    score = db.Column(db.Integer)

    def __init__(self, userid, animeid, status=1, episode=0, score=0):
        self.userid = userid
        self.animeid = animeid
        self.status = status
        self.episode = episode
        self.score = score

    def __repr__(self):
        return '<User {}, Anime {}>'.format(self.userid, self.animeid)


class Anime(db.Model):
    __tablename__ = 'anime'
    __table_args__ = {"useexisting": True}

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    type = db.Column(db.String)
    episodes = db.Column(db.Integer)
    start = db.Column(db.Integer)
    end = db.Column(db.Integer)
    image = db.Column(db.String)

    def __init__(self, id, title, type, episodes, start, end, image):
        self.id = id
        self.title = title
        self.type = type
        self.episodes = episodes
        self.start = start
        self.end = end
        self.image = image

    def __repr__(self):
        return '<Anime {}>'.format(self.id)


class AnimeToGenre(db.Model):
    __tablename__ = 'animetogenre'
    __table_args__ = {"useexisting": True}

    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String, primary_key=True)

    def __repr__(self):
        return '<Anime {}, Genre {}>'.format(self.id, self.genre)