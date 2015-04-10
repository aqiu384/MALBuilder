from flask import render_template, redirect, session, make_response, g, url_for, flash, request, Flask, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from src import app, db, lm
from src.forms import LoginForm, AnimeSearchForm, ADD_ANIME_FIELDS, UPDATE_ANIME_FIELDS, AnimeFilterForm, \
    createMultiAnimeForm, getMultiAnimeUtoa
from src.models import User
import src.malb as MALB


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
        return after_login(MALB.authenticate(form.username.data, form.password.data))

    return render_template('login.html',
                           title='Sign In',
                           form=form)


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
    session['username'] = my_username

    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)

    login_user(user, remember=remember_me)
    return redirect(url_for('index'))


@app.route('/logout')
@login_required
def logout():
    session.pop('malKey', None)
    session.pop('username', None)
    session.pop('search_data', None)
    logout_user()
    return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = AnimeFilterForm(prefix='my_form')
    parsed_results = []
    if form.submit.data and form.validate_on_submit():
        results = MALB.search_mal(g.user.malId, form.get_data(), form.data['fields'])
        for result in results:
            parsed_results.append(result.parse(form.data['fields']))

    return render_template("index.html",
                           title='Home',
                           username=session['username'],
                           fields=form.data['fields'],
                           form=form,
                           animelist=parsed_results)


@app.route('/searchanime', methods=['GET', 'POST'])
@login_required
def searchanime():
    form = AnimeSearchForm(prefix='my_form')

    if form.validate():
        session['search_data'] = form.get_data()
        return redirect(url_for('addanime'))

    return make_response(render_template('searchanime.html',
                         title='MALB Anime Search',
                         form=form))


@app.route('/addanime', methods=['GET', 'POST'])
@login_required
def addanime():
    try:
        data = session['search_data']
    except KeyError:
        return redirect(url_for('searchanime'))

    results = MALB.search_anime(g.user.malId, data, data['fields'])
    form = createMultiAnimeForm(results, ADD_ANIME_FIELDS, 'Add Anime', g.user.get_id())(prefix='add_form')

    if form.validate_on_submit():
        MALB.add_anime(getMultiAnimeUtoa(form, ['myStatus']), session['malKey'])
        return redirect(url_for('addanime'))

    return make_response(render_template('addanime.html',
                         title='MALB Anime Search',
                         form=form,
                         fields=ADD_ANIME_FIELDS))


@app.route('/sync')
@login_required
def sync():
    MALB.synchronize_with_mal(session['username'], session['malKey'], g.user.malId)
    print('synched')
    flash('Successfully synchronized with MyAnimeList')
    return redirect(request.referrer)


@app.route('/updateanime', methods=['GET', 'POST'])
@login_required
def updateanime():
    results = MALB.get_malb(g.user.malId, ['title', 'japTitle', 'engTitle', 'imgLink', 'score',
                                           'genres', 'episodes',
                                           'myStatus', 'myScore', 'myEpisodes', 'malId'])

    form = createMultiAnimeForm(results, UPDATE_ANIME_FIELDS, 'Update Anime', g.user.get_id())(prefix='edit_form')

    if form.validate_on_submit():
        MALB.update_anime(getMultiAnimeUtoa(form, ['myScore', 'myEpisodes', 'myStatus']), session['malKey'])
        return redirect(url_for('updateanime'))

    return render_template("updateanime.html",
                           title='Update Anime',
                           username=session['username'],
                           form=form,
                           fields=UPDATE_ANIME_FIELDS)