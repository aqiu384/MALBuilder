from Website import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def __init__(self, id, nickname, email):
        self.id = id
        self.nickname = nickname
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.nickname