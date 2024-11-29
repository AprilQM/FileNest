from flask_login import UserMixin
class WebUser(UserMixin):
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username

    def get_id(self):
        return self.user_id
