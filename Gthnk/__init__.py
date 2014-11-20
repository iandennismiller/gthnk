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

class Gthnk(Diamond):
    def administration(self, app, db):
        from flask.ext.diamond.administration import AdminModelView, AuthenticatedMenuLink
        from .Views.Administration import Administration as A

        admin = super(Gthnk, self).administration(app, db, index_view=A.SearchView(name="Home"))
        #admin = super(Gthnk, self).administration(app, db)
        #admin.index_view=A.SearchView(name="Home")

        #admin.add_view(A.SearchView(name="Search"))
        admin.add_view(A.EntryAdmin(Models.Entry, db.session, name="Entries"))
        #admin.add_view(A.DayAdmin(Models.Day, db.session, name="Days", category="Model"))

        #from .Views.Administration.EntryExplorer import EntryExplorer
        #admin.add_view(EntryExplorer(db.session, name="Explorer", endpoint="explorer"))

        from .Views.Administration.DayExplorer import DayExplorer
        admin.add_view(DayExplorer(db.session, name="Journal", endpoint="journal"))

    def blueprints(self, app):
        from .Views.Administration.Administration import adminbaseview
        app.register_blueprint(adminbaseview)

        from .Views.Frontend.Workspace import workspace
        app.register_blueprint(workspace)

def create_app():
    gthnk = Gthnk(db, security, toolbar)
    gthnk.init_app()
    gthnk.logger(gthnk.app)
    gthnk.app.permanent_session_lifetime = timedelta(minutes=30)
    gthnk.md = Markdown(gthnk.app, extensions=['fenced_code'])
    return gthnk.app
