from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class SignupForm(FlaskForm):
    """Creates the form for the sign up page"""
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20, message='Boss mai lung un pic')])
    first_name = StringField('First Name', 
                            validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', 
                            validators=[DataRequired(), Length(min=2, max=20)])                          
    email = StringField('Email',
                        validators=[DataRequired(), Email(message='Not gut')])
    password = PasswordField('Password',
                            validators=[DataRequired(), Length(min=2, max=20, message='Boss mai lung un pic')])
    confirm_password = PasswordField('Confirm Password',
                            validators=[DataRequired(), Length(min=2, max=20, message='Boss mai lung un pic'), EqualTo('password')])
    profesor_token = PasswordField('Profesor token', validators=[Length(min=0,max=20)], default=0)
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    """Creates the form for the login page"""
    email = StringField('Email',
                        validators=[DataRequired(), Email(message='Boss mai lung un pic')])
    password = PasswordField('Password',
                            validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class CloseForm(FlaskForm):
    close_button = SubmitField('Close')