# -*- coding: utf-8 -*-
# gthnk (c) 2014 Ian Dennis Miller

from flask.ext.diamond.utils.mixins import CRUDMixin
from .. import db


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
