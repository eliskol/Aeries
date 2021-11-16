import requests
from aeries import Aeries
import urllib.parse

from flask import Flask
from flask import render_template
from flask import g
from flask import request
from flask import session

app = Flask(__name__)
app.secret_key = 'ooga'
user_aeries = None


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    user_aeries = Aeries(request.form['username'], request.form['password'])
    session['username'], session['password'] = request.form['username'], request.form['password']
    session['classes'] = user_aeries.classes

    if user_aeries.logged_in:
        return render_template('dashboard.html', classes=user_aeries.classes)

    return render_template('login.html')


@app.route('/class/<encoded_class_name>')
def _class(encoded_class_name):
    decoded_class_name = urllib.parse.unquote(encoded_class_name)
    if decoded_class_name in session['classes']:
        return render_template('class.html', _class=session['classes'][decoded_class_name])


app.run(host='0.0.0.0', port=3000)
