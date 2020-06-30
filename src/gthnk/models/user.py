import flask
import json
import random
import logging
from flask_login import UserMixin

from .. import db

class User(db.Model, UserMixin):
    def __init__(self, id):
        self.data = db.read("user", id)
        self.id = id

    def __repr__(self):
        return "<User: {}>".format(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
