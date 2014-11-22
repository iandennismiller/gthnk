# -*- coding: utf-8 -*-
# greenthink-library (c) 2013 Ian Dennis Miller

from __future__ import with_statement
import flask
from flask.ext.security import login_required
import json, sys, glob, csv, time, datetime, string, random, re, os, codecs
from markdown import markdown
from sqlalchemy import and_, desc
from Gthnk import Models, security
from Gthnk.Adaptors.Projects import ProjectList

workspace = flask.Blueprint('workspace', __name__, template_folder='templates', static_folder='static')

# @workspace.route('/projects')
# @login_required
# def get_project_list():
#     project_list = ProjectList()
#     return flask.render_template('results.html', results=project_list.get_recent_projects())
#     # return flask.render_template('project_list.html', files=project_list.get_recent_projects())

# @workspace.route('/project/<name>')
# @login_required
# def get_project_readme(name):
#     target_file = os.path.join(flask.current_app.config["PROJECT_PATH"], name, "Readme.md")
#     if os.path.exists(target_file):
#         with open(target_file, "r") as f:
#             buf = f.read()
#         buf = markdown.markdown(buf, ['linkify', 'journal'])
#     #buf = re.sub(r"\n", "<br/>", buf)
#     return flask.render_template('article.html', buf=buf)
