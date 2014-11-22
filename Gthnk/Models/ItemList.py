# -*- coding: utf-8 -*-
# greenthink-library (c) 2013 Ian Dennis Miller

import json, os, datetime
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask.ext.security.utils import encrypt_password, verify_password
from flask.ext.diamond.utils.mixins import CRUDMixin
from flask.ext.diamond.models import User
from Gthnk import db, security
import Gthnk.Models
import flask

class ItemList(db.Model, CRUDMixin):
    """
    An entry is an individual chunk of content in the Journal.
    An entry has a day, hour, and minute.  Seconds is always 0.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(256))
    content = db.Column(db.Unicode(2**32))

    def __repr__(self):
        return '<ItemList {} "{}">'.format(self.id, self.name)
