# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import datetime
import re
import flask
from sqlalchemy import desc
from flask_admin import expose
from flask_security import current_user
from flask_diamond.facets.administration import AuthView
from gthnk import db
from gthnk.models.day import Day, latest
from gthnk.models.entry import Entry
from gthnk.adaptors.librarian import Librarian


journal_blueprint = flask.Blueprint(
    'journal_blueprint',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/journal_explorer',
    )


class JournalExplorer(AuthView):
    def is_accessible(self):
        return(current_user.is_authenticated)

    @expose('/')
    def index_view(self):
        return flask.redirect(flask.url_for('.latest_view'))

    @expose("/refresh")
    def refresh(self):
        librarian = Librarian(flask.current_app)
        librarian.rotate_buffers()
        return flask.redirect(flask.url_for('.latest_view'))

    @expose("/nearest/<date>")
    def nearest_day_view(self, date):
        day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        if day:
            return flask.redirect(flask.url_for('.day_view', date=day.date))
        else:
            day = Day.query.order_by(Day.date).filter(Day.date > date).first()
            if day:
                return flask.redirect(flask.url_for('.day_view', date=day.date))
            else:
                day = Day.query.order_by(Day.date.desc()).filter(Day.date < date).first()
                if day:
                    return flask.redirect(flask.url_for('.day_view', date=day.date))
        # if no dates are found, redirect to home page
        return flask.redirect(flask.url_for('admin.index'))

    @expose("/day/<date>.html")
    def day_view(self, date):
        day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        if day:
            day_str = re.sub(r'(\d\d\d\d)', '<a name="\g<1>"></a>\n\g<1>', day.render())
            return self.render('journal_explorer/day_view.html', day=day, day_str=day_str)
        else:
            return flask.redirect(flask.url_for('admin.index'))

    @expose("/text/<date>.txt")
    def text_view(self, date):
        day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        if day:
            return day.render()
        else:
            return flask.redirect(flask.url_for('admin.index'))

    @expose("/markdown/<date>.md")
    def markdown_view(self, date):
        day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        if day:
            return day.render_markdown()
        else:
            return flask.redirect(flask.url_for('admin.index'))

    @expose("/latest.html")
    def latest_view(self):
        latest_day = latest()
        if latest_day:
            return self.render('journal_explorer/day_view.html',
                day=latest_day, day_str=latest_day.render())
        else:
            return self.render('journal_explorer/day_view.html',
                day=None, day_str="No entries yet")

    @expose("/search")
    def search_view(self):
        if not flask.request.args:
            return self.render("journal_explorer/search_view.html")
        else:
            query_str = flask.request.args['q']
            query = Entry.query.filter(
                Entry.content.contains(query_str)).order_by(desc(Entry.timestamp))
            results = query.all()[:20]
            for idx in range(0, len(results)):
                results[idx].content = re.sub(query_str, "**{}**".format(
                    query_str.upper()), results[idx].content, flags=re.I)
            return self.render('journal_explorer/results_list.html', data=results,
                count=query.count())

    @expose("/inbox/<date>", methods=['POST'])
    def upload_file(self, date):
        day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        file_handle = flask.request.files['file']
        if day and file_handle:
            day.attach(file_handle.read())
        return flask.redirect(flask.url_for('.day_view', date=date))

    @expose("/download/<date>.pdf")
    def download(self, date):
        day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        if day:
            response = flask.make_response(day.render_pdf())
            response.headers['Content-Type'] = 'application/pdf'
            disposition_str = 'attachment; filename="{0}.pdf"'.format(day.date)
            response.headers['Content-Disposition'] = disposition_str
            return response
        else:
            return flask.redirect(flask.url_for('.day_view', date=date))

    @expose("/thumbnail/<date>-<sequence>.jpg")
    def thumbnail(self, date, sequence):
        day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        page = day.pages[int(sequence)]
        response = flask.make_response(page.thumbnail)
        response.headers['Content-Type'] = 'image/jpeg'
        return response

    @expose("/preview/<date>-<sequence>.jpg")
    def preview(self, date, sequence):
        day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        page = day.pages[int(sequence)]
        response = flask.make_response(page.preview)
        response.headers['Content-Type'] = 'image/jpeg'
        return response

    @expose("/attachment/<date>-<sequence>.<extension>")
    def attachment(self, date, sequence, extension):
        day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        page = day.pages[int(sequence)]
        response = flask.make_response(page.binary)
        response.headers['Content-Type'] = page.content_type()
        response.headers['Content-Disposition'] = 'inline; filename="{0}"'.format(page.filename())
        return response

    @expose("/day/<date>/attachment/<sequence>/move_up")
    def move_page_up(self, date, sequence):
        if int(sequence) > 0:
            day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
            active_page = day.pages.pop(int(sequence))
            day.pages.reorder()
            day.pages.insert(int(sequence)-1, active_page)
            day.pages.reorder()
            db.session.commit()
        return flask.redirect(flask.url_for('.day_view', date=date))

    @expose("/day/<date>/attachment/<sequence>/move_down")
    def move_page_down(self, date, sequence):
        day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        if int(sequence) < len(day.pages)-1:
            active_page = day.pages.pop(int(sequence))
            day.pages.reorder()
            day.pages.insert(int(sequence)+1, active_page)
            day.pages.reorder()
            db.session.commit()
        return flask.redirect(flask.url_for('.day_view', date=date))

    @expose("/day/<date>/attachment/<sequence>/delete")
    def delete_page(self, date, sequence):
        day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        idx = int(sequence)
        active_page = day.pages.pop(idx)
        active_page.delete()
        db.session.commit()
        return flask.redirect(flask.url_for('.day_view', date=date))
