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

class RedirectView(AdminIndexView):
    def is_accessible(self):
        return security.current_user.is_authenticated()

    @expose('/')
    def index(self):
        return flask.redirect(flask.url_for('journal.index_view'))

class EntryAdmin(AuthModelView):
    def is_visible(self):
        return False

    can_create = False
    can_delete = False
    can_edit = True
    column_display_pk = True

    list_template = 'journal_explorer/entry_list.html'

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

class ItemListAdmin(AuthModelView):
    can_delete = False
    can_edit = False
    can_create = False
    column_display_pk = True
    #form_excluded_columns = ['articles', 'snapshot']

