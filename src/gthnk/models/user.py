import flask
import json
import random
import logging
from flask_login import UserMixin


class Participant(UserMixin):
    def __init__(self, id):
        self.data = db.read("participants", id)
        self.id = id

    def __repr__(self):
        return "<Participant: {}>".format(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_admin(self):
        return "sudo" in flask.session and flask.session["sudo"] == True

    def get_id(self):
        return self.id