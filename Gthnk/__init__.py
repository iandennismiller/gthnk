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
        admin.add_view(AdminModelView(Models.Entry, db.session, name="Entries", category="Journal"))

        from .Views.Administration.EntryExplorer import EntryExplorer
        admin.add_view(EntryExplorer(db.session, name="Explorer", endpoint="explorer"))

        #admin.add_view(adminViews.StatusView(name="Status"))
        #admin.add_view(adminViews.UserAdmin(db.session))
        #admin.add_view(adminViews.AssetAdmin(db.session))

def create_app():
    gthnk = Gthnk(db, security, toolbar)
    gthnk.init_app()
    gthnk.logger(gthnk.app)
    gthnk.app.permanent_session_lifetime = timedelta(minutes=30)
    return gthnk.app
