import datetime

import logging

import flask
from flask_login import current_user, login_required

from ..server import gthnk

api = flask.Blueprint('api', __name__)


@api.route('/api/ask', methods=['GET'])
def ask_question():
    query = flask.request.args.get('q')
    if not query:
        return flask.jsonify({'error': 'no query', "result": None, "elapsed": None})

    # record the start time, in seconds
    start_time = datetime.datetime.now()
    result = gthnk.ask_llm(query)
    end_time = datetime.datetime.now()
    elapsed = end_time - start_time

    return flask.jsonify({'error': None, 'result': result, 'elapsed': elapsed.total_seconds()})
