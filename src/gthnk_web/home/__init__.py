import re
import os
import flask
import datetime

from sqlalchemy import desc
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, validators

from ..app import gthnk

home = flask.Blueprint(
    'home',
    __name__,
    template_folder='templates',
    url_prefix='/'
)

class NoteForm(FlaskForm):
    entry = TextAreaField('Entry',
        validators=[validators.DataRequired()],
        render_kw={
            'class': 'form-control rounded-0',
            'rows': 5
        }
    )
    save_button = SubmitField("Save")

@home.route('/config')
@login_required
def config_view():
    return flask.render_template('config.html.j2',
            configuration=flask.current_app.config
        )


@home.route("/search")
@login_required
def search_view():
    if not flask.request.args:
        return flask.redirect(flask.url_for("gthnk.index"))
    else:
        query_str = flask.request.args['q']
        if 'page' in flask.request.args:
            page = int(flask.request.args['page'])
        else:
            page = 1

        matches = list(gthnk.journal.search(query_str))
        count = len(matches)

        per_page = 10
        start_id = (page - 1) * per_page
        end_id = start_id + per_page
        results = matches[start_id:end_id]

        return flask.render_template('search.html.j2',
            page=page,
            results=results,
            query_str=query_str,
            count=count
            )

###
# Index

@home.route('/')
def index():
    return flask.render_template('index.html.j2')
