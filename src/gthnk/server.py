# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import time
import json
import flask
import logging
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, DateTimeField

from datetime import timedelta
from flaskext.markdown import Markdown
from mdx_linkify.mdx_linkify import LinkifyExtension
from mdx_journal import JournalExtension

from .models.day import Day, latest
from .models.entry import Entry
from .models.page import Page
from .models.user import User
from .adaptors.librarian import Librarian

log_filename = '../var/log/server.log'
print("logging to {}".format(log_filename))
logging.basicConfig(
    format='%(asctime)s %(module)-16s %(levelname)-8s %(message)s',
    filename=log_filename,
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
logging.info("Server: Start")

app = flask.Flask(__name__)
app.secret_key = b'_5#y3L"F4Q8z\n\xec]/'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
# db.init_app(app)

login_manager = LoginManager(app)
# login_manager.init_app(app)
login_manager.login_view = ".login"

Markdown(app)

class LoginForm(FlaskForm):
    access_code = StringField('Code',
        [validators.Length(min=7, max=7)],
        render_kw={"placeholder": "123-456"}
    )
    submit_button = SubmitField("Login")


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route("/refresh")
def refresh(self):
    librarian = Librarian(flask.current_app)
    librarian.rotate_buffers()
    return flask.redirect(flask.url_for('.latest_view'))

@app.route("/nearest/<date>")
def nearest_day_view(date):
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

@app.route("/day/<date>.html")
def day_view(date):
    day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
    if day:
        day_str = re.sub(r'(\d\d\d\d)', '<a name="\g<1>"></a>\n\g<1>', day.render())
        return self.render('journal_explorer/day_view.html', day=day, day_str=day_str)
    else:
        return flask.redirect(flask.url_for('admin.index'))

@app.route("/text/<date>.txt")
def text_view(date):
    day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
    if day:
        return day.render()
    else:
        return flask.redirect(flask.url_for('admin.index'))

@app.route("/markdown/<date>.md")
def markdown_view(date):
    day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
    if day:
        return day.render_markdown()
    else:
        return flask.redirect(flask.url_for('admin.index'))

@app.route("/latest.html")
def latest_view(self):
    latest_day = latest()
    if latest_day:
        return self.render('journal_explorer/day_view.html',
            day=latest_day, day_str=latest_day.render())
    else:
        return self.render('journal_explorer/day_view.html',
            day=None, day_str="No entries yet")

@app.route("/search")
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

@app.route("/inbox/<date>", methods=['POST'])
def upload_file(date):
    day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
    file_handle = flask.request.files['file']
    if day and file_handle:
        day.attach(file_handle.read())
    return flask.redirect(flask.url_for('.day_view', date=date))

@app.route("/download/<date>.pdf")
def download(date):
    day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
    if day:
        response = flask.make_response(day.render_pdf())
        response.headers['Content-Type'] = 'application/pdf'
        disposition_str = 'attachment; filename="{0}.pdf"'.format(day.date)
        response.headers['Content-Disposition'] = disposition_str
        return response
    else:
        return flask.redirect(flask.url_for('.day_view', date=date))

@app.route("/thumbnail/<date>-<sequence>.jpg")
def thumbnail(date, sequence):
    day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
    page = day.pages[int(sequence)]
    response = flask.make_response(page.thumbnail)
    response.headers['Content-Type'] = 'image/jpeg'
    return response

@app.route("/preview/<date>-<sequence>.jpg")
def preview(date, sequence):
    day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
    page = day.pages[int(sequence)]
    response = flask.make_response(page.preview)
    response.headers['Content-Type'] = 'image/jpeg'
    return response

@app.route("/attachment/<date>-<sequence>.<extension>")
def attachment(date, sequence, extension):
    day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
    page = day.pages[int(sequence)]
    response = flask.make_response(page.binary)
    response.headers['Content-Type'] = page.content_type()
    response.headers['Content-Disposition'] = 'inline; filename="{0}"'.format(page.filename())
    return response

@app.route("/day/<date>/attachment/<sequence>/move_up")
def move_page_up(date, sequence):
    if int(sequence) > 0:
        day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        active_page = day.pages.pop(int(sequence))
        day.pages.reorder()
        day.pages.insert(int(sequence)-1, active_page)
        day.pages.reorder()
        db.session.commit()
    return flask.redirect(flask.url_for('.day_view', date=date))

@app.route("/day/<date>/attachment/<sequence>/move_down")
def move_page_down(date, sequence):
    day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
    if int(sequence) < len(day.pages)-1:
        active_page = day.pages.pop(int(sequence))
        day.pages.reorder()
        day.pages.insert(int(sequence)+1, active_page)
        day.pages.reorder()
        db.session.commit()
    return flask.redirect(flask.url_for('.day_view', date=date))

@app.route("/day/<date>/attachment/<sequence>/delete")
def delete_page(date, sequence):
    day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
    idx = int(sequence)
    active_page = day.pages.pop(idx)
    active_page.delete()
    db.session.commit()
    return flask.redirect(flask.url_for('.day_view', date=date))

###
# Index

@app.route('/')
def index():
    return flask.render_template('index.html.j2')
