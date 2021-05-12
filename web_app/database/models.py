from web_app import db
from flask_login import UserMixin
from web_app import login_manager

@login_manager.user_loader
def load_user(user_id):
        return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True,nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    admin = db.Column(db.Integer, nullable=False, default=0)

    def get_id(self):
        return self.id
    def __repr__(self):
        return f"Profesor:\nid_profesor: {self.id_prosefor}\nfirst_name: {self.first_name}\nlast_name: {self.last_name}"
