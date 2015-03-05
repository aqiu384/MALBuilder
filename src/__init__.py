from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
# from flask.ext.heroku import Heroku

app = Flask(__name__)
app.config.from_object('config')
# #heroku = Heroku(app)
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from src import views, models