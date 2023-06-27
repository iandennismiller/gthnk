# gthnk (c) Ian Dennis Miller

import os
import logging

import flask
from flask_login import LoginManager
from flaskext.markdown import Markdown
from mdx_linkify.mdx_linkify import LinkifyExtension
from mdx_journal import JournalExtension
from gthnk import Gthnk

login_manager = LoginManager()
config_filename = os.getenv('GTHNK_CONFIG', os.path.expanduser('~/.config/gthnk/gthnk.conf'))
gthnk = Gthnk(config_filename=config_filename)

from .journal import journal # pylint: disable=wrong-import-position
from .root import root # pylint: disable=wrong-import-position
from .home import home # pylint: disable=wrong-import-position
from .auth import auth # pylint: disable=wrong-import-position


def create_app():
    "Create the Flask app object."
    app_obj = flask.Flask(__name__, static_folder=None)
    app_obj.config.from_pyfile(config_filename)
    app_obj.markdown = Markdown(app_obj, extensions=[
        LinkifyExtension(),
        JournalExtension()
    ])

    app_obj.register_blueprint(root)
    app_obj.register_blueprint(home)
    app_obj.register_blueprint(auth)
    app_obj.register_blueprint(journal)

    login_manager.init_app(app_obj)

    # print(app.url_map)
    logging.getLogger("gthnk").info("Server: Start")

    return app_obj

app = create_app()
