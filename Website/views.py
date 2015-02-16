from flask import render_template
from Website import app

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'quetzalcoatl384'}
    return render_template('index.html',
                           title='MALBuilder',
                           user=user)