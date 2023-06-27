import re
import os
import flask
import datetime

from flask_login import login_required

from ..app import gthnk

home = flask.Blueprint(
    'home',
    __name__,
    template_folder='templates',
    url_prefix='/'
)

@home.route('/config')
@login_required
def config_view():
    return flask.render_template('config.html.j2',
            configuration=flask.current_app.config
        )

@home.route('/')
def index():
    return flask.render_template('index.html.j2')
