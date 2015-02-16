from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

db_conn = 'postgresql+psycopg2://dev:uiuc@localhost/malb0'

app = Flask(__name__)
from Website import views
app.config['SQLALCHEMY_DATABASE_URI'] = db_conn
db = SQLAlchemy(app)

from Website import views, models