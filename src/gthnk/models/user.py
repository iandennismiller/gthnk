from flask_login import UserMixin
from .. import db
from .mixins.crud import CRUDMixin

class User(db.Model, UserMixin, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(1024))
    password = db.Column(db.Unicode(1024))

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
