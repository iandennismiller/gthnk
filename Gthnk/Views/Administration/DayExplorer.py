# (c) 2013 www.turkr.com

import json, datetime
from flask.ext.admin import expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.security import current_user
from Gthnk import Models, security
from Gthnk.Models.Day import latest

import flask

class DayExplorer(ModelView):
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

    list_template = 'explorer/day_list.html'

    @expose("/day/")
    def day_view(self):
        date_str = flask.request.args['date']
        if date_str is None:
            return flask.redirect(flask.url_for('admin.index'))

        day = Models.Day.find(date=datetime.datetime.strptime(date_str, "%Y-%m-%d").date())
        if day:
            return self.render('explorer/day_view.html',day=day, latest=latest())
        else:
            return flask.redirect(flask.url_for('admin.index'))

    def __init__(self, session, **kwds):
        super(DayExplorer, self).__init__(Models.Day, session, **kwds)
