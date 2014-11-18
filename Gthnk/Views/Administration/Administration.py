# -*- coding: utf-8 -*-
# topcolors (c) 2013 Ian Dennis Miller

import flask
from flask.ext.admin import expose
from flask.ext.diamond.administration import AuthModelView, AuthView
#from Gthnk import Models

adminbaseview = flask.Blueprint('adminbaseview', __name__, template_folder='templates', static_folder='static')

#class StatusView(AuthView):
#    @expose('/')
#    def index(self):
#        return self.render("admin/status.html", Models=Models)
