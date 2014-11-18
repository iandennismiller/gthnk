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

class DayAdmin(AuthModelView):
    can_create = False
    can_delete = False
    can_edit = False
    column_display_pk = True

class EntryAdmin(AuthModelView):
    can_create = False
    can_delete = False
    can_edit = False
    column_display_pk = True

    list_template = 'explorer/entry_list.html'

    column_list=["timestamp", "content"]
    column_filters = ['timestamp']
    column_sortable_list = (('timestamp', 'timestamp'))
    column_searchable_list = ['content']
