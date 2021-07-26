from flask_login import UserMixin

class User(UserMixin):
    def __init__ (self, id_, name, email):
        self.id = id_
        self.name = name
        self.email = email 

    def get(user_id):
        # need to implement
        return 0

    def create(id_, name, email):

