# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import os
import flask
import logging

from flaskext.markdown import Markdown
from mdx_linkify.mdx_linkify import LinkifyExtension
from mdx_journal import JournalExtension

from . import db, login_manager, bcrypt

from .models.day import Day
from .models.entry import Entry
from .models.page import Page
from .models.user import User


def create_app():
    app = flask.Flask(__name__)
    try:
        app.config.from_envvar('SETTINGS')
    except RuntimeError:
        default_filename = os.path.expanduser('~/.gthnk/gthnk.conf')
        if os.path.isfile(default_filename):
            print("WARN: using default configuration file ~/.gthnk/gthnk.conf")
            app.config.from_pyfile(default_filename)

    logging.basicConfig(
        format='%(asctime)s %(module)-16s %(levelname)-8s %(message)s',
        filename=app.config["LOG"],
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.info("Server: Start")
    logging.info("Database: {}".format(app.config['SQLALCHEMY_DATABASE_URI']))

    from .blueprints.root import root
    app.register_blueprint(root)

    from .blueprints.auth import auth
    app.register_blueprint(auth)

    from .blueprints.day import day
    app.register_blueprint(day)

    # from .blueprints.attachments import attachments
    # app.register_blueprint(attachments)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    app.markdown = Markdown(app, extensions=[
        LinkifyExtension(),
        JournalExtension()
    ])

    return app

app = create_app()
