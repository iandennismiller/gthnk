class UserStore(object):
    def __init__(self):
        self.users = []
    
    def add(self, user):
        user.id = len(self.users) + 1
        self.users.append(user)

    def get(self, username):
        for user in self.users:
            if user.username == username:
                return user
            else:
                print(f"User {user.username} does not match {username}")
        return None
    
    def get_by_id(self, id):
        for user in self.users:
            if user.id == id:
                return user
        return None

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
