import re
import flask
from sqlalchemy import desc
from flask_login import login_required
from ..models.entry import Entry
from ..librarian import Librarian

root = flask.Blueprint('gthnk', __name__)

@root.route("/search")
@login_required
def search_view():
    if not flask.request.args:
        return flask.redirect(flask.url_for("gthnk.index"))
    else:
        query_str = flask.request.args['q']
        query = Entry.query.filter(
            Entry.content.contains(query_str)).order_by(desc(Entry.timestamp))
        results = query.all()[:20]

        for idx in range(0, len(results)):
            results[idx].content = re.sub(query_str, "**{}**".format(
                query_str), results[idx].content, flags=re.I)

        return flask.render_template('explorer/results-list.html.j2',
            data=results,
            query_str=query_str,
            count=query.count()
            )

@root.route("/refresh")
@login_required
def refresh():
    librarian = Librarian(flask.current_app)
    librarian.rotate_buffers()
    return flask.redirect(flask.url_for('day.latest_view'))

###
# Index

@root.route('/')
def index():
    return flask.render_template('index.html.j2')
