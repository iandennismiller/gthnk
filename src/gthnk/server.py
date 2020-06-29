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
from flask.ext.markdown import Markdown
from mdx_linkify.mdx_linkify import LinkifyExtension
from mdx_journal import JournalExtension

from .models import Entry, Day, Page

application = None

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

class LoginForm(FlaskForm):
    access_code = StringField('Code',
        [validators.Length(min=7, max=7)],
        render_kw={"placeholder": "123-456"}
    )
    submit_button = SubmitField("Login")


@login_manager.user_loader
def load_user(user_id):
    return Participant(user_id)


class Gthnk(Diamond):
    def init_administration(self):
        from .views.journal_explorer import JournalExplorer
        from .views.administration import DayAdmin, PageAdmin, EntryAdmin

        admin = self.super("administration", user=User, role=Role, index_view="")

        admin.add_view(DayAdmin(
            Day,
            db.session,
            name="Days",
            category="Admin"))

        admin.add_view(PageAdmin(
            Page,
            db.session,
            name="Pages",
            category="Admin"))

        admin.add_view(EntryAdmin(
            Entry,
            db.session,
            name="Entries",
            category="Admin"))

        admin.add_view(JournalExplorer(name="Journal", endpoint="journal"))

    def init_blueprints(self):
        self.super("blueprints")

        from .views.diamond import diamond_blueprint
        self.app.register_blueprint(diamond_blueprint)

        from .views.journal_explorer import journal_blueprint
        self.app.register_blueprint(journal_blueprint)

        # administration blueprint is custom to this application
        from .views.administration import adminbaseview
        self.app.register_blueprint(adminbaseview)


def create_app():
    global application
    if not application:
        application = Gthnk()
        application.facet("configuration")
        application.facet("logs")
        application.facet("database")
        application.facet("marshalling")
        application.facet("blueprints")
        application.facet("accounts")
        application.facet("signals")
        application.facet("forms")
        application.facet("error_handlers")
        application.facet("request_handlers")
        application.facet("administration")
        # application.facet("rest", api_map=api_map)
        # application.facet("webassets")
        # application.facet("email")
        # application.facet("debugger")
        # application.facet("task_queue")

        application.app.permanent_session_lifetime = timedelta(minutes=30)
        application.app.logger.info("starting gthnk server")
        application.app.md = Markdown(application.app,
            extensions=[LinkifyExtension(), JournalExtension()])

    # print(application.app.url_map)
    return(application.app)
