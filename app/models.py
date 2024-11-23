from app import db

# 用户和用户数据库对象
class DatabaseUser(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return f'<User Id: {self.user_id} Username: {self.username}>'
