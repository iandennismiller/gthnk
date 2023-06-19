class User(object):
    def __init__(self, username, password):
        self.id = None
        self.username = username
        self.password = password

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
