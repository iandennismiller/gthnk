# -*- coding: utf-8 -*-
# gthnk (c) 2014 Ian Dennis Miller

import json, datetime, os
from flask.ext.admin import expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.security import current_user
from Gthnk import Models, security
from flask.ext.diamond.administration import AuthModelView, AuthView, AdminIndexView
from Gthnk.Adaptors.Projects import ProjectList
import flask

class ProjectExplorer(AuthView):
    def is_accessible(self):
        return current_user.is_authenticated()

    @expose("/")
    def index_view(self):
        project_list = ProjectList()
        list_columns=(('timestamp', 'timestamp'), ('name', 'name'))
        return self.render('project_explorer/project_list.html', data=project_list.get_recent(), list_columns=list_columns)

    @expose("/readme")
    def readme_view(self):
        project_name = flask.request.args['name']
        if project_name is None:
            return flask.redirect(flask.url_for('admin.index'))

        project_list = ProjectList()
        buf = project_list.get_readme(project_name)

        return self.render('project_explorer/readme_view.html', buf=buf, project_name=project_name)
