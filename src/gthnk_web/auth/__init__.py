import flask
import logging

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
    return userstore.get_by_id(user_id)

class LoginForm(FlaskForm):
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
    user = userstore.get_by_id(1)
    login_user(user)
    logging.getLogger("gthnk").info("{user} automatically logs in without password".format(user=current_user))
    return flask.redirect(flask.url_for('gthnk.index'))

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    if current_user.is_authenticated:
        logging.getLogger("gthnk").info("{user} logs out".format(user=current_user))
        logout_user()
        flask.flash('You have successfully logged out.')
    return flask.redirect(flask.url_for('gthnk.index'))
