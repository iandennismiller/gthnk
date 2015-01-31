# -*- coding: utf-8 -*-
# gthnk (c) 2014 Ian Dennis Miller

import flask
from flask.ext.admin import expose
import flask.ext.security as security
from flask.ext.diamond.administration import AuthModelView, AdminIndexView
from wtforms.fields import TextAreaField
from flask_admin.form.upload import FileUploadField

adminbaseview = flask.Blueprint('adminbaseview', __name__,
    template_folder='templates', static_folder='static')


class RedirectView(AdminIndexView):
    def is_visible(self):
        return False

    def is_accessible(self):
        return security.current_user.is_authenticated()

    @expose('/')
    def index(self):
        return flask.redirect(flask.url_for('journal.index_view'))


class EntryAdmin(AuthModelView):
    def is_visible(self):
        return security.current_user.has_role('Admin')

    can_create = False
    can_delete = False
    can_edit = True
    column_display_pk = True

    list_template = 'journal_explorer/entry_list.html'

    column_list = ["timestamp", "content"]
    column_filters = ['timestamp']
    column_sortable_list = (('timestamp', 'timestamp'))
    column_searchable_list = ['content']

    form_overrides = dict(content=TextAreaField)
    form_excluded_columns = 'day'
    form_widget_args = {
        'content': {
            'rows': 15
        }
    }


class ItemListAdmin(AuthModelView):
    def is_visible(self):
        return security.current_user.has_role('Admin')

    can_delete = True
    can_edit = True
    can_create = True
    column_display_pk = True
    column_list = ['name', 'content']

    form_overrides = dict(content=TextAreaField)
    form_widget_args = {
        'content': {
            'rows': 15
        }
    }


class DayAdmin(AuthModelView):
    def is_visible(self):
        return security.current_user.has_role('Admin')

    can_create = False
    can_delete = False
    can_edit = True
    column_display_pk = True


class PageAdmin(AuthModelView):
    def is_visible(self):
        return security.current_user.has_role('Admin')

    can_create = True
    can_delete = True
    can_edit = True
    column_display_pk = True

    form_excluded_columns = ['binary']
    column_list = ["day", "sequence", "extension", "title"]

    form_overrides = {
        "binary": FileUploadField
    }

    form_args = {
        'binary': {
            'label': 'File',
            'base_path': "/tmp",
            #"validators": [binary_validation]
        }
    }
    #form = PageForm
