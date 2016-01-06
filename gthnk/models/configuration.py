# -*- coding: utf-8 -*-
# gthnk (c) 2014 Ian Dennis Miller

from flask.ext.diamond.utils.mixins import CRUDMixin
from .. import db


class Configuration(db.Model, CRUDMixin):
    # BACKUP_PATH = "{{{ home_directory }}}/Library/Journal/backup"
    # INPUT_FILES = "{{{ home_directory }}}/Dropbox/journal/journal-phone.txt,{{{ home_directory }}}/Dropbox/journal/journal-tablet.txt,{{{ home_directory }}}/Library/Journal/journal.txt"
    # PROJECT_PATH = "{{{ home_directory }}}/Work"
    # EXPORT_PATH = "{{{ home_directory }}}/Backup/gthnk"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    # an asset has an owner
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('User', backref=db.backref('asset', lazy='dynamic'))

    def __repr__(self):
        return '<Asset %r>' % self.name

    def __str__(self):
        return self.name
