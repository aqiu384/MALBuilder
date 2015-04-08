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


def mal_transaction(function):
    """Limits MAL transactions to only occur if enabled"""
    def wrapper(*args, **kwargs):
        if app.config['MAL_TRANSACTIONS_ENABLED']:
            return function(*args, **kwargs)
        print('MAL transaction attempted.')
        return False
    return wrapper

from src import views, models