# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import os
import logging

import flask
from flask_login import LoginManager
from flaskext.markdown import Markdown
from mdx_linkify.mdx_linkify import LinkifyExtension
from mdx_journal import JournalExtension

login_manager = LoginManager()

from gthnk import Gthnk

if 'SETTINGS' in os.environ:
    gthnk = Gthnk(os.getenv('SETTINGS'))
else:
    gthnk = Gthnk()

def create_app():
    app = flask.Flask(__name__, static_folder=None)
    
    try:
        app.config.from_envvar('SETTINGS')
    except RuntimeError:
        default_filename = os.path.expanduser('~/.config/gthnk/gthnk.conf')
        if os.path.isfile(default_filename):
            print(f"WARN: using default configuration file {default_filename}")
            app.config.from_pyfile(default_filename)

    logging.getLogger("gthnk").info("Server: Start")

    from .root import root
    app.register_blueprint(root)

    from .home import home
    app.register_blueprint(home)

    from .api import api
    app.register_blueprint(api)

    from .auth import auth
    app.register_blueprint(auth)

    from .day import day
    app.register_blueprint(day)

    login_manager.init_app(app)
    app.markdown = Markdown(app, extensions=[
        LinkifyExtension(),
        JournalExtension()
    ])

    print(app.url_map)

    return app

app = create_app()
