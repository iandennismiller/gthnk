# -*- coding: utf-8 -*-
# gthnk (c) 2014 Ian Dennis Miller

import json, datetime
from flask.ext.admin import expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.security import current_user
from Gthnk import Models, security
from flask.ext.diamond.administration import AuthModelView, AuthView, AdminIndexView
from Gthnk.Models.Day import latest
import flask

class JournalExplorer(AuthView):
    def is_accessible(self):
        return current_user.is_authenticated()

    @expose('/')
    def index_view(self):
        return self.render("journal_explorer/search.html", latest=latest())

    @expose("/day/")
    def day_view(self):
        date_str = flask.request.args['date']
        if date_str is None:
            return flask.redirect(flask.url_for('admin.index'))

        day = Models.Day.find(date=datetime.datetime.strptime(date_str, "%Y-%m-%d").date())
        if day:
            return self.render('journal_explorer/day_view.html', day=day)
        else:
            return flask.redirect(flask.url_for('admin.index'))

    @expose("/latest")
    def latest_view(self):
        return self.render('journal_explorer/day_view.html', day=latest())
