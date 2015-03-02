from flask import render_template, flash, redirect, session, make_response, request
from app import app
from .forms import LoginForm, AaSearchForm
from .api.aasession import AaSession, getquery, search_results
import json


@app.route('/')
@app.route('/index')
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])


@app.route('/aasearch', methods=['GET', 'POST'])
def aasearch():
    form = AaSearchForm()
    aa_query = ''

    if form.validate_on_submit():
        aa_query = getquery({
            'filters': form.data,
            'fields': form.data['returnFields'],
            'sort_col': 'aired_from',
            'sort_dir': -1,
            'result_count': 30
        })
        resp = make_response(redirect('/aasearch'))
        resp.set_cookie('query', aa_query)
        resp.set_cookie('fields', json.dumps(form.data['returnFields']))
        return resp

    aa_query = request.cookies.get('query')
    aa_fields = request.cookies.get('fields')
    aa_results = None
    if aa_query:
        print(aa_fields)
        aa_fields = json.loads(aa_fields)
        aa_results = search_results(aa_query, 0)

    resp = make_response(render_template('aasearch.html',
                         title='AnimeAdvice Search',
                         query=aa_query,
                         fields=aa_fields,
                         results=aa_results,
                         form=form))
    resp.set_cookie('query', '')
    resp.set_cookie('fields', '')
    return resp