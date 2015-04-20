from flask import render_template, redirect, session, make_response, g, url_for, flash, request, Flask, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from src import app, db, lm
from src.forms import LoginForm, AnimeSearchForm, ADD_ANIME_FIELDS, UPDATE_ANIME_FIELDS, AnimeFilterForm, \
    createMultiAnimeForm, getMultiAnimeUtoa, AnichartForm, FlashcardForm, FlashcardSeasonForm
from src.models import User, UserToAnime
from flask_wtf import csrf
import src.malb as MALB
import json


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


@app.route('/anichart', methods=['GET', 'POST'])
@login_required
def anichart():
    form = AnichartForm(prefix='my_form')
    ret = "empty"
    if form.submit.data:
        startDateStart, startDateEnd = MALB.get_season_dates(form.data['startDateStart'], form.data['season'])
        filters = dict()
        filters['anichartDateStart'] = startDateStart
        filters['anichartDateEnd'] = startDateEnd
        ret = MALB.search_anime(g.user.malId, filters, ['title', 'startDate', 'malId', 'imgLink', 'description'],
                                sort_col='startDate')

    return render_template("anichart.html",
                           form=form,
                           ret=ret,
                           hasRet=form.submit.data,
                           lenRet=len(ret))


@app.route('/updateanime', methods=['GET', 'POST'])
@login_required
def updateanime():
    results = MALB.get_malb(g.user.malId, ['title', 'japTitle', 'engTitle', 'imgLink', 'score', 'genres', 'episodes',
                                           'myStatus', 'myScore', 'myEpisodes',
                                           'malId',
                                           'myRewatchEps', 'myLastUpdate', 'myStartDate', 'myEndDate'
                                           ])

    form = createMultiAnimeForm(results, UPDATE_ANIME_FIELDS, 'Update Anime', g.user.get_id())(prefix='edit_form')

    if form.validate_on_submit():
        MALB.update_anime(getMultiAnimeUtoa(form, ['myScore', 'myEpisodes', 'myStatus']), session['malKey'])
        return redirect(url_for('updateanime'))
    else:
        print(form.errors)

    return render_template("updateanime.html",
                           title='Update Anime',
                           username=session['username'],
                           form=form,
                           fields=UPDATE_ANIME_FIELDS)


@app.route('/flashcard', methods=['GET', 'POST'])
@login_required
def flashcard():
    session.pop('search_index', None)
    session.pop('search_results', None)

    season_form = FlashcardSeasonForm(csrf_enabled=False)

    return render_template("flashcard.html",
                           season_form=season_form)


@app.route('/add_flashcard', methods=['POST'])
@login_required
def add_flashcard():
    season_form = FlashcardSeasonForm(csrf_enabled=False)
    flashcard_form = FlashcardForm(csrf_enabled=False)

    search_metric = request.form.get('search_metric')
    my_filters = {}

    if search_metric == 'members':
        session['search_metric'] = 'members'
        session.pop('search_index', None)
        session.pop('search_results', None)
    elif search_metric == 'score':
        session['search_metric'] = 'score'
        session.pop('search_index', None)
        session.pop('search_results', None)
    elif search_metric == 'season' and season_form.validate_on_submit():
        sds, sde, = MALB.get_season_dates(season_form.data['year'], season_form.data['season'])
        my_filters = {'anichartDateStart': sds, 'anichartDateEnd': sde}
        session['search_metric'] = 'score'
        session.pop('search_index', None)
        session.pop('search_results', None)

    if flashcard_form.validate_on_submit():
        utoa = UserToAnime(g.user.malId, flashcard_form.data['anime_id'])
        utoa.myStatus = flashcard_form.data['status']
        MALB.add_anime([utoa], session['malKey'])
        session['search_index'] -= 1

    if not session.get('search_index'):
        results = MALB.search_anime(g.user.malId, my_filters, ['malId'], sort_col=session['search_metric'], desc=True)
        session['search_results'] = [x.malId for x in results]
        session['search_index'] = len(session['search_results'])

    anime = MALB.get_anime_info(session['search_results'][len(session['search_results']) - session['search_index']],
                                ['title', 'japTitle', 'engTitle', 'imgLink',
                                 'score', 'genres', 'episodes', 'malId', 'description'])[0].__dict__

    return json.dumps(anime)


@app.route('/delete_anime', methods=['POST'])
@login_required
def delete_anime():
    utoa = UserToAnime(g.user.get_id(), request.form.get('anime_id'))
    MALB.delete_anime(utoa, session['malKey'])
    print('successfully deleted')
    return json.dumps({'anime': '123'})


@app.route('/update_anime', methods=['POST'])
@login_required
def update_anime():
    utoa = UserToAnime(g.user.get_id(), request.form.get('anime_id'))

    field = request.form.get('field')
    value = request.form.get('value')

    if 'myEpisodes' in field:
        utoa.myEpisodes = value
    elif 'myScore' in field:
        utoa.myScore = value
    elif 'myStatus' in field:
        utoa.myStatus = value

    MALB.update_anime([utoa], session['malKey'])
    print('successfully updated')
    return json.dumps({'anime': '123'})


@app.route('/deleteanime', methods=['GET', 'POST'])
@login_required
def deleteanime():
    results = MALB.get_malb(g.user.malId, ['title', 'japTitle', 'engTitle', 'imgLink', 'score',
                                           'genres', 'episodes',
                                           'myStatus', 'myScore', 'myEpisodes', 'malId'])

    form = createMultiAnimeForm(results, UPDATE_ANIME_FIELDS, 'Update Anime', g.user.get_id())(prefix='edit_form')

    if form.validate_on_submit():
        MALB.update_anime(getMultiAnimeUtoa(form, ['myScore', 'myEpisodes', 'myStatus']), session['malKey'])
        return redirect(url_for('updateanime'))

    return render_template("deleteanime.html",
                           title='Update Anime',
                           username=session['username'],
                           form=form,
                           fields=UPDATE_ANIME_FIELDS)