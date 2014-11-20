# -*- coding: utf-8 -*-
# greenthink-library (c) 2013 Ian Dennis Miller

from __future__ import with_statement
import flask
from flask.ext.security import login_required
import json, sys, glob, csv, time, datetime, string, random, re, os, codecs
from markdown import markdown
from sqlalchemy import and_, desc
from Gthnk import Models, security

workspace = flask.Blueprint('workspace', __name__, template_folder='templates', static_folder='static')

@workspace.route('/day/<datestamp>')
@login_required
def get_day(datestamp):
    try:
        date = datetime.datetime.strptime(datestamp, "%Y-%m-%d").date()
    except:
        flask.abort(404)

    day = Models.Day.find(date=date)
    yesterday = Models.Day.query.filter(Models.Day.date < day.date).order_by(desc(Models.Day.date)).first()
    tomorrow = Models.Day.query.filter(Models.Day.date > day.date).order_by(Models.Day.date).first()
    if day:
        return flask.render_template('day_view.html', content=unicode(day), yesterday=yesterday, tomorrow=tomorrow)
    else:
        flask.abort(404)

@workspace.route('/project/<name>')
@login_required
def get_project_readme(name):
    base_path = "/Users/idm/Work"
    target_file = os.path.join(base_path, name, "Readme.md")
    if os.path.exists(target_file):
        with open(target_file, "r") as f:
            buf = f.read()
        buf = markdown.markdown(buf, ['linkify', 'journal'])
    #buf = re.sub(r"\n", "<br/>", buf)
    return flask.render_template('article.html', buf=buf)
