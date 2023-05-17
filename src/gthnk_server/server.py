# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import os
import flask

from flaskext.markdown import Markdown
from mdx_linkify.mdx_linkify import LinkifyExtension
from mdx_journal import JournalExtension

from . import login_manager, bcrypt

from gthnk import Gthnk


def create_app():
    app = flask.Flask(__name__)
    
    try:
        app.config.from_envvar('SETTINGS')
        g = Gthnk(os.getenv('SETTINGS'))
    except RuntimeError:
        default_filename = os.path.expanduser('~/.config/gthnk/.env')
        if os.path.isfile(default_filename):
            print(f"WARN: using default configuration file {default_filename}")
            app.config.from_pyfile(default_filename)
            g = Gthnk(default_filename)

    g.logger.info("Server: Start")

    from .blueprints.root import root
    app.register_blueprint(root)

    from .blueprints.auth import auth
    app.register_blueprint(auth)

    from .blueprints.day import day
    app.register_blueprint(day)

    # from .blueprints.attachments import attachments
    # app.register_blueprint(attachments)

    # db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    app.markdown = Markdown(app, extensions=[
        LinkifyExtension(),
        JournalExtension()
    ])

    return app

app = create_app()
