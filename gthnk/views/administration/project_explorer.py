# -*- coding: utf-8 -*-
# gthnk (c) 2014 Ian Dennis Miller
from flask.ext.admin import expose
from flask.ext.diamond.administration import AuthView
from flask.ext.security import current_user

from gthnk import cache
from gthnk.adaptors.projects import ProjectList


class ProjectExplorer(AuthView):
    def is_accessible(self):
        return current_user.is_authenticated()

    @expose("/")
    def index_view(self):
        project_list = ProjectList()
        list_columns = (('timestamp', 'timestamp'), ('name', 'name'))
        return self.render('project_explorer/project_list.html',
            data=project_list.get_recent(), list_columns=list_columns)

    @cache.cached(timeout=300)
    @expose("/<project_name>/readme")
    def readme_view(self, project_name):
        project_list = ProjectList()
        buf = project_list.get_readme(project_name)
        return self.render('project_explorer/readme_view.html', buf=buf, project_name=project_name)
