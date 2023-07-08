import re
import os
import datetime
import flask

from gthnk.__meta__ import __version__
from ..app import gthnk


home = flask.Blueprint(
    'home',
    __name__,
    template_folder='templates',
    url_prefix='/'
)

@home.route('/config')
def config_view():
    "Render the config page."
    return flask.render_template('config.html.j2',
            configuration=flask.current_app.config,
            version=__version__,
            num_journal_days=len(gthnk.journal),
        )

@home.route('/')
def index():
    "Render the index page."
    return flask.render_template('index.html.j2')
