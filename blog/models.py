from blog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    full_name = db.Column(db.String(60), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    varsity = db.Column(db.String(100), unique=False, nullable=False)
    img1 = db.Column(db.String(20), nullable=False, default='default.png')
    img2 = db.Column(db.String(20), nullable=False, default='default.png')
    img3 = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{ self.username }', '{ self.email })"
