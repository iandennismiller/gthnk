# -*- coding: utf-8 -*-
# greenthink-library (c) 2013 Ian Dennis Miller

import json, os, datetime
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from sqlalchemy import and_
from Gthnk import db, security
import Gthnk.Models

class Day(object):
    """
    A Day consists of the Entry objects that were created on that day.
    This is just a convenient way of referring to Entry objects in the database.
    This object is also capable of creating a string that is parsable by the JournalBuffer
    """

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

        # create datetime objects with time bounds of Day
        self.startingTime = datetime.datetime(year, month, day, 00, 00)
        self.endingTime = datetime.datetime(year, month, day, 23, 59)

        # create unevaluated query object referencing entries from this day
        self.entries = Gthnk.Models.Entry.query.filter(and_(
            Gthnk.Models.Entry.timestamp>=self.startingTime,
            Gthnk.Models.Entry.timestamp<=self.endingTime)).order_by(Gthnk.Models.Entry.timestamp)

    def __str__(self):
        buf = datetime.datetime.strftime(self.startingTime, "%Y-%m-%d")
        for entry in self.entries.all():
            buf += "\n\n%s\n\n" % datetime.datetime.strftime(entry.timestamp, "%H%M")
            buf += entry.content
        buf += "\n"
        return buf
