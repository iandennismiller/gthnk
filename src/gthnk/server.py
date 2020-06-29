# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import time
import json
import flask
import logging
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, DateTimeField

from datetime import timedelta
from flaskext.markdown import Markdown
from mdx_linkify.mdx_linkify import LinkifyExtension
from mdx_journal import JournalExtension

from .models import Entry, Day, Page, User

log_filename = '../var/log/server.log'
print("logging to {}".format(log_filename))
logging.basicConfig(
    format='%(asctime)s %(module)-16s %(levelname)-8s %(message)s',
    filename=log_filename,
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
logging.info("Server: Start")

app = flask.Flask(__name__)
app.secret_key = b'_5#y3L"F4Q8z\n\xec]/'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = ".login"

Markdown(app)

class LoginForm(FlaskForm):
    access_code = StringField('Code',
        [validators.Length(min=7, max=7)],
        render_kw={"placeholder": "123-456"}
    )
    submit_button = SubmitField("Login")


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/task/<path:path>/', methods = ['GET'])
@login_required
def task_index(path):
    available_task_list = [
        'welcome',
        'calibration',
        'exposure',
        'sound-to-spelling',
        'spelling-to-sound',
        'deadline-naming',
        'finish-final'
    ]

    if path in available_task_list:
        logging.info("{participant} Task '{task}': starting".format(participant=current_user, task=path))
        return flask.render_template('tasks/{}.html.j2'.format(path))
    else:
        logging.warn("task not found: {}".format(path))
        return flask.abort(404)



# admin.add_view(DayAdmin(
#     Day,
#     db.session,
#     name="Days",
#     category="Admin"))

# admin.add_view(PageAdmin(
#     Page,
#     db.session,
#     name="Pages",
#     category="Admin"))

# admin.add_view(EntryAdmin(
#     Entry,
#     db.session,
#     name="Entries",
#     category="Admin"))

# admin.add_view(JournalExplorer(name="Journal", endpoint="journal"))


###
# Index

@app.route('/')
def index():
    return flask.render_template('index.html.j2')
