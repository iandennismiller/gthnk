# (c) 2013 www.turkr.com

import json, datetime
from flask.ext.admin import expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.security import current_user
from Gthnk import Models, security
from Gthnk.Models.Day import latest

import flask

class JournalExplorer(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated()

    def is_visible(self):
        return False

    can_create = False
    can_delete = False
    can_edit = False
    column_list=["date"]#, "content"]
    column_filters = ['date']
    column_sortable_list = (('date', 'date'))

    list_template = 'journal_explorer/day_list.html'

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

    def __init__(self, session, **kwds):
        super(JournalExplorer, self).__init__(Models.Day, session, **kwds)
