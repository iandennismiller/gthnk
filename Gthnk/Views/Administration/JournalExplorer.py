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
from Gthnk.Librarian import Librarian
from wand.image import Image


class JournalExplorer(AuthView):
    def is_accessible(self):
        return current_user.is_authenticated()

    @expose('/')
    def index_view(self):
        return self.render("journal_explorer/search_view.html")

    @expose("/refresh")
    def refresh(self):
        librarian = Librarian(flask.current_app)
        librarian.rotate_buffers()
        return flask.redirect(flask.url_for('.latest_view'))

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
            with Image(blob=f) as img:
                img.format = 'png'

                thumbnail = img.clone()
                thumbnail.transform(resize='150x200>')

                preview = img.clone()
                preview.gaussian_blur(radius=2, sigma=0.5)
                preview.transform(resize='612x792>')

                page = Models.Page.create(
                    day=day,
                    binary=f,
                    thumbnail=thumbnail.make_blob(),
                    preview=preview.make_blob(),
                )
            day.pages.append(page)
            db.session.commit()
            return flask.redirect(flask.url_for('.day_view', date=date))

    @expose("/attachment/thumb/<date>-<sequence>.png")
    def thumb_pdf(self, date, sequence):
        day = Models.Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        page = day.pages[int(sequence)]
        if page.thumbnail:
            response = flask.make_response(page.thumbnail)
        else:
            with Image(blob=page.binary) as img:
                img.format = 'png'
                img.transform(resize='150x200>')
                page.thumbnail = img.make_blob()
                page.save()
                response = flask.make_response(page.thumbnail)
        response.headers['Content-Type'] = 'image/png'
        return response

    @expose("/attachment/full/<date>-<sequence>.png")
    def full_pdf(self, date, sequence):
        day = Models.Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        page = day.pages[int(sequence)]
        if page.preview:
            response = flask.make_response(page.preview)
        else:
            with Image(blob=day.pages[int(sequence)].binary) as img:
                img.format = 'png'
                img.transform(resize='612x792>')
                page.preview = img.make_blob()
                page.save()
                response = flask.make_response(page.preview)
        response.headers['Content-Type'] = 'image/png'
        return response

    @expose("/attachment/<date>-<sequence>.pdf")
    def raw_pdf(self, date, sequence):
        day = Models.Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        raw = day.pages[int(sequence)].binary
        response = flask.make_response(raw)
        response.headers['Content-Type'] = 'application/pdf'
        disposition_str = 'inline; filename="{0}-{1}.pdf"'
        response.headers['Content-Disposition'] = disposition_str.format(date, sequence)
        return response

    @expose("/attachment/<date>-<sequence>.jpg")
    def raw_jpeg(self, date, sequence):
        day = Models.Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        raw = day.pages[int(sequence)].binary
        response = flask.make_response(raw)
        response.headers['Content-Type'] = 'image/jpeg'
        disposition_str = 'inline; filename="{0}-{1}.jpg"'
        response.headers['Content-Disposition'] = disposition_str.format(date, sequence)
        return response

    @expose("/attachment/<date>-<sequence>.png")
    def raw_png(self, date, sequence):
        day = Models.Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        raw = day.pages[int(sequence)].binary
        response = flask.make_response(raw)
        response.headers['Content-Type'] = 'image/png'
        disposition_str = 'inline; filename="{0}-{1}.png"'
        response.headers['Content-Disposition'] = disposition_str.format(date, sequence)
        return response

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
        return flask.redirect(flask.url_for('.day_view', date=date))

    @expose("/day/<date>/attachment/<sequence>/delete")
    def delete_page(self, date, sequence):
        day = Models.Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        active_page = day.pages.pop(int(sequence))
        active_page.delete()
        db.session.commit()
        return flask.redirect(flask.url_for('.day_view', date=date))
