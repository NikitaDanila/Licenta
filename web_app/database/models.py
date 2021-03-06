from flask_admin import AdminIndexView
from sqlalchemy.orm import backref
from web_app import db, login_manager, app
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, flash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Experiments(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False,
                   unique=True, autoincrement=True)
    experiment_name = db.Column(db.String(30), nullable=False, unique=True)
    description = db.Column(db.String(300), default="")
    data = db.relationship('ExperimentData', backref='experiment_id')
    @classmethod
    def get_headers(self):
        header = ('Experiment Id', 'Experiment Name', 'Data Colected')
        return header

    @classmethod
    def get_data(self, id):
        exp = Experiments.query.filter_by(id=id).first()
        return exp

    def __repr__(self):
        return f"id:\n{self.id}\n experiment_name: {self.experiment_name}"

class ExperimentData(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, 
                    unique=True, autoincrement=True)
    
    data_colected = db.Column(db.Numeric(scale=2), default=0)
    experiment_id_relation = db.Column(db.Integer, db.ForeignKey('experiments.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True,
                   nullable=False, autoincrement=True)
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

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"Profesor:\nid_profesor: {self.id}\nfirst_name: {self.first_name}\nlast_name: {self.last_name}"


class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.admin == 1:
            return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        flash("You don't have permissions", 'danger')
        return redirect(url_for('login'))



class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.admin == 1:
            return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        flash("You don't have permissions", 'danger')
        return redirect(url_for('login'))
