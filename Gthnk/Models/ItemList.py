# -*- coding: utf-8 -*-
# gthnk (c) 2014 Ian Dennis Miller

from flask.ext.diamond.utils.mixins import CRUDMixin
from Gthnk import db


class ItemList(db.Model, CRUDMixin):
    """
    An entry is an individual chunk of content in the Journal.
    An entry has a day, hour, and minute.  Seconds is always 0.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(256))
    content = db.Column(db.Unicode(2**32))

    def __repr__(self):
        return '<ItemList {} "{}">'.format(self.id, self.name)
