from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from picamera import PiCamera

# Creating aplication
app = Flask(__name__)
app.config['SECRET_KEY'] = 'e0c2e77c7caec2a08617ff7f2df59d2c'

# Database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/pi/Licenta/web_app/database/site_database.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///E:\Licenta\web_app\database\site_database.db'
db = SQLAlchemy(app)

# Bcrypt
bcrypt = Bcrypt()


# Login
login_manager = LoginManager(app)
camera = PiCamera()

from web_app import routes