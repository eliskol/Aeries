import requests
from aeries import Aeries

from flask import Flask
from flask import render_template
from flask import g
from flask import request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    user_aeries = Aeries(request.form['username'], request.form['password'])
    if user_aeries.logged_in:
        print('gj')
        return render_template('dashboard.html', classes=user_aeries.classes)
    return render_template('login.html')

@app.route('/class/<encoded_class_name>')
# def _class(encoded_class_name):
    # return 

app.run(host='0.0.0.0', port=3000)