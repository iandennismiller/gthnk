# -*- coding: utf-8 -*-
# greenthink-library (c) 2013 Ian Dennis Miller

from __future__ import with_statement
import flask
import json, sys, glob, csv, time, datetime, string, random, re, os, codecs
import markdown

workspace = flask.Blueprint('workspace', __name__, template_folder='templates', static_folder='static')

# @app.route('/')
# @login_required
# def index():
#     return render_template('index.html')

@workspace.route('/day/<datestamp>')
def get_file(datestamp):
    auto_path = "/Users/idm/Library/Journal/auto"
    target_file = os.path.join(auto_path, "%s.txt" % datestamp)
    if os.path.exists(target_file):
        with open(target_file, "r") as f:
            buf = f.read()
        #buf = markdown.markdown(buf, ['linkify', 'journal'])
        buf = markdown.markdown(buf, ['linkify', 'journal'])
    return flask.render_template('article.html', buf=buf)

@workspace.route('/project/<name>')
def get_project_readme(name):
    base_path = "/Users/idm/Work"
    target_file = os.path.join(base_path, name, "Readme.md")
    if os.path.exists(target_file):
        with open(target_file, "r") as f:
            buf = f.read()
        buf = markdown.markdown(buf, ['linkify', 'journal'])
    #buf = re.sub(r"\n", "<br/>", buf)
    return flask.render_template('article.html', buf=buf)
