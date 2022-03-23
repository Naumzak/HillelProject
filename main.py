import cherrypy


class Band(object):
    def __init__(self):
        self.albums = Album()
        self.songs = Song()

    def _cp_dispatch(self, vpath):
        if len(vpath) == 2: # <author>/author or <search>/search/
            resource_type = vpath.pop(0)
            if resource_type == 'author':
                cherrypy.request.params['name'] = vpath.pop()
                return self
            elif resource_type == 'search':
                pass
            return 'TypeError'

        if len(vpath) == 3:  # author/album/song
            cherrypy.request.params['artist'] = vpath.pop(0)
            cherrypy.request.params['title'] = vpath.pop(0)
            cherrypy.request.params['song'] = vpath.pop(0)
            return self.songs

        if len(vpath) == 4:  # <author>/author/<album>/album or <author>/author/<song>/song
            _ = vpath.pop(0)  # author/<album>/album or author/<song>/song
            cherrypy.request.params['artist'] = vpath.pop(0)  # /band name/
            resource_type = vpath.pop(0)
            if resource_type == 'album':
                cherrypy.request.params['title'] = vpath.pop(0)  # /album title/
                return self.albums
            elif resource_type == 'song':
                cherrypy.request.params['title'] = vpath.pop(0)  # /album title/
                return self.songs
            else:
                return 'TypeError'

    @cherrypy.expose
    def index(self, name):
        return 'About %s...' % name


class Album(object):
    @cherrypy.expose
    def index(self, artist, title):
        return 'About %s by %s...' % (title, artist)


class Song(object):
    @cherrypy.expose
    def index(self, artist, title):
        return 'About %s by %s...' % (title, artist)


if __name__ == '__main__':
    cherrypy.quickstart(Band())
