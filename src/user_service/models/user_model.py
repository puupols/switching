

class UserModel:

    def __init__(self, user_name, password, user_email, id=None):
        self.id = id
        self.user_name = user_name
        self.password = password
        self.user_email = user_email
