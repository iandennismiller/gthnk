# -*- coding: utf-8 -*-
# greenthink-library (c) 2013 Ian Dennis Miller

from __future__ import with_statement
from flask import Flask, request, jsonify, send_from_directory, abort, session, render_template, send_file, redirect
import json, sys, glob, csv, time, datetime, string, random, re, os, codecs

from GT import app
from flask.ext.security import login_required
from GT.dashboard.IdeaListsWidget import IdeaListsWidget
from GT.dashboard.TodoWidget import TodoWidget
from GT.dashboard.WorkWidget import WorkWidget

# this is really just for debugging on the local machine.
@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/get/<datestamp>')
def get_file(datestamp):
    auto_path = "/Users/idm/Library/Journal/auto"
    target_file = os.path.join(auto_path, "%s.txt" % datestamp)
    if os.path.exists(target_file):
        with open(target_file, "r") as f:
            buf = f.read()
    buf = re.sub(r"\n", "<br/>", buf)
    return render_template('article.html', buf=buf)

@app.route('/dashboard.json')
def dashboard_data():
    cache_name = "/tmp/dashboard.json"
    if os.path.exists(cache_name):
        mtime = os.stat(cache_name).st_mtime
        delta = datetime.datetime.now() - datetime.datetime.fromtimestamp(mtime)
        seconds = delta.seconds
    else:
        seconds = 99999

    # if the file is old and expired (i.e. more than 30 minutes)
    if seconds > 1800:
        app.logger.debug("rebuild")

        # todo
        app.logger.debug("start todo")
        todo = TodoWidget().render()
        app.logger.debug("finish todo")

        # work
        app.logger.debug("start work")
        work = WorkWidget().render()
        app.logger.debug("finish work")

        h = {
            "lists": IdeaListsWidget().render(),
            "todo": todo,
            "work": work,
        }
        with open(cache_name, "w") as f:
            buf = render_template('dashboard.json', dump=json.dumps(h, indent=4))
            f.write(buf)
    # otherwise just grab the saved copy
    else:
        app.logger.debug("cached")
        with open(cache_name, "r") as f:
            buf = f.read()
    return buf

@app.route('/search', methods=['POST', 'GET'])
def search_query():
    query = request.args.get('q', '')
    if not query:
        abort(400)
    results = []
    file_list = glob.glob("/Users/idm/Library/Journal/auto/*")
    file_list.reverse()
    file_list = ["/Users/idm/Library/Journal/journal.txt"] + file_list
    for filename in file_list:
        try:
            for line in codecs.open(filename, encoding='utf-8'):
                if query in line:
                    file_date, ext = os.path.splitext(os.path.basename(filename))
                    #output += out_tmpl % (file_date, line)
                    results.append([file_date, line])
        except UnicodeDecodeError:
            print filename + "ERROR"
    return render_template('results.html', results=results)

def search_query_ack(query):
    # grep for this term
    cmd = [
        '/usr/local/bin/ack',
        '-a',
        '-C3',
        '-i',
        query,
        "/Users/idm/Library/Journal/journal.txt",
        "/Users/idm/Library/Journal/auto",
    ]
    output = subprocess.check_output(cmd)
    output = re.sub("/Users/idm/Library/Journal/auto/", "", output)
    output = re.sub("\n", "<br/>\n", output)

    return "<div width='750px'>\n" + output + "</div>"
