from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Creating aplication
app = Flask(__name__)


# Database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/pi/Licenta/web_app/database/site_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///E:\Licenta\web_app\database\site_database.db'
db = SQLAlchemy(app)

# Bcrypt
bcrypt = Bcrypt()

# Login
login_manager = LoginManager(app)

from web_app import routes