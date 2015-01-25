# -*- coding: utf-8 -*-
# gthnk (c) 2014 Ian Dennis Miller

from flask.ext.diamond.utils.mixins import CRUDMixin
from Gthnk import db


class Page(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'))
    sequence = db.Column(db.Integer)
    binary = db.Column(db.Binary)
    title = db.Column(db.Unicode(1024))

    def __repr__(self):
        return '<Page filename: %r-%d.pdf>' % (self.day, self.sequence)

    def __unicode__(self):
        return repr(self)
