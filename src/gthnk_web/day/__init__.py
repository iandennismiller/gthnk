import os
import re
import flask
import logging
import datetime
from flask_login import login_required
from gthnk.model.day import Day
from gthnk.model.journal import Journal
from gthnk.filetree.buffer import FileBuffer
from .j2_slugify import slugify, _slugify
from ..app import gthnk

day = flask.Blueprint('day',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/day'
)

day.add_app_template_filter(slugify)


@day.route("nearest/<date>")
@login_required
def nearest_day_view(date):
    datestamp = str(datetime.datetime.strptime(date, "%Y-%m-%d").date())
    day = gthnk.journal.get_day(datestamp)

    # if content exists, then the day exists
    if len(day.entries) > 0:
        return flask.redirect(flask.url_for('day.day_view', date=day.datestamp))
    else:
        # find the index of the first date that is larger
        datestamp_list = sorted(list(gthnk.journal.days.keys()))
        try:
            day_index = next(idx for idx, value in enumerate(datestamp_list) if value > date)
            datestamp = datestamp_list[day_index]
        except StopIteration:
            # or try to find the first one that is smaller
            datestamp_list = list(reversed(datestamp_list))
            try:
                day_index = next(idx for idx, value in enumerate(datestamp_list) if value < date)
                datestamp = datestamp_list[day_index]
            except StopIteration:
                return flask.redirect(flask.url_for('gthnk.index'))

        # if content exists, then the day exists
        day = gthnk.journal.days[datestamp]
        if 'entries' in day.__dict__ and len(day.entries) > 0:
            return flask.redirect(flask.url_for('day.day_view', date=day.datestamp))
        else:
            datestamp_list = sorted(list(gthnk.journal.days.keys()))
            breakpoint()
            day_index = next(idx for idx, value in enumerate(datestamp_list) if value < date)
            datestamp = datestamp_list[day_index]
            if day:
                return flask.redirect(flask.url_for('day.day_view', date=day.datestamp))

    # if no dates are found, redirect to home page
    return flask.redirect(flask.url_for('gthnk.index'))


@day.route("latest")
@login_required
def latest_view():
    datestamp = gthnk.journal.get_latest_datestamp()
    if datestamp:
        return flask.redirect(flask.url_for('day.day_view', date=datestamp))
    else:
        return flask.render_template('day-view.html.j2',
            day=None, day_str="No entries yet")


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


@day.route("latest.json")
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


@day.route("live")
@login_required
def buffer_view():

    j = Journal()
    for buffer in gthnk.buffers:
        fb = FileBuffer(buffer, journal=j)

    date = datetime.datetime.today().strftime('%Y-%m-%d')

    buffer_str = j.__repr__()
    day_md = render_day_pipeline(buffer_str)

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_of_week = days[datetime.datetime.strptime(date, "%Y-%m-%d").weekday()]

    return flask.render_template(
        'day-view.html.j2',
        date=date,
        day=None,
        day_str=day_md,
        day_of_week=day_of_week,
        is_buffer=True,
    )


@day.route("<date>.html")
@login_required
def day_view(date):
    day = gthnk.journal.get_day(date)
    # if there is any content, this day exists
    if len(day.entries) > 0:
        day_str = day.__repr__()
        day_md = render_day_pipeline(day_str)

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_of_week = days[datetime.datetime.strptime(date, "%Y-%m-%d").weekday()]

        return flask.render_template(
            'day-view.html.j2',
            date=date,
            day=day,
            day_str=day_md,
            day_of_week=day_of_week,
        )
    else:
        return flask.redirect(flask.url_for('.nearest_day_view', date=date))


@day.route("<date>.txt")
@login_required
def text_view(date):
    day = gthnk.journal.get_day(date)
    if day:
        return str(day)
    else:
        return flask.redirect(flask.url_for('gthnk.index'))
