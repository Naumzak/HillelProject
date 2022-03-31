import cherrypy
import sqlite3
import os


def db_request(query):
    data_base = os.environ['db_name']
    con = sqlite3.connect(data_base)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    result = [dict(i) for i in cur.fetchall()]
    con.close()
    return result


class Band(object):
    def __init__(self):
        self.albums = Album()
        self.songs = Song()
        self.artist = Artist()
        self.search = Search()

    def _cp_dispatch(self, vpath):

        if len(vpath) == 2:  # <author>/author or <search>/search/
            resource_type = vpath.pop(0)
            if resource_type == 'author':
                cherrypy.request.params['artist'] = vpath.pop()
                return self.artist

        elif len(vpath) == 1:  # /search
            resource_type = vpath.pop(0)
            if resource_type == 'search':
                return self.search
            else:
                return self

        elif len(vpath) == 3:  # author/album/song
            cherrypy.request.params['artist'] = vpath.pop(0)
            cherrypy.request.params['title'] = vpath.pop(0)
            cherrypy.request.params['song'] = vpath.pop(0)
            return self.songs

        elif len(vpath) == 4:  # <author>/author/<album>/album or <author>/author/<song>/song
            _ = vpath.pop(0)  # author/<album>/album or author/<song>/song
            cherrypy.request.params['artist'] = vpath.pop(0)  # /band name/
            resource_type = vpath.pop(0)
            if resource_type == 'album':
                cherrypy.request.params['title'] = vpath.pop(0)  # /album title/
                return self.albums
            elif resource_type == 'song':
                cherrypy.request.params['song'] = vpath.pop(0)  # /album title/
                return self.songs
            else:
                return 'TypeError'

    @cherrypy.expose
    def index(self):
        query = f"""SELECT DISTINCT s.song_name, s.song_text, s.origin_lang, s.song_year  FROM song as s"""
        result = db_request(query)
        return str(result)



class Artist(object):
    @cherrypy.expose
    def index(self, artist):
        query = f"""
                    SELECT DISTINCT al.album_name, album_year FROM album as al
                    JOIN info_about_song AS ias ON ias.album_id = al.album_id
                    JOIN artist as ar ON ar.artist_id = ias.artist_id
                    WHERE ar.artist_name = '{artist.title()}'"""
        result = db_request(query)
        return str(result)


class Album(object):
    @cherrypy.expose
    def index(self, artist, title):
        query = f"""
                    SELECT DISTINCT s.song_name, s.song_text, s.origin_lang, s.song_year  FROM song as s
JOIN info_about_song AS ias ON ias.song_id = s.song_id
JOIN album as al ON al.album_id = ias.album_id
JOIN artist as ar ON ar.artist_id = ias.artist_id
WHERE ar.artist_name = '{artist.title()}' and al.album_name = '{' '.join(title.split('_')).title()}' """
        result = db_request(query)
        return str(result)


class Song(object):
    @cherrypy.expose
    def index(self, artist, song, title=''):
        query = f"""
                            SELECT DISTINCT s.song_name, s.song_text, s.origin_lang, s.song_year  FROM song as s
        JOIN info_about_song AS ias ON ias.song_id = s.song_id
        JOIN album as al ON al.album_id = ias.album_id
        JOIN artist as ar ON ar.artist_id = ias.artist_id
        WHERE ar.artist_name = '{artist.title()}' and s.song_name = '{' '.join(song.split('_')).title()}' """
        result = db_request(query)
        return str(result)


class Search(object):
    @cherrypy.expose
    def index(self):
        pass


if __name__ == '__main__':
    cherrypy.quickstart(Band())
