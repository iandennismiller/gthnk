import os
import re
import logging
import datetime

import flask

from gthnk.model.day import Day
from gthnk.model.journal import Journal
from gthnk.filetree.buffer import FileBuffer

from .j2_slugify import slugify, _slugify
from ..app import gthnk

days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

journal = flask.Blueprint('journal',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/journal'
)

journal.add_app_template_filter(slugify)

@journal.route("nearest/<date>")
def nearest_day(date):
    "Redirect to the nearest day."
    try:
        datestamp = str(datetime.datetime.strptime(date, "%Y-%m-%d").date())
    except ValueError:
        return flask.redirect(flask.url_for('.latest'))

    day = gthnk.journal.get_nearest_day(datestamp)
    if day:
        return flask.redirect(flask.url_for('.day_view', date=day.datestamp))
    return flask.redirect(flask.url_for('.latest'))

@journal.route("latest")
def latest():
    "Redirect to the latest day."
    datestamp = gthnk.journal.get_latest_datestamp()
    if datestamp:
        return flask.redirect(flask.url_for('.day_view', date=datestamp))
    return flask.render_template('day.html.j2', day=None, day_str="No entries yet")

@journal.route("/search")
def search_view():
    "Render the search page, handle search, and render results."
    if not flask.request.args:
        return flask.redirect(flask.url_for("home.index"))

    query_str = flask.request.args['q']
    if 'page' in flask.request.args:
        page = int(flask.request.args['page'])
    else:
        page = 1

    matches = list(gthnk.journal.search(query_str))
    count = len(matches)

    per_page = 10
    start_id = (page - 1) * per_page
    end_id = start_id + per_page
    results = matches[start_id:end_id]

    return flask.render_template('search.html.j2',
        page=page,
        results=results,
        query_str=query_str,
        count=count
        )

@journal.route("status.json")
def status_json():
    "Return the timestamp of the latest input file."
    input_files = flask.current_app.config["INPUT_FILES"]
    latest_time = 0.0

    for buffer_file in input_files.split(","):
        if os.path.isfile(buffer_file):
            mtime = os.path.getmtime(buffer_file)
            if mtime > latest_time:
                latest_time = mtime

    # check the filetree for any updates
    gthnk.filetree.read_journal()

    return {
        'timestamp': latest_time,
        'latest': gthnk.journal.get_latest_datestamp(),
    }

@journal.route("<date>.html")
def day_view(date):
    "View the specified day as HTML."
    return flask.render_template('day.html.j2', date=date)

@journal.route("<date>.json")
def day_json(date):
    day_struct = {}
    if date == "live":
        today = datetime.datetime.today()
        j = Journal()
        for buffer in gthnk.buffers:
            FileBuffer(buffer, journal=j).read()
        day_struct = {
            'datestamp': today.strftime('%Y-%m-%d'),
            'content': render_day_pipeline(str(j)),
            'day_of_week': days_of_week[today.weekday()],
            'yesterday': gthnk.journal.get_latest_datestamp(),
            'tomorrow': None,
        }
    else:
        day = gthnk.journal.get_day(date)
        if day:
            day_struct = {
                'datestamp': day.datestamp,
                'content': render_day_pipeline(str(day)),
                'day_of_week': days_of_week[datetime.datetime.strptime(date, "%Y-%m-%d").weekday()],
                'yesterday': day.yesterday.datestamp if day.yesterday else None,
                'tomorrow': day.tomorrow.datestamp if day.tomorrow else None,
            }
    if day_struct:
        return flask.jsonify(day_struct)

@journal.route("<date>.txt")
def text_view(date):
    "Render the day as plain text."
    day = gthnk.journal.get_day(date)
    if day:
        return str(day)
    return flask.redirect(flask.url_for('home.index'))

def render_day_pipeline(day_str):
    "Render the day string - first as markdown, then as html."

    # convert Markdown to string to avoid HTML escaping
    day_md = str(flask.current_app.markdown(day_str))

    # add anchors before timestamps
    regex = re.compile(r'^<p><h4>(\d\d\d\d)</h4></p>$', re.MULTILINE)
    replacement = r'\n<a class="anchor" name="\g<1>"></a>\n<p><h4>\g<1></h4></p>\n'
    day_md = regex.sub(replacement, day_md)

    # done processing, convert to Markup
    return flask.Markup(day_md)
