# -*- coding: utf-8 -*-
# greenthink-library (c) 2013 Ian Dennis Miller

from __future__ import with_statement
from flask import Flask, request, jsonify, send_from_directory, abort, session, render_template, send_file, redirect
import json, sys, glob, csv, time, datetime, string, random, re, os

from GTLibrary import app
from flask.ext.security import login_required

# this is really just for debugging on the local machine.
@app.route('/')
@login_required
def index():
    return render_template('index.html')