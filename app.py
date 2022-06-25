# file: app.py
# Andrew Jarcho
# 2022-06-21

from flask import Flask, render_template , request, session, redirect, url_for  # , flash
# from markupsafe import escape
import os
import psycopg2
# import urllib.parse
from wtforms import RadioField
# from forms import radio_field


app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='tunes',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn


@app.route('/', methods=["GET", "POST"])
def choose_query():
    if request.method == "POST":
        selected_value = request.form['choose_query']
        if selected_value == '1':
            return redirect(url_for('get_tune'))
        elif selected_value == '2':
            return redirect(url_for('by_band'))
        else:
            return redirect(url_for('choose_query'))
    # radio = RadioField('Choose Query', choices=[
    #     ('1','by song title'),('2','by band or leader name'),('3','by partial song title'),('0','quit')])

    return render_template('choose_query.html')  # , radio=radio)


@app.route('/show')
def show_releases():
    conn = get_db_connection()
    cur = conn.cursor()
    if session['tune'] is not None:
        # return f'session[tune] is {session["tune"]}'
        cur.execute("SELECT discogs_release_string FROM tu_release r JOIN tu_song_release sr ON r.release_id = sr.release_id JOIN tu_song s ON sr.song_id = s.song_id WHERE s.song_title = %s;", (session['tune'],))
    elif session['band'] is not None:
        # return f'session[band] is {session["band"]}'
        band_with_dashes = session['band'].replace(' ', '-')
        # cur.execute("SELECT discogs_release_string FROM tu_release WHERE discogs_release_string LIKE %s;", ('%' + session['band'] + '%',))
        cur.execute("SELECT discogs_release_string FROM tu_release WHERE discogs_release_string LIKE %s;", ('%' + band_with_dashes + '%',))
    releases = cur.fetchall()
    cur.close()
    conn.close()
    # return f'len(releases) is {len(releases)}\n'
    return render_template('show_releases.html', releases=releases)


@app.route('/get', methods=["GET", "POST"])
def get_tune():
    if request.method == "POST":
        session['tune'] = request.form['tname']
        session['band'] = None
        return redirect(url_for('show_releases'))
    return render_template('get_tune.html')


@app.route('/band', methods=["GET", "POST"])
def by_band():
    if request.method == "POST":
        session['band'] = request.form['bname']
        session['tune'] = None
        return redirect(url_for('show_releases'))
    return render_template('by_band.html')

