# -*- coding: utf-8 -*-
# greenthink-library (c) 2013 Ian Dennis Miller

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask

# set up the app
app = Flask(__name__)
app.secret_key = 'W\xdd\x0e\x86\xd8|.\x87\x7f\xc9\xa0\x03\xfdC\x84\xfa\xf9\xdf\xb2\xfc\xf9\x9d\xadI'
app.config.from_envvar('SETTINGS')
app.config['SECURITY_PASSWORD_HASH'] = 'sha256_crypt'
app.config['SECURITY_PASSWORD_SALT'] = '1hvrUIauwTJmahHg'

# set up the database
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
import models as Model

# Setup Flask-Security
from flask.ext.security import Security, SQLAlchemyUserDatastore
user_datastore = SQLAlchemyUserDatastore(db, Model.User, Model.Role)
security = Security(app, user_datastore)

# admin interface
from flask.ext.admin import Admin
import adminViews
admin = Admin(app, name='GTLibrary')
admin.add_view(adminViews.StatusView(name="Status"))
admin.add_view(adminViews.UserAdmin(db.session))
admin.add_view(adminViews.AssetAdmin(db.session))
admin.add_link(adminViews.AuthenticatedMenuLink(name='Logout', url='/logout'))
admin.add_link(adminViews.NotAuthenticatedMenuLink(name='Login', url='/login'))

# Setup Views
import GTLibrary.workViews

# init logging
import logging
handler = logging.FileHandler(app.config['LOG'])
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
app.logger.addHandler(handler)
app.logger.info('Startup with log: %s' % app.config['LOG'])
if app.config['LOG_LEVEL'] == "DEBUG":
    app.logger.setLevel(logging.DEBUG)
    app.logger.info('log level is DEBUG')
else:
    app.logger.setLevel(logging.INFO)