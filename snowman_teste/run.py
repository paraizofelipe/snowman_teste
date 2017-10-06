import gunicorn.app.base
from snowman_teste import api
from gunicorn.six import iteritems


class ServerApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(ServerApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
    API = api.create_api()
    options = {
        'reload': True,
        'workers': 2,
        'bind': '{}:{}'.format('0.0.0.0', '8000')
    }
    ServerApplication(API.module.__hug_wsgi__, options).run()
    # API.http.serve()
