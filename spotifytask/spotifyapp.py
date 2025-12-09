from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_albums():
    conn = sqlite3.connect('spotifyDB.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT album_name FROM spotifyTracks WHERE popularity > 96")
    albums = cursor.fetchall()
    conn.close()
    return [album[0] for album in albums]

def top_100_tracks():
    conn = sqlite3.connect('spotifyDB.db')
    cursor = conn.cursor()
    cursor.execute("SELECT track_name, album_name, popularity FROM spotifyTracks ORDER BY popularity DESC LIMIT 100")
    tracks = cursor.fetchall()
    conn.close()
    return tracks

def search_tracks(track_name):
    conn = sqlite3.connect('spotifyDB.db')
    cursor = conn.cursor()
    cursor.execute("SELECT track_name, album_name, popularity FROM spotifyTracks WHERE track_name LIKE ?", ('%' + track_name + '%',))
    tracks = cursor.fetchall()
    conn.close()
    return tracks

@app.route("/")
def spotify():
    albums = get_albums()
    return render_template("index.html", albums=albums)

@app.route("/top100")
def top100():
    tracks = top_100_tracks()
    return render_template("index.html", tracks=tracks)

@app.route("/search")
def search():
    track_name = request.args.get('track', '')
    tracks = search_tracks(track_name) if track_name else []
    return render_template("index.html", tracks=tracks)

if __name__ == "__main__":
    app.debug = True
    app.run()