# -*- coding: utf-8 -*-
# greenthink-library (c) 2013 Ian Dennis Miller

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask.ext.diamond import Diamond, db, toolbar, security
import Models
from datetime import timedelta
from flask.ext.mail import Mail
from flask.ext.markdown import Markdown
from mdx_linkify.mdx_linkify import LinkifyExtension
from mdx_journal import JournalExtension

class Gthnk(Diamond):
    def administration(self, app, db):
        from flask.ext.diamond.administration import AdminModelView, AuthenticatedMenuLink, MenuLink
        from .Views.Administration import Administration as A
        from .Views.Administration.JournalExplorer import JournalExplorer
        from .Views.Administration.ProjectExplorer import ProjectExplorer

        admin = super(Gthnk, self).administration(app, db, index_view=A.RedirectView(name="Home"))
        admin.add_view(A.EntryAdmin(Models.Entry, db.session, name="Entries"))
        admin.add_view(JournalExplorer(name="Journal", endpoint="journal"))
        admin.add_view(ProjectExplorer(name="Projects", endpoint="projects"))

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
    gthnk.md = Markdown(gthnk.app,
        extensions=[LinkifyExtension(), JournalExtension()])
    return gthnk.app
