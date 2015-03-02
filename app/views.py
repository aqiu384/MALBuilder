from flask import render_template, redirect, session, make_response, g, url_for, flash, request
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import LoginForm, AnimeSearchForm
from .models import search_anime, User
from .api.malsession import authenticate
from sqlalchemy import update


@lm.user_loader
def load_user(my_id):
    print(my_id)
    love = User.query.filter_by(malId=int(my_id)).first()
    # love = User(my_id)
    print('HI')
    print(love)
    print('HI')
    return love


@app.before_request
def before_request():
    g.user = current_user
    print(g.user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user and g.user.is_authenticated():
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.rememberMe.data
        resp = authenticate(form.username.data, form.password.data)

        if not resp.get('malId'):
            flash('Invalid MAL credentials. Please try again.')
            return redirect(url_for('login'))

        user = User.query.filter_by(malId=resp['malId']).first()

        if not user:
            print('ouch')
            user = User(resp['malId'])
            db.session.add(user)
            db.session.commit()

        update(User).where(User.malId == resp['malId']).values(name=resp['username'])

        remember_me = False
        if 'remember_me' in session:
            remember_me = session['remember_me']
            session.pop('remember_me', None)

        login_user(user, remember=remember_me)
        print(current_user)
        return redirect(url_for('index'))

    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'nickname': 'Miguel'}  # fake user
    posts = [  # fake array of posts
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html",
                           title='Home',
                           user=user,
                           posts=posts)


@app.route('/animesearch', methods=['GET', 'POST'])
def animesearch():
    form = AnimeSearchForm()
    results = []

    if form.validate_on_submit():
        results = search_anime(form.data, form.data['fields'])
        print(results)

    resp = make_response(render_template('animesearch.html',
                         title='MALB Anime Search',
                         results=results,
                         fields=form.data['fields'],
                         form=form))
    return resp