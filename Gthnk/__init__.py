# -*- coding: utf-8 -*-
# greenthink-library (c) 2013 Ian Dennis Miller

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask.ext.diamond import Diamond, db, toolbar, security
import Models
from datetime import timedelta
from flask.ext.mail import Mail

class Gthnk(Diamond):
    def administration(self, app, db):
        from flask.ext.diamond.administration import AdminModelView, AuthenticatedMenuLink
        admin = super(Gthnk, self).administration(app, db)
        #admin.add_view(AdminModelView(Models.Entry, db.session, name="Entries", category="Journal"))
        #admin.add_view(AdminModelView(Models.Day, db.session, name="Days", category="Journal"))

        #from .Views.Administration.EntryExplorer import EntryExplorer
        #admin.add_view(EntryExplorer(db.session, name="Explorer", endpoint="explorer"))

        from .Views.Administration.DayExplorer import DayExplorer
        admin.add_view(DayExplorer(db.session, name="Days", endpoint="days"))

    def blueprints(self, app):
        from .Views.Administration.Administration import adminbaseview
        app.register_blueprint(adminbaseview, url_prefix="/")

def create_app():
    gthnk = Gthnk(db, security, toolbar)
    gthnk.init_app()
    gthnk.logger(gthnk.app)
    gthnk.app.permanent_session_lifetime = timedelta(minutes=30)
    return gthnk.app
