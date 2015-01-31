# -*- coding: utf-8 -*-
# gthnk (c) 2014 Ian Dennis Miller
import datetime
import re

from flask.ext.diamond.utils.mixins import CRUDMixin
from sqlalchemy import desc
from sqlalchemy.ext.orderinglist import ordering_list

import Gthnk.Models
from Gthnk import db


class Day(db.Model, CRUDMixin):
    """
    A Day consists of the Entry objects that were created on that day.
    This is just a convenient way of referring to Entry objects in the database.
    This object is also capable of creating a string that is parsable by the JournalBuffer
    """
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True)

    pages = db.relationship("Page", order_by="Page.sequence",
        collection_class=ordering_list('sequence', reorder_on_append=True),
        backref=db.backref("day"))

    def yesterday(self):
        return self.query.filter(Day.date < self.date).order_by(desc(Day.date)).first()

    def tomorrow(self):
        return self.query.filter(Day.date > self.date).order_by(Day.date).first()

    def render(self):
        buf = datetime.datetime.strftime(self.date, "%Y-%m-%d")
        for entry in self.entries.order_by(Gthnk.Models.Entry.timestamp).all():
            buf += unicode(entry)
        buf += "\n\n"
        return buf

    def render_markdown(self):
        buf = self.render()
        buf = re.sub(r'(\d\d\d\d-\d\d-\d\d)\n', '# \g<1>\n', buf)
        buf = re.sub(r'(\d\d\d\d)\n', '## \g<1>\n', buf)

        img_fmt = "[![{sequence}](../thumbnail/{attachment})](../attachment/{attachment})\n"

        if len(self.pages) > 0:
            buf += "# Attachments\n\n"
            for page in self.pages:
                buf += img_fmt.format(
                    sequence=page.sequence,
                    thumbnail=page.png_filename(),
                    attachment=page.filename()
                )

        return buf

    def __repr__(self):
        return "<Day: {}>".format(self.date)

    def __unicode__(self):
        return repr(self)


def latest():
    return Day.query.order_by(desc(Day.date)).first()
