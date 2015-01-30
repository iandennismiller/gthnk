# -*- coding: utf-8 -*-
# gthnk (c) 2014 Ian Dennis Miller

from flask.ext.diamond.utils.mixins import CRUDMixin
from Gthnk import db
from wand.image import Image


class Page(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'))
    sequence = db.Column(db.Integer)
    binary = db.Column(db.Binary)
    title = db.Column(db.Unicode(1024))
    thumbnail = db.Column(db.Binary)
    preview = db.Column(db.Binary)

    def format(self):
        with Image(blob=self.binary) as img:
            return img.format

    def filename(self):
        return '{0}-{1}.{2}'.format(self.day.date, self.sequence, self.format().lower())

    def png_filename(self):
        return '{0}-{1}.{2}'.format(self.day.date, self.sequence, "png")

    def __repr__(self):
        if self.sequence is not None:
            return '<Page filename: %s-%d.pdf>' % (self.day.date, self.sequence)
        else:
            return '<Page filename: %s-xxx.pdf>' % (self.day.date)

    def __unicode__(self):
        return repr(self)
