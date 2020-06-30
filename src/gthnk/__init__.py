import os
import flask
import logging
import configparser

from pathlib import Path, PurePath
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flaskext.markdown import Markdown

from mdx_linkify.mdx_linkify import LinkifyExtension
from mdx_journal import JournalExtension

app = flask.Flask(__name__)
app.secret_key = b'_5#y3L"F4Q8z\n\xec]/'

app.config.from_envvar('SETTINGS')

print("logging to {}".format(app.config["LOG"]))
logging.basicConfig(
    format='%(asctime)s %(module)-16s %(levelname)-8s %(message)s',
    filename=app.config["LOG"],
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
logging.info("Server: Start")

logging.info("Database: {}".format(app.config['SQLALCHEMY_DATABASE_URI']))
db = SQLAlchemy()

login_manager = LoginManager()

markdown = Markdown(app, extensions=[
    LinkifyExtension(),
    JournalExtension()
])

def create_app():
    # this refers locally to the instance of app, above
    db.init_app(app)
    login_manager.init_app(app)

    return app
