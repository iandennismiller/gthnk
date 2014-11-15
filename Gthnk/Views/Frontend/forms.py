# -*- coding: utf-8 -*-
# greenthink-library (c) 2013 Ian Dennis Miller

from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import Required

from GT import app

# 'csrf_enabled' has to be set to false otherwise Flask-WTForms do not work and you get an error message 
# {'csrf': ['Missing or invalid CSRF token']}!
class LoginForm(Form):
    username = TextField('username')
    password = PasswordField('password', default = False)

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False #not app.config['DEBUG']
        Form.__init__(self, *args, **kwargs)

class EntryForm(Form):
    content = TextAreaField('content', validators = [Required()])

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False #not app.config['DEBUG']
        Form.__init__(self, *args, **kwargs)