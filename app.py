from flask import Flask, render_template , request, session, redirect, url_for  # , flash
# from markupsafe import escape
import os
import psycopg2
# import urllib.parse


app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='tunes',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn


@app.route('/show')
def show_releases():
    conn = get_db_connection()
    cur = conn.cursor()
    # cur.execute("SELECT discogs_release_string FROM tu_release r JOIN tu_song_release sr ON r.release_id = sr.release_id JOIN tu_song s ON sr.song_id = s.song_id WHERE s.song_title = 'moonlight in vermont';")
    cur.execute("SELECT discogs_release_string FROM tu_release r JOIN tu_song_release sr ON r.release_id = sr.release_id JOIN tu_song s ON sr.song_id = s.song_id WHERE s.song_title = %s;", (session['tune'],))
    releases = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('show_releases.html', releases=releases)


@app.route('/get', methods=["GET", "POST"])
def get_tune():
    if request.method == "POST":
        session['tune'] = request.form['tname']
        return redirect(url_for('show_releases'))

    # conn = get_db_connection()
    # cur = conn.cursor()
    return render_template('get_tune.html')
    # return """
    #     <form method="POST">
    #         <label for="tune_name">Tune Name</label>
    #         <input type="text" id="tunename" name="tname" placeholder="Tune Name">
    #         <button type="submit">Look Up</button>
    #     </form>
    # """

