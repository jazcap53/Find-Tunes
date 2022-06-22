from flask import Flask, render_template, request, flash
from markupsafe import escape
import os
from sqlalchemy import create_engine
import urllib.parse



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:kaZ00bie!do@localhost/tunes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ['SECRET_KEY']


@app.route('/')
def find_a_tune():
    return render_template('find_a_tune.html')
