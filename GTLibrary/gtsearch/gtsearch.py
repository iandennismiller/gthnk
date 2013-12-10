#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import subprocess, re, glob, codecs, os

from flask import Flask, render_template, request, abort
app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get/<datestamp>')
def get_file():
    return render_template('index.html')

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
