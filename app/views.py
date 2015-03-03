from flask import render_template, redirect, session, make_response, g, url_for, flash, request
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import LoginForm, AnimeSearchForm
from .models import search_anime, User
from dbsession import DbSession
from .api.malsession import authenticate, MalSession
from sqlalchemy import update
from xml.etree import ElementTree as ET


@lm.user_loader
def load_user(my_id):
    my_user = User.query.filter_by(malId=int(my_id)).first()
    return my_user


@app.before_request
def before_request():
    g.user = current_user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user and g.user.is_authenticated():
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.rememberMe.data
        return after_login(authenticate(form.username.data, form.password.data))

    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])


def after_login(resp):
    if not resp.get('malId'):
        flash('Invalid MAL credentials. Please try again.')
        return redirect(url_for('login'))

    my_malid = resp['malId']
    my_malKey = resp['malKey']
    my_username = resp['username']

    user = User.query.filter_by(malId=my_malid).first()

    if not user:
        user = User(my_malid)
        db.session.add(user)
        db.session.commit()

    session['malKey'] = my_malKey
    session['malId'] = my_malid
    session['username'] = my_username

    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)

    login_user(user, remember=remember_me)
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('malKey', None)
    session.pop('username', None)
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template("index.html",
                           title='Home',
                           username=session['username'])


@app.route('/animesearch', methods=['GET', 'POST'])
def animesearch():
    form = AnimeSearchForm()
    results = []

    if form.validate_on_submit():
        results = search_anime(form.data, form.data['fields'])

    resp = make_response(render_template('animesearch.html',
                         title='MALB Anime Search',
                         results=results,
                         fields=form.data['fields'],
                         form=form))
    return resp

@app.route('/sync', methods=['GET', 'POST'])
def sync():
    mal = MalSession(session['username'], '')
    ret = mal.getmal()
    db_session = DbSession(db)
    db_session.synchronize_mal(ret)
    resp = make_response(render_template('sync_mal.html', malID = session['username'], debug = ret))
    return resp