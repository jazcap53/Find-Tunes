from flask import Flask, render_template  # , request, flash
# from markupsafe import escape
import os
import psycopg2
# import urllib.parse


app = Flask(__name__)


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='tunes',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn


@app.route('/show')
def find_a_tune():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT discogs_release_string FROM tu_release r JOIN tu_song_release sr ON r.release_id = sr.release_id JOIN tu_song s ON sr.song_id = s.song_id WHERE s.song_title = 'take the a train';")
    releases = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('find_a_tune.html', releases=releases)
