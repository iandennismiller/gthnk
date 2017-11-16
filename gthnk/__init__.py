# -*- coding: utf-8 -*-
# gthnk (c) 2014-2017 Ian Dennis Miller

from datetime import timedelta
from flask_diamond import Diamond
from flask_diamond.facets.administration import AdminModelView
from flask_diamond.facets.database import db
from flask.ext.markdown import Markdown
from mdx_linkify.mdx_linkify import LinkifyExtension
from mdx_journal import JournalExtension

from .models import User, Role, Entry, Day, Page

application = None


class Gthnk(Diamond):
    def init_administration(self):
        from .views.administration.journal_explorer import JournalExplorer
        from .views.administration import administration as A

        admin = self.super("administration", user=User, role=Role)

        admin.add_view(A.DayAdmin(
            Day,
            db.session,
            name="Days",
            category="Admin"))

        admin.add_view(A.PageAdmin(
            Page,
            db.session,
            name="Pages",
            category="Admin"))

        admin.add_view(A.EntryAdmin(
            Entry,
            db.session,
            name="Entries",
            category="Admin"))

        admin.add_view(JournalExplorer(name="Journal", endpoint="journal"))

    def init_blueprints(self):
        self.super("blueprints")

        # administration blueprint is custom to this application
        from .views.administration.administration import adminbaseview
        self.app.register_blueprint(adminbaseview)

        from .views.diamond import diamond_blueprint
        self.app.register_blueprint(diamond_blueprint)


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

    # print application.app.url_map
    return(application.app)
