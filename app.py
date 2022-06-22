from flask import Flask, render_template, request, flash
from markupsafe import escape
import os
import psycopg2
# from sqlalchemy import create_engine, text, select
import urllib.parse



app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='flask_db',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn




pw = os.environ['DB_PASSWORD']
escaped_pw = urllib.parse.quote_plus(pw)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://jazcap53:' + escaped_pw + '@localhost/tunes'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.secret_key = os.environ['SECRET_KEY']

# engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='tunes',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn




@app.route('/')
def find_a_tune():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT discogs_release_string FROM tu_release r JOIN tu_song_release sr ON r.release_id = sr.release_id JOIN tu_song s ON sr.song_id = s.song_id WHERE s.song_title = 'take the a train';")
    tunes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('find_a_tune.html', tunes=tunes)


# @app.route('/<tune>')
# def find_a_tune(tune=None):
#     conn = get_db_connection()
#     cur = conn.cursor()
#     select_stmnt = "SELECT discogs_release_string FROM tu_release r JOIN tu_song_release sr ON r.release_id = sr.release_id JOIN tu_song s ON sr.song_id = s.song_id WHERE s.song_title = %(song_title)s"
#     cur.execute(select_stmnt, { 'song_title': tune } )
#     tunes = cur.fetchall()
#     cur.close()
#     conn.close()
#     return render_template('find_a_tune.html', tunes=tunes)

