# -*- coding: utf-8 -*-
# gthnk (c) 2014 Ian Dennis Miller

import datetime
import re
import flask
from sqlalchemy import desc
from flask.ext.admin import expose
from flask.ext.security import current_user
from flask.ext.diamond.administration import AuthView
from Gthnk import Models, db, cache
from Gthnk.Models.Day import latest
from wand.image import Image


class JournalExplorer(AuthView):
    def is_accessible(self):
        return current_user.is_authenticated()

    @expose('/')
    def index_view(self):
        return self.render("journal_explorer/search_view.html")

    @expose("/day/<date>.html")
    def day_view(self, date):
        day = Models.Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        if day:
            day_str = re.sub(r'(\d\d\d\d)', '<a name="\g<1>"></a>\n\g<1>', day.render())
            return self.render('journal_explorer/day_view.html', day=day, day_str=day_str)
        else:
            return flask.redirect(flask.url_for('admin.index'))

    @expose("/latest.html")
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

    @expose("/inbox/<date>", methods=['POST'])
    def upload_file(self, date):
        day = Models.Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        file_handle = flask.request.files['file']
        if day and file_handle:
            f = file_handle.read()
            page = Models.Page.create(day=day, binary=f)
            day.pages.append(page)
            db.session.commit()
            return flask.redirect(flask.url_for('.day_view', date=date))

    @cache.cached(timeout=300)
    @expose("/attachment/thumb/<date>-<sequence>.png")
    def thumb_pdf(self, date, sequence):
        day = Models.Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        with Image(blob=day.pages[int(sequence)].binary) as img:
            img.format = 'png'
            img.transform(resize='150x200>')
            response = flask.make_response(img.make_blob())
            response.headers['Content-Type'] = 'image/png'
            return response

    @cache.cached(timeout=300)
    @expose("/attachment/full/<date>-<sequence>.png")
    def full_pdf(self, date, sequence):
        day = Models.Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        with Image(blob=day.pages[int(sequence)].binary) as img:
            img.format = 'png'
            img.transform(resize='612x792>')
            response = flask.make_response(img.make_blob())
            response.headers['Content-Type'] = 'image/png'
            return response

    @cache.cached(timeout=300)
    @expose("/attachment/<date>-<sequence>.pdf")
    def raw_pdf(self, date, sequence):
        day = Models.Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        raw = day.pages[int(sequence)].binary
        response = flask.make_response(raw)
        response.headers['Content-Type'] = 'application/pdf'
        disposition_str = 'inline; filename="{0}-{1}.pdf"'
        response.headers['Content-Disposition'] = disposition_str.format(date, sequence)
        return response

    @cache.cached(timeout=300)
    @expose("/attachment/<date>-<sequence>.jpg")
    def raw_jpeg(self, date, sequence):
        day = Models.Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        raw = day.pages[int(sequence)].binary
        response = flask.make_response(raw)
        response.headers['Content-Type'] = 'image/jpeg'
        disposition_str = 'inline; filename="{0}-{1}.jpg"'
        response.headers['Content-Disposition'] = disposition_str.format(date, sequence)
        return response

    @cache.cached(timeout=300)
    @expose("/attachment/<date>-<sequence>.png")
    def raw_png(self, date, sequence):
        day = Models.Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        raw = day.pages[int(sequence)].binary
        response = flask.make_response(raw)
        response.headers['Content-Type'] = 'image/png'
        disposition_str = 'inline; filename="{0}-{1}.png"'
        response.headers['Content-Disposition'] = disposition_str.format(date, sequence)
        return response

    @cache.cached(timeout=300)
    @expose("/attachment/raw/<date>-<sequence>")
    def raw_binary(self, date, sequence):
        day = Models.Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        raw = day.pages[int(sequence)].binary
        with Image(blob=raw) as img:
            if img.format == "JPEG":
                return flask.redirect(flask.url_for('.raw_jpeg', date=date, sequence=sequence))
            elif img.format == "PDF":
                return flask.redirect(flask.url_for('.raw_pdf', date=date, sequence=sequence))
            elif img.format == "PNG":
                return flask.redirect(flask.url_for('.raw_png', date=date, sequence=sequence))

    @expose("/day/<date>/attachment/<sequence>/move_up")
    def move_page_up(self, date, sequence):
        if int(sequence) > 0:
            day = Models.Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
            active_page = day.pages.pop(int(sequence))
            day.pages.reorder()
            day.pages.insert(int(sequence)-1, active_page)
            day.pages.reorder()
            db.session.commit()
            cache.clear()
        return flask.redirect(flask.url_for('.day_view', date=date))

    @expose("/day/<date>/attachment/<sequence>/move_down")
    def move_page_down(self, date, sequence):
        day = Models.Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        if int(sequence) < len(day.pages)-1:
            active_page = day.pages.pop(int(sequence))
            day.pages.reorder()
            day.pages.insert(int(sequence)+1, active_page)
            day.pages.reorder()
            db.session.commit()
            cache.clear()
        return flask.redirect(flask.url_for('.day_view', date=date))

    @expose("/day/<date>/attachment/<sequence>/delete")
    def delete_page(self, date, sequence):
        day = Models.Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        active_page = day.pages.pop(int(sequence))
        active_page.delete()
        db.session.commit()
        cache.clear()
        return flask.redirect(flask.url_for('.day_view', date=date))
