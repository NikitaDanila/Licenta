from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
from flask_mail import Mail
import os

# Creating aplication
app = Flask(__name__)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/pi/Licenta/web_app/database/site_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Bcrypt
bcrypt = Bcrypt()

# Login
login_manager = LoginManager(app)

from database.models import ExperimentData, Experiments, MyAdminIndexView, MyModelView, User

# Admin and admin view
admin = Admin(app, template_mode='bootstrap4',
              index_view=MyAdminIndexView(), url='/admin')
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(ExperimentData, db.session))
admin.add_view(MyModelView(Experiments, db.session))

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True 
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER') 
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)

from web_app import routes