from flask import render_template, redirect, session, make_response, g, url_for, flash, request, Flask, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from src import app, db, lm
from src.forms import LoginForm, AnimeSearchForm, AddAnimeForm, UpdateAnimeForm, AnimeFilterForm
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
def logout():
    session.pop('malKey', None)
    session.pop('username', None)
    logout_user()
    return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = AnimeFilterForm(prefix='my_form')
    parsed_results = []
    if form.submit.data and form.validate_on_submit():
        results = MALB.search_anime(g.user.malId, form.data, form.data['fields'])
        for result in results:
            parsed_results.append(result.parse(form.data['fields']))

    return render_template("index.html",
                           title='Home',
                           username=session['username'],
                           fields=form.data['fields'],
                           animelist=parsed_results)


@app.route('/animesearch', methods=['GET', 'POST'])
def animesearch():
    form = AnimeSearchForm(prefix='my_form')
    add_form = AddAnimeForm(prefix='add_form')
    print("i'm searching")
    if form.submit.data and form.validate_on_submit():
        results = MALB.search_anime(g.user.malId, form.data, form.data['fields'])
        add_form.init_results(results)

    if add_form.submit.data:
        #MALB.add_anime(add_form.subforms.data, g.user.get_id(), session['malKey'])
        print(add_form.subforms.data)
        results = MALB.search_anime(g.user.malId, form.data, form.data['fields'])
        add_form.init_results(results)
        flash('Successfully synchronized with MyAnimeList')
        # return redirect(url_for('animesearch'))

    resp = make_response(render_template('animesearch.html',
                         title='MALB Anime Search',
                         add_form=add_form,
                         fields=form.data['fields'],
                         form=form))
    return resp


@app.route('/addanime', methods=['GET'])
def addanime():
    form = AnimeSearchForm(prefix='my_form')
    add_form = AddAnimeForm(prefix='add_form')

    if form.submit.data and form.validate_on_submit():
        results = MALB.search_anime(g.user.malId, form.data, form.data['fields'])
        add_form.init_results(results)

    resp = make_response(render_template('addanime.html',
                         title='MALB Anime Search',
                         add_form=add_form,
                         fields=form.data['fields'],
                         form=form))
    return resp

@app.route('/addanime', methods=['POST'])
def addanimepost():
    form = AnimeSearchForm(prefix='my_form')
    add_form = AddAnimeForm(prefix='add_form')

    if form.validate():
        results = MALB.search_anime(g.user.malId, form.data, form.data['fields'])
        add_form.init_results(results)
    else:
         MALB.add_anime(add_form.subforms.data, g.user.get_id(), session['malKey'])
         print(add_form.subforms.data)
         flash('Successfully synchronized with MyAnimeList')
         return redirect(url_for('addanime'))

    resp = make_response(render_template('addanime.html',
                         title='MALB Anime Search',
                         add_form=add_form,
                         fields=form.data['fields'],
                         form=form))
    return resp

@app.route('/sync')
@login_required
def sync():
    MALB.synchronize_with_mal(session['username'], session['malKey'], g.user.malId)
    flash('Successfully synchronized with MyAnimeList')
    return redirect(url_for('index'))