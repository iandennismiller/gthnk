import os
import re
import flask
import logging
import datetime
from flask_login import login_required
from gthnk.model.day import Day
from gthnk.model.journal import Journal
from gthnk.filebuffer import FileBuffer
from ..jinja_slugify import slugify, _slugify
from ..server import gthnk

day = flask.Blueprint('day', __name__)

day.add_app_template_filter(slugify)


@day.route("/nearest/<date>")
@login_required
def nearest_day_view(date):
    day_id = str(datetime.datetime.strptime(date, "%Y-%m-%d").date())
    day = gthnk.journal.get_day(day_id)

    # if content exists, then the day exists
    if len(day.entries) > 0:
        return flask.redirect(flask.url_for('day.day_view', date=day.day_id))
    else:
        # find the index of the first date that is larger
        day_id_list = sorted(list(gthnk.journal.days.keys()))
        try:
            day_index = next(idx for idx, value in enumerate(day_id_list) if value > day_id)
        except StopIteration:
            try:
                day_index = next(idx for idx, value in enumerate(day_id_list) if value < day_id)
            except StopIteration:
                return flask.redirect(flask.url_for('gthnk.index'))
        
        day_id = day_id_list[day_index]

        # if content exists, then the day exists
        day = gthnk.journal.days[day_id]
        if 'content' in day.__dict__:
            return flask.redirect(flask.url_for('day.day_view', date=day.day_id))
        else:
            day_id_list = list(gthnk.journal.days.keys())
            day_index = next(x[0] for x in enumerate(day_id_list) if str(x[1]) < day_id)
            day_id = day_id_list[day_index]
            if day:
                return flask.redirect(flask.url_for('day.day_view', date=day.day_id))

    # if no dates are found, redirect to home page
    return flask.redirect(flask.url_for('gthnk.index'))


@day.route("/latest")
@login_required
def latest_view():
    day_id = gthnk.journal.get_latest_day_id()
    if day_id:
        return flask.redirect(flask.url_for('day.day_view', date=day_id))
    else:
        return flask.render_template('day-view.html.j2',
            day=None, day_str="No entries yet")


def extract_todo_items(day_md):
    todo_items = []

    regex = re.compile(r'\s*-\s*\[([\sxX])\]\s*(.+)$', re.MULTILINE)
    if day_md:
        for checked, item in regex.findall(day_md):
            todo_items.append((checked != ' ', item))

    return todo_items


def render_day_pipeline(day_str):
    # convert Markdown to string to avoid HTML escaping
    day_md = str(flask.current_app.markdown(day_str))

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


@day.route("/day/live/latest.json")
@login_required
def buffer_timestamp():
    input_files = flask.current_app.config["INPUT_FILES"]
    latest_time = 0

    for buffer_file in input_files.split(","):
        if os.path.isfile(buffer_file):
            mtime = os.path.getmtime(buffer_file)
            if mtime > latest_time:
                latest_time = mtime

    return {'timestamp': latest_time}


@day.route("/day/live")
@login_required
def buffer_view():

    j = Journal()
    for buffer in gthnk.buffers:
        fb = FileBuffer(buffer, journal=j)

    date = datetime.datetime.today().strftime('%Y-%m-%d')

    buffer_str = j.__repr__()
    todo_items = extract_todo_items(buffer_str)
    day_md = render_day_pipeline(buffer_str)

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_of_week = days[datetime.datetime.strptime(date, "%Y-%m-%d").weekday()]

    return flask.render_template(
        'day-view.html.j2',
        date=date,
        day=None,
        day_str=day_md,
        day_of_week=day_of_week,
        todo_items=todo_items,
        is_buffer=True,
    )


@day.route("/day/<date>.html")
@login_required
def day_view(date):
    day = gthnk.journal.get_day(date)
    # if there is any content, this day exists
    if len(day.entries) > 0:
        day_str = day.__repr__()
        todo_items = extract_todo_items(day_str)
        day_md = render_day_pipeline(day_str)

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_of_week = days[datetime.datetime.strptime(date, "%Y-%m-%d").weekday()]

        return flask.render_template(
            'day-view.html.j2',
            date=date,
            day=day,
            day_str=day_md,
            day_of_week=day_of_week,
            todo_items=todo_items,
        )
    else:
        return flask.redirect(flask.url_for('.nearest_day_view', date=date))


@day.route("/day/<date>.txt")
@login_required
def text_view(date):
    day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
    if day:
        return day.render()
    else:
        return flask.redirect(flask.url_for('gthnk.index'))


@day.route("/day/<date>.md")
@login_required
def markdown_view(date):
    day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
    if day:
        return day.render_markdown()
    else:
        return flask.redirect(flask.url_for('gthnk.index'))


@day.route("/day/<date>.pdf")
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
        return flask.redirect(flask.url_for('day.day_view', date=date))
