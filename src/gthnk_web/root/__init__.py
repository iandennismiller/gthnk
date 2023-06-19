import flask

root = flask.Blueprint(
    'root',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/'
)

@root.route('/')
def index():
    return flask.redirect(flask.url_for('home.index'))
