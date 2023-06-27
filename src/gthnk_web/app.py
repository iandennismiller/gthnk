# gthnk (c) Ian Dennis Miller

import os
import sys
import logging

import flask
from flask_login import LoginManager
from flaskext.markdown import Markdown
from mdx_linkify.mdx_linkify import LinkifyExtension
from mdx_journal import JournalExtension

login_manager = LoginManager()

from gthnk import Gthnk
config_filename = os.getenv('GTHNK_CONFIG', os.path.expanduser('~/.config/gthnk/gthnk.conf'))
gthnk = Gthnk(config_filename=config_filename)

from .journal import journal
from .root import root
from .home import home
from .auth import auth


def create_app():
    app = flask.Flask(__name__, static_folder=None)
    app.config.from_pyfile(config_filename)
    app.markdown = Markdown(app, extensions=[
        LinkifyExtension(),
        JournalExtension()
    ])

    app.register_blueprint(root)
    app.register_blueprint(home)
    app.register_blueprint(auth)
    app.register_blueprint(journal)

    login_manager.init_app(app)

    # print(app.url_map)
    logging.getLogger("gthnk").info("Server: Start")

    return app

app = create_app()
