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

mal_transactions_enabled = app.config.get('MAL_TRANSACTIONS_ENABLED', False)


def mal_transaction(function):
    """Limits MAL transactions to only occur if enabled"""
    def wrapper(*args, **kwargs):
        if mal_transactions_enabled:
            return function(*args, **kwargs)
        print('MAL transaction attempted.')
        return False
    return wrapper

from src import views, models