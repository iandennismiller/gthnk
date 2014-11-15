# -*- coding: utf-8 -*-
# gthnk (c) 2014 Ian Dennis Miller

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
