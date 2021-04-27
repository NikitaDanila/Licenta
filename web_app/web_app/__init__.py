from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Creating aplication
app = Flask(__name__)
app.config['SECRET_KEY'] = 'e0c2e77c7caec2a08617ff7f2df59d2c'
# Database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from web_app import routes
