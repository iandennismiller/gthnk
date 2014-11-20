# -*- coding: utf-8 -*-
# topcolors (c) 2013 Ian Dennis Miller

import flask
from flask.ext.admin import expose
import flask.ext.security as security
from flask.ext.diamond.administration import AuthModelView, AuthView, AdminIndexView
from Gthnk.Models.Day import latest
from flask.ext.admin.form import rules
from wtforms.fields import TextAreaField

adminbaseview = flask.Blueprint('adminbaseview', __name__, template_folder='templates', static_folder='static')

class SearchView(AdminIndexView):
    def is_accessible(self):
        return security.current_user.is_authenticated()

    @expose('/')
    def index(self):
        return self.render("admin/search.html", latest=latest())

class EntryAdmin(AuthModelView):
    def is_visible(self):
        return False

    can_create = False
    can_delete = False
    can_edit = True
    column_display_pk = True

    list_template = 'explorer/entry_list.html'

    column_list=["timestamp", "content"]
    column_filters = ['timestamp']
    column_sortable_list = (('timestamp', 'timestamp'))
    column_searchable_list = ['content']

    form_overrides = dict(content=TextAreaField)
    form_excluded_columns = 'day'
    form_widget_args = {
        'content':{
            'rows': 15
        }
    }
