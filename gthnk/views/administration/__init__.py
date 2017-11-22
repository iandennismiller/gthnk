# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import flask
import flask_security as security
from flask_admin import expose
from flask_diamond.facets.administration import AuthModelView, AdminIndexView
from wtforms.fields import TextAreaField
from flask_admin.form.upload import FileUploadField

adminbaseview = flask.Blueprint(
    'adminbaseview',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/admin',
    )


class RedirectView(AdminIndexView):
    def is_visible(self):
        return False

    def is_accessible(self):
        return security.current_user.is_authenticated()

    @expose('/')
    def index(self):
        return flask.redirect(flask.url_for('journal.latest_view'))


class EntryAdmin(AuthModelView):
    def is_visible(self):
        return security.current_user.has_role('Admin')

    def is_accessible(self):
        return security.current_user.has_role('User')

    can_create = False
    can_delete = False
    can_edit = True
    column_display_pk = True

    list_template = 'journal_explorer/entry_list.html'

    column_list = ["timestamp", "content"]
    column_sortable_list = (('timestamp', 'timestamp'))
    column_searchable_list = ['content']

    form_overrides = dict(content=TextAreaField)
    form_excluded_columns = 'day'
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
            # "validators": [binary_validation]
        }
    }
    # form = PageForm
