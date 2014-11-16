# -*- coding: utf-8 -*-
# greenthink-library (c) 2013 Ian Dennis Miller

import json, os, datetime
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask.ext.security.utils import encrypt_password, verify_password
from flask.ext.diamond.utils.mixins import CRUDMixin
from flask.ext.diamond.models import User
from Gthnk import db, security

class Entry(db.Model, CRUDMixin):
    """
    An entry is an individual chunk of content in the Journal.
    An entry has a day, hour, and minute.  Seconds is always 0.
    """
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.String(2**32))
    tags = db.Column(db.String(2**16))

    def __repr__(self):
        return '<Entry {} ({}) "{}">'.format(self.timestamp, self.tags, self.content)

    def __str__(self):
        return "\n\n{}\n\n{}".format(datetime.datetime.strftime(self.timestamp, "%H%M"), self.content)
