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

class Entry(db.Model, CRUDMixin):
    """
    An entry is an individual chunk of content in the Journal.
    An entry has a day, hour, and minute.  Seconds is always 0.
    """
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.Unicode(2**32))
    # tags = db.Column(db.String(2**16))

    # track the Day
    day_id = db.Column(db.Integer, db.ForeignKey("day.id"), nullable=False)
    day = db.relationship('Day', backref=db.backref('entries', lazy='dynamic'))

    def save(self, _commit):
        if not self.day_id:
            # find the day if it exists
            this_date = datetime.date.fromordinal(self.timestamp.toordinal())
            this_day = Gthnk.Models.Day.find(date=this_date)
            if not this_day: # else create the day right now
                this_day = Gthnk.Models.Day.create(date=this_date)
            # now assign a value to this Entry's day
            self.day = this_day
        super(Entry, self).save()

    def __repr__(self):
        return '<Entry {} "{}">'.format(self.timestamp, self.content)
        #return '<Entry {} ({}) "{}">'.format(self.timestamp, self.tags, self.content)

    def __unicode__(self):
        return "\n\n{}\n\n{}".format(datetime.datetime.strftime(self.timestamp, "%H%M"), self.content)
