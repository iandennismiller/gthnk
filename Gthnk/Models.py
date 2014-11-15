# -*- coding: utf-8 -*-
# greenthink-library (c) 2013 Ian Dennis Miller

import json, os
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask.ext.security.utils import encrypt_password, verify_password
from flask.ext.diamond.utils.mixins import CRUDMixin
from flask.ext.diamond.models import User
from Gthnk import db, security

class Asset(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    # an asset has an owner
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('User', backref=db.backref('asset', lazy='dynamic'))

    def __repr__(self):
        return '<Asset %r>' % self.name

    def __str__(self):
        return self.name

class Entry(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    # an entry has a day, hour, and minute.  Seconds is always 0.
    timestamp = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.String(2**32))

    def __repr__(self):
        return '<Entry {} "{}">'.format(self.timestamp, self.content)

    def __str__(self):
        return '<Entry {} "{}">'.format(self.timestamp, self.content)

class Day(object):
    """
    a Day is a collection of Entry objects from a single day.
    This is sortof a virtual object...  but it might become a real object.
    """
    pass
