# -*- coding: utf-8 -*-
# gthnk (c) 2014 Ian Dennis Miller

from __future__ import with_statement
import flask

workspace = flask.Blueprint(
    'workspace',
    __name__,
    template_folder='templates',
    static_folder='static'
)
