# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import re
import os
import time
import json
import flask
import logging
import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, DateTimeField

from sqlalchemy import desc

from datetime import timedelta
from mdx_linkify.mdx_linkify import LinkifyExtension
from mdx_journal import JournalExtension

from . import db, markdown, login_manager, create_app

from .models.day import Day, latest
from .models.entry import Entry
from .models.page import Page
from .models.user import User
from .adaptors.librarian import Librarian


app = create_app()


login_manager.login_view = ".login"


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(id=user_id)


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit_button = SubmitField("Login")


@app.route("/nearest/<date>")
@login_required
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
    return flask.redirect(flask.url_for('.index'))

@app.route("/latest")
@login_required
def latest_view():
    latest_day = latest()
    if latest_day:
        return flask.redirect(flask.url_for('day_view', date=latest_day.date))
    else:
        return flask.render_template('explorer/day-view.html.j2',
            day=None, day_str="No entries yet")

@app.route("/search")
@login_required
def search_view():
    if not flask.request.args:
        return flask.redirect(flask.url_for("index"))
    else:
        query_str = flask.request.args['q']
        query = Entry.query.filter(
            Entry.content.contains(query_str)).order_by(desc(Entry.timestamp))
        results = query.all()[:20]

        for idx in range(0, len(results)):
            results[idx].content = re.sub(query_str, "**{}**".format(
                query_str), results[idx].content, flags=re.I)

        return flask.render_template('explorer/results-list.html.j2',
            data=results,
            query_str=query_str,
            count=query.count()
            )

###
# Day Views

def extract_todo_items(day_md):
    todo_items = []

    regex = re.compile(r'\s*-\s*\[[\sxX]\]\s*(.+)$', re.MULTILINE)
    for group in regex.findall(day_md):
        todo_items.append(group)

    return todo_items

def render_day_pipeline(day_str):
    # convert Markdown to string to avoid HTML escaping
    day_md = str(markdown(day_str))

    # add anchors before timestamps
    regex = re.compile(r'^<p><h4>(\d\d\d\d)</h4></p>$', re.MULTILINE)
    replacement = r'\n<a class="anchor" name="\g<1>"></a>\n<p><h4>\g<1></h4></p>\n'
    day_md = regex.sub(replacement, day_md)

    # make tags searchable
    regex = re.compile(r'\[\[([\w\s]+)\]\]', re.MULTILINE)
    replacement = r'[[<a href="/search?q=\g<1>">\g<1></a>]]'
    day_md = regex.sub(replacement, day_md)

    # done processing, convert to Markup
    day_md = flask.Markup(regex.sub(replacement, day_md))

    return day_md


@app.route("/buffer")
@login_required
def buffer_view():
    date = datetime.datetime.today().strftime('%Y-%m-%d')

    input_files = app.config["INPUT_FILES"]

    buffer_str = ""
    for buffer_file in input_files.split(","):
        if os.path.isfile(buffer_file):
            with open(buffer_file, 'r') as f:
                buffer_str += f.read()
                buffer_str += "\n\n"

    todo_items = extract_todo_items(buffer_str)
    day_md = render_day_pipeline(buffer_str)

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_of_week = days[datetime.datetime.strptime(date, "%Y-%m-%d").weekday()]

    return flask.render_template(
        'explorer/day-view.html.j2',
        date=date,
        day=None,
        day_str=day_md,
        day_of_week=day_of_week,
        todo_items=todo_items,
        is_buffer=True,
    )

@app.route("/day/<date>.html")
@login_required
def day_view(date):

    day = Day.find(date=date)
    if day:
        day_str = day.render()
        todo_items = extract_todo_items(day_str)
        day_md = render_day_pipeline(day_str)

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_of_week = days[datetime.datetime.strptime(date, "%Y-%m-%d").weekday()]

        return flask.render_template(
            'explorer/day-view.html.j2',
            date=date,
            day=day,
            day_str=day_md,
            day_of_week=day_of_week,
            todo_items=todo_items,
        )
    else:
        return flask.redirect(flask.url_for('.index'))

@app.route("/day/<date>.txt")
@login_required
def text_view(date):
    day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
    if day:
        return day.render()
    else:
        return flask.redirect(flask.url_for('.index'))

@app.route("/day/<date>.md")
@login_required
def markdown_view(date):
    day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
    if day:
        return day.render_markdown()
    else:
        return flask.redirect(flask.url_for('.index'))

@app.route("/day/<date>.pdf")
@login_required
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

###
# Attachments

@app.route("/inbox/<date>", methods=['POST'])
@login_required
def upload_file(date):
    day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
    file_handle = flask.request.files['file']
    if day and file_handle:
        day.attach(file_handle.read())
    return flask.redirect(flask.url_for('.day_view', date=date))

@app.route("/thumbnail/<date>-<sequence>.jpg")
@login_required
def thumbnail(date, sequence):
    day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
    page = day.pages[int(sequence)]
    response = flask.make_response(page.thumbnail)
    response.headers['Content-Type'] = 'image/jpeg'
    return response

@app.route("/preview/<date>-<sequence>.jpg")
@login_required
def preview(date, sequence):
    day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
    page = day.pages[int(sequence)]
    response = flask.make_response(page.preview)
    response.headers['Content-Type'] = 'image/jpeg'
    return response

@app.route("/attachment/<date>-<sequence>.<extension>")
@login_required
def attachment(date, sequence, extension):
    day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
    page = day.pages[int(sequence)]
    response = flask.make_response(page.binary)
    response.headers['Content-Type'] = page.content_type()
    response.headers['Content-Disposition'] = 'inline; filename="{0}"'.format(page.filename())
    return response

@app.route("/day/<date>/attachment/<sequence>/move_up")
@login_required
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
@login_required
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
@login_required
def delete_page(date, sequence):
    day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
    idx = int(sequence)
    active_page = day.pages.pop(idx)
    active_page.delete()
    db.session.commit()
    return flask.redirect(flask.url_for('.day_view', date=date))

###
# Authentication

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user and current_user.is_authenticated:
        flask.flash('Already logged in.')
        return flask.redirect(flask.url_for('index'))

    # next_page = flask.request.args.get('next', '')

    form = LoginForm()
    if form.validate_on_submit():
        # convert access code to user id
        user = User.find(username=form.username.data)

        if user and user.password == form.password.data:
            login_user(user)
            logging.info("{user} logs in".format(user=current_user))
            flask.flash('Logged in successfully.')
            return flask.redirect(flask.url_for('index'))

    return flask.render_template('login.html.j2', form=form)

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    if current_user.is_authenticated:
        logging.info("{user} logs out".format(user=current_user))
        logout_user()
        flask.flash('You have successfully logged out.')
    return flask.redirect(flask.url_for('index'))

###
# Refresh Buffers

@app.route("/refresh")
@login_required
def refresh():
    librarian = Librarian(flask.current_app)
    librarian.rotate_buffers()
    return flask.redirect(flask.url_for('.latest_view'))

###
# Index

@app.route('/')
def index():
    return flask.render_template('index.html.j2')

