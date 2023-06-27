class User:
    "A user object."

    def __init__(self, username, password):
        self.uid = None
        self.username = username
        self.password = password

    def __repr__(self):
        "Return a string representation of the user."
        return f"<User: {self.uid}>"

    def is_authenticated(self):
        "Return True if the user is authenticated."
        return True

    def is_active(self):
        "True, as all users are active."
        return True

    def is_anonymous(self):
        "False, as anonymous users aren't supported."
        return False

    def get_uid(self):
        "Return the user id."
        return self.uid


class UserStore:
    "A dummy user store."

    def __init__(self):
        self.users = []

    def add(self, user):
        "Add a user to the store."
        user.uid = len(self.users) + 1
        self.users.append(user)

    def get(self, username):
        "Get a user by username."
        for user in self.users:
            if user.username == username:
                return user
        return None

    def get_by_uid(self, uid):
        "Get a user by id."
        for user in self.users:
            if user.uid == uid:
                return user
        return None
