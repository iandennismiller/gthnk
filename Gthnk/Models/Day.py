# -*- coding: utf-8 -*-
# greenthink-library (c) 2013 Ian Dennis Miller

import json, os, datetime
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from sqlalchemy import and_, desc
from flask.ext.diamond.utils.mixins import CRUDMixin
from Gthnk import db, security
import Gthnk.Models

def latest():
    return Day.query.order_by(desc(Day.date)).first()

class Day(db.Model, CRUDMixin):
    """
    A Day consists of the Entry objects that were created on that day.
    This is just a convenient way of referring to Entry objects in the database.
    This object is also capable of creating a string that is parsable by the JournalBuffer
    """
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)

    def yesterday(self):
        # query days for a timestamp "less than" the current date; order by date descending
        # retrieve the first result; this is the previous day
        # if there is no previous day, return None.
        return self.query.filter(Day.date < self.date).order_by(desc(Day.date)).first()

    def tomorrow(self):
        #yesterday = Models.Day.query.filter(Models.Day.date < day.date).order_by(desc(Models.Day.date)).first()
        return self.query.filter(Day.date > self.date).order_by(Day.date).first()

    def __unicode__(self):
        buf = datetime.datetime.strftime(self.date, "%Y-%m-%d")
        for entry in self.entries.order_by(Gthnk.Models.Entry.timestamp).all():
            buf += unicode(entry)
        buf += "\n\n"
        return buf

    def __repr__(self):
        return "{}".format(self.date)
