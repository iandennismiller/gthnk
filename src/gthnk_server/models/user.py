from flask_login import UserMixin
from .mixins.crud import CRUDMixin
from .. import db

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

    def change_password(self, password):
        from .. import bcrypt
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.password = pw_hash
        self.save()

    @classmethod
    def create_with_password(cls, username, password):
        from .. import bcrypt
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        u = cls.create(username=username, password=pw_hash)
        return u
