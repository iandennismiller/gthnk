import logging
import flask
from flask_wtf import FlaskForm
from flask_login import login_user, logout_user, current_user, login_required
from wtforms import StringField, PasswordField, SubmitField, validators
from ..app import login_manager
from ..model import User, UserStore

login_manager.login_view = "auth.login"

userstore = UserStore()
user = User(username='gthnk', password='gthnk')
userstore.add(user)

@login_manager.user_loader
def load_user(user_id):
    "Load the user."
    return userstore.get_by_uid(user_id)

class LoginForm(FlaskForm):
    "Login form."
    username = StringField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    submit_button = SubmitField("Login")

auth = flask.Blueprint(
    'auth',
    __name__,
    template_folder='templates',
    url_prefix='/',
    )

@auth.route('/login', methods=['GET', 'POST'])
def login():
    "Log the user in."
    user_obj = userstore.get_by_uid(1)
    login_user(user_obj)
    logging.getLogger("gthnk").info("%s automatically logs in without password", current_user)
    return flask.redirect(flask.url_for('home.index'))

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    "Log the user out."
    if current_user.is_authenticated:
        logging.getLogger("gthnk").info("%s logs out", current_user)
        logout_user()
        flask.flash('You have successfully logged out.')
    return flask.redirect(flask.url_for('home.index'))
