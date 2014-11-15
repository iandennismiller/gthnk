# -*- coding: utf-8 -*-
# greenthink-library (c) 2013 Ian Dennis Miller

from __future__ import with_statement
from flask import Flask, request, jsonify, send_from_directory, abort, session, render_template, send_file, redirect, flash, url_for
import json, sys, glob, csv, time, datetime, string, random, re, os

from GT import app
from GT.database import init_db, db_session, drop_tables
import GT.models as Models

from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm

@app.route('/account/')
def account_index():
    return redirect(url_for('login'))

@app.route('/account/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Models.User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=False)
            flash("Logged in successfully.")
            app.logger.info("log in {0}".format(user))
            app.logger.info("redirect to {0}".format(url_for("login")))
            return redirect(request.args.get("next") or url_for("index"))
        else:
            flash("Login unsuccessful.")
    elif request.method == 'POST':
        flash("Login unsuccessful.")
    return render_template("account/login.html", form=form)

@app.route('/account/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out')
    return redirect(url_for('login'))