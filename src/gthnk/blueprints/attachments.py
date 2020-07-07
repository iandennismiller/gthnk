import flask
import datetime
from flask_login import login_required
from ..models.day import Day
from .. import db

attachments = flask.Blueprint('attachments', __name__)

@attachments.route("/inbox/<date>", methods=['POST'])
@login_required
def upload_file(date):
    day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
    file_handle = flask.request.files['file']
    if day and file_handle:
        day.attach(file_handle.read())
    return flask.redirect(flask.url_for('day.day_view', date=date))

@attachments.route("/thumbnail/<date>-<sequence>.jpg")
@login_required
def thumbnail(date, sequence):
    day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
    page = day.pages[int(sequence)]
    response = flask.make_response(page.thumbnail)
    response.headers['Content-Type'] = 'image/jpeg'
    return response

@attachments.route("/preview/<date>-<sequence>.jpg")
@login_required
def preview(date, sequence):
    day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
    page = day.pages[int(sequence)]
    response = flask.make_response(page.preview)
    response.headers['Content-Type'] = 'image/jpeg'
    return response

@attachments.route("/attachment/<date>-<sequence>.<extension>")
@login_required
def attachment(date, sequence, extension):
    day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
    page = day.pages[int(sequence)]
    response = flask.make_response(page.binary)
    response.headers['Content-Type'] = page.content_type()
    response.headers['Content-Disposition'] = 'inline; filename="{0}"'.format(page.filename())
    return response

@attachments.route("/day/<date>/attachment/<sequence>/move_up")
@login_required
def move_page_up(date, sequence):
    if int(sequence) > 0:
        day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
        active_page = day.pages.pop(int(sequence))
        day.pages.reorder()
        day.pages.insert(int(sequence)-1, active_page)
        day.pages.reorder()
        db.session.commit()
    return flask.redirect(flask.url_for('day.day_view', date=date))

@attachments.route("/day/<date>/attachment/<sequence>/move_down")
@login_required
def move_page_down(date, sequence):
    day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
    if int(sequence) < len(day.pages)-1:
        active_page = day.pages.pop(int(sequence))
        day.pages.reorder()
        day.pages.insert(int(sequence)+1, active_page)
        day.pages.reorder()
        db.session.commit()
    return flask.redirect(flask.url_for('day.day_view', date=date))

@attachments.route("/day/<date>/attachment/<sequence>/delete")
@login_required
def delete_page(date, sequence):
    day = Day.find(date=datetime.datetime.strptime(date, "%Y-%m-%d").date())
    idx = int(sequence)
    active_page = day.pages.pop(idx)
    active_page.delete()
    db.session.commit()
    return flask.redirect(flask.url_for('day.day_view', date=date))
