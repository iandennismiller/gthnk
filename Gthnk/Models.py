# -*- coding: utf-8 -*-
# greenthink-library (c) 2013 Ian Dennis Miller

import json, os
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask.ext.security.utils import encrypt_password, verify_password
from flask.ext.diamond.utils.mixins import CRUDMixin
from Gthnk import db, security

class Asset(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    # an asset has an owner
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('User',
        backref=db.backref('family', lazy='dynamic'))

    def __repr__(self):
        return '<Asset %r>' % self.name

    def __str__(self):
        return self.name