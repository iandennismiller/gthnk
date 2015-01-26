# -*- coding: utf-8 -*-
# gthnk (c) 2014 Ian Dennis Miller

import datetime
import re
import flask
from sqlalchemy import desc
from flask.ext.admin import expose
from flask.ext.security import current_user
from flask.ext.diamond.administration import AuthView
from Gthnk import Models, db
from Gthnk.Models.Day import latest
from wand.image import Image


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
            day_str = re.sub(r'(\d\d\d\d)', '<a name="\g<1>"></a>\n\g<1>', day.render())
            return self.render('journal_explorer/day_view.html', day=day, day_str=day_str)
        else:
            return flask.redirect(flask.url_for('admin.index'))

    @expose("/latest")
    def latest_view(self):
        return self.render('journal_explorer/day_view.html',
            day=latest(), day_str=latest().render())

    @expose("/search")
    def results_view(self):
        query_str = flask.request.args['q']
        if query_str is None:
            return flask.redirect(flask.url_for('admin.index'))

        query = Models.Entry.query.filter(
            Models.Entry.content.contains(query_str)).order_by(desc(Models.Entry.timestamp))
        results = query.all()[:20]
        for idx in range(0, len(results)):
            results[idx].content = re.sub(query_str, "**{}**".format(
                query_str.upper()), results[idx].content, flags=re.I)
        return self.render('journal_explorer/results_list.html', data=results, count=query.count())

    @expose("/day/<date>/upload", methods=['POST'])
    def upload_file(self, date):
        day = Models.Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        file_handle = flask.request.files['file']  # [0]
        if day and file_handle:
            f = file_handle.read()
            page = Models.Page.create(day=day, binary=f)
            day.pages.append(page)
            db.session.commit()
            return flask.redirect(flask.url_for('.day_view', date=date))

    @expose("/thumb/<date>-<sequence>.png")
    def thumb_pdf(self, date, sequence):
        day = Models.Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        with Image(blob=day.pages[int(sequence)].binary) as img:
            img.format = 'png'
            img.transform(resize='150x200>')
            response = flask.make_response(img.make_blob())
            response.headers['Content-Type'] = 'image/png'
            #response.headers['Content-Disposition'] = 'attachment; filename=img.png'
            return response

    @expose("/full/<date>-<sequence>.png")
    def full_pdf(self, date, sequence):
        day = Models.Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        with Image(blob=day.pages[int(sequence)].binary) as img:
            img.format = 'png'
            img.transform(resize='612x792>')
            response = flask.make_response(img.make_blob())
            response.headers['Content-Type'] = 'image/png'
            return response
