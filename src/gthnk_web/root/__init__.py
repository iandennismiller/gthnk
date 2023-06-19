import flask

root = flask.Blueprint(
    'root',
    __name__,
    template_folder='templates',
    static_folder='static',
)
