# -*- coding: utf-8 -*-
# gthnk (c) 2014 Ian Dennis Miller

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask.ext.diamond import Diamond, db, toolbar, security
import Models
from datetime import timedelta
from flask.ext.markdown import Markdown
from flask.ext.cache import Cache
from mdx_linkify.mdx_linkify import LinkifyExtension
from mdx_journal import JournalExtension

cache = Cache(config={'CACHE_TYPE': 'simple'})


class Gthnk(Diamond):

    def administration(self, app, db):
        from flask.ext.diamond.administration import AuthenticatedMenuLink
        from .Views.Administration import Administration as A
        from .Views.Administration.JournalExplorer import JournalExplorer
        from .Views.Administration.ProjectExplorer import ProjectExplorer
        from .Views.Administration.ListExplorer import ListExplorer

        admin = super(Gthnk, self).administration(app, db, index_view=A.RedirectView(name="Home"))

        admin.add_view(A.EntryAdmin(
            Models.Entry,
            db.session,
            name="Entries",
            category="Admin"))

        admin.add_view(A.DayAdmin(
            Models.Day,
            db.session,
            name="Days",
            category="Admin"))

        admin.add_view(A.ItemListAdmin(
            Models.ItemList,
            db.session,
            name="ItemList",
            category="Admin"))

        admin.add_view(A.PageAdmin(
            Models.Page,
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

    def blueprints(self, app):
        #from .Views.Frontend.Workspace import workspace
        #app.register_blueprint(workspace)

        from .Views.Administration.Administration import adminbaseview
        app.register_blueprint(adminbaseview)


def create_app():
    gthnk = Gthnk(db, security, toolbar)
    gthnk.init_app()
    gthnk.logger(gthnk.app)
    gthnk.app.logger.info("starting gthnk server")
    gthnk.app.permanent_session_lifetime = timedelta(minutes=30)
    gthnk.app.md = Markdown(gthnk.app,
        extensions=[LinkifyExtension(), JournalExtension()])
    cache.init_app(gthnk.app)
    return gthnk.app
