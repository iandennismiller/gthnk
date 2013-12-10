# -*- coding: utf-8 -*-
# greenthink-library (c) 2013 Ian Dennis Miller

import json, os
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask.ext.security.utils import encrypt_password, verify_password
from mixins import CRUDMixin
from GTLibrary import db, app

# Define models
roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin, CRUDMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

class User(db.Model, UserMixin, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    _password = db.Column('password', db.String(255), nullable=False)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email

    def __repr__(self):
        return '<User %r>' % self.email

    # any operation on _password will be passed through a hash function first
    def _set_password(self, password):
        self._password = encrypt_password(password)

    def _get_password(self):
        return self._password

    password = db.synonym('_password', descriptor=property(_get_password, _set_password))

    def valid_password(self, password):
        """Check if provided password is valid."""
        return verify_password(password, self._password)

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