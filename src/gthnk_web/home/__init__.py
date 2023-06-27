import re
import os
import datetime
import flask

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
            configuration=flask.current_app.config
        )

@home.route('/')
def index():
    "Render the index page."
    return flask.render_template('index.html.j2')
