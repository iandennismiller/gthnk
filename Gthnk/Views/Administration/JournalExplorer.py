# -*- coding: utf-8 -*-
# gthnk (c) 2014 Ian Dennis Miller

import json, datetime, re
from flask.ext.admin import expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.security import current_user
from Gthnk import Models, security
from flask.ext.diamond.administration import AuthModelView, AuthView, AdminIndexView
from Gthnk.Models.Day import latest
from sqlalchemy import and_, desc
import flask

class JournalExplorer(AuthView):
    def is_accessible(self):
        return current_user.is_authenticated()

    @expose('/')
    def index_view(self):
        return self.render("journal_explorer/search_view.html")

    @expose("/day/<date>")
    def day_view(self, date):
        day = Models.Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        if day:
            day_str = re.sub(r'(\d\d\d\d)', '<a name="\g<1>"></a>\n\g<1>', unicode(day))
            return self.render('journal_explorer/day_view.html', day=day, day_str=day_str)
        else:
            return flask.redirect(flask.url_for('admin.index'))

    @expose("/latest")
    def latest_view(self):
        return self.render('journal_explorer/day_view.html', day=latest(), day_str=unicode(latest()))

    @expose("/search")
    def results_view(self):
        query_str = flask.request.args['q']
        if query_str is None:
            return flask.redirect(flask.url_for('admin.index'))

        query = Models.Entry.query.filter(Models.Entry.content.contains(query_str)).order_by(desc(Models.Entry.timestamp))
        results = query.all()[:20]
        for idx in range(0, len(results)):
            results[idx].content = re.sub(query_str, "**{}**".format(query_str.upper()), results[idx].content, flags=re.I)
        return self.render('journal_explorer/results_list.html', data=results, count=query.count())
