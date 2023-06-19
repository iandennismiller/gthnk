import flask
import logging

from flask_wtf import FlaskForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from wtforms import StringField, PasswordField, SubmitField, validators
from ..app import login_manager #, bcrypt
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
    static_folder='static',
    url_prefix='/auth'
    )

@auth.route('/login', methods=['GET', 'POST'])
def login():
    user = userstore.get_by_id(1)
    login_user(user)
    logging.getLogger("gthnk").info("{user} automatically logs in without password".format(user=current_user))
    return flask.redirect(flask.url_for('gthnk.index'))

@auth.route('/login-password', methods=['GET', 'POST'])
def login_password():
    if current_user and current_user.is_authenticated:
        flask.flash('Already logged in.')
        return flask.redirect(flask.url_for('gthnk.index'))

    # next_page = flask.request.args.get('next', '')

    form = LoginForm()
    if form.validate_on_submit():
        # convert access code to user id
        user = userstore.get(username=form.username.data)

        if user:
            try:
                # password_match = bcrypt.check_password_hash(user.password, form.password.data)
                password_match = user.password == form.password.data
            except ValueError:
                password_match = False

            if password_match:
                login_user(user)
                logging.getLogger("gthnk").info("{user} logs in".format(user=current_user))
                flask.flash('Logged in successfully.')
                return flask.redirect(flask.url_for('gthnk.index'))

    return flask.render_template('login.html.j2', form=form)

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    if current_user.is_authenticated:
        logging.getLogger("gthnk").info("{user} logs out".format(user=current_user))
        logout_user()
        flask.flash('You have successfully logged out.')
    return flask.redirect(flask.url_for('gthnk.index'))
