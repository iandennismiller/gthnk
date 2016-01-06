# -*- coding: utf-8 -*-
# gthnk (c) 2014-2016 Ian Dennis Miller

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask.ext.diamond import Diamond, db, security
from datetime import timedelta
from flask.ext.markdown import Markdown
from flask.ext.cache import Cache
from mdx_linkify.mdx_linkify import LinkifyExtension
from mdx_journal import JournalExtension

app_instance = None
cache = Cache(config={'CACHE_TYPE': 'simple'})

assert security


class Gthnk(Diamond):
    def administration(self):
        from flask.ext.diamond.administration import AuthenticatedMenuLink
        from .views.administration import administration as A
        from .views.administration.journal_explorer import JournalExplorer
        from .views.administration.project_explorer import ProjectExplorer
        from .views.administration.list_explorer import ListExplorer

        admin = super(Gthnk, self).administration()

        from models.entry import Entry
        admin.add_view(A.EntryAdmin(
            Entry,
            db.session,
            name="Entries",
            category="Admin"))

        from models.day import Day
        admin.add_view(A.DayAdmin(
            Day,
            db.session,
            name="Days",
            category="Admin"))

        from models.item_list import ItemList
        admin.add_view(A.ItemListAdmin(
            ItemList,
            db.session,
            name="ItemList",
            category="Admin"))

        from models.page import Page
        admin.add_view(A.PageAdmin(
            Page,
            db.session,
            name="Pages",
            category="Admin"))

        admin.add_view(JournalExplorer(name="Journal", endpoint="journal"))
        admin.add_view(ProjectExplorer(name="Projects", endpoint="projects"))
        admin.add_view(ListExplorer(name="Lists", endpoint="lists"))

        list_list = [
            "domain-list",
            "gifts",
            "media",
            "org-chart",
            "radar",
            "someday",
            "tech-to-research",
            "themes",
            "wanna"
        ]

        for name in list_list:
            admin.add_link(AuthenticatedMenuLink(
                name=name,
                url="/admin/lists/{}/items".format(name),
                category="Lists"))

    def blueprints(self):
        from flask_diamond.views.diamond import diamond_blueprint
        self.app.register_blueprint(diamond_blueprint)

        from .views.administration.administration import adminbaseview
        self.app.register_blueprint(adminbaseview)


def create_app():
    global app_instance
    if not app_instance:
        app_instance = Gthnk()
        app_instance.init_app(email=False, request_handlers=False)
        app_instance.app.permanent_session_lifetime = timedelta(minutes=30)
        app_instance.app.logger.info("starting gthnk server")
        app_instance.app.md = Markdown(app_instance.app,
            extensions=[LinkifyExtension(), JournalExtension()])
        cache.init_app(app_instance.app)

    # print app_instance.app.url_map
    return app_instance.app
