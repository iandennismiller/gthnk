# -*- coding: utf-8 -*-
# gthnk (c) 2014 Ian Dennis Miller

from flask.ext.wtf import Form
from wtforms import TextAreaField
from wtforms.validators import Required


class EntryForm(Form):
    content = TextAreaField('content', validators=[Required()])

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False  # not app.config['DEBUG']
        Form.__init__(self, *args, **kwargs)
