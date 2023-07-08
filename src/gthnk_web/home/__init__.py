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


@home.route('/api/ask', methods=['GET'])
def api_ask():
    query = flask.request.args.get('q')
    if not query:
        return flask.jsonify({
            'error': 'no query',
            "result": None,
            "elapsed": None
        })

    # record the start time, in seconds
    start_time = datetime.datetime.now()
    result = gthnk.llm.ask(query)
    end_time = datetime.datetime.now()
    elapsed = end_time - start_time

    return flask.jsonify({
        'error': None,
        'result': result,
        'elapsed': elapsed.total_seconds()
    })
