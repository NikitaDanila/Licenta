from re import S
from flask.helpers import flash
from flask_admin import AdminIndexView
from web_app import db
from flask_login import UserMixin
from web_app import login_manager
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for

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
    
    def get_admin(self):
        return self.admin
        
    def __repr__(self):
        return f"Profesor:\nid_profesor: {self.id_prosefor}\nfirst_name: {self.first_name}\nlast_name: {self.last_name}"

class MyModelView(ModelView):
    def is_accessible(self):
            return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        flash("You don't have permissions", 'danger')
        return redirect(url_for('login'))

class MyAdminIndexView(AdminIndexView):
    # def is_accessible(self):
    #     user = load_user(User.get_id(self))
    #     if user.admin == 1:
    #         return current_user.is_authenticated
    pass

    def inaccessible_callback(self, name, **kwargs):
        flash("You don't have permissions", 'danger')
        return redirect(url_for('login'))