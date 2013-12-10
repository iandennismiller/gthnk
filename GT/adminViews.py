# -*- coding: utf-8 -*-
# greenthink-library (c) 2013 Ian Dennis Miller

from flask import Flask
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.base import MenuLink
from flask.ext.admin.contrib.sqlamodel import ModelView
from flask.ext.security import current_user
from GT import Model

class AuthView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated()

class AdminView(ModelView):
    def is_accessible(self):
        return current_user.has_role("Admin")

class AuthenticatedMenuLink(MenuLink):
    def is_accessible(self):
        return current_user.is_authenticated()

class NotAuthenticatedMenuLink(MenuLink):
    def is_accessible(self):
        return not current_user.is_authenticated()

class StatusView(BaseView):
    "This is an example of a normal Jinja page"
    def is_accessible(self):
        return current_user.is_authenticated()
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

class UserAdmin(AdminView):
    column_filters = ['email']
    column_searchable_list = ['email']
    column_exclude_list = ('_password')

    def __init__(self, session):
        # Just call parent class with predefined model.
        super(UserAdmin, self).__init__(Model.User, session)

class AssetAdmin(AuthView):
    can_create = False
    can_delete = False
    can_edit = False

    def __init__(self, session):
        super(AssetAdmin, self).__init__(Model.Asset, session)

class AssetProxyAdmin(AuthView):
    "This is a pattern for using the ID to render a separate view in an IFRAME"
    can_create = False
    can_delete = False

    class AssetEditForm(Form):
        id = fields.TextField('id')
    form = AssetEditForm
    edit_template = 'admin/model/asset.html'

    def __init__(self, session):
        super(AssetAdmin, self).__init__(Model.Asset, session)