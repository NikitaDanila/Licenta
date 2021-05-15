from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class SignupForm(FlaskForm):
    """Creates the form for the sign up page"""
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20, message='Please enter a valid Username')])
    first_name = StringField('First Name', 
                            validators=[DataRequired(), Length(min=2, max=20, message='Please enter a valid First Name')])
    last_name = StringField('Last Name', 
                            validators=[DataRequired(), Length(min=2, max=20, message='Please enter a valid Last Name')])                          
    email = StringField('Email',
                        validators=[DataRequired(), Email(message='Please enter a valid Email')])
    password = PasswordField('Password',
                            validators=[DataRequired(), Length(min=2, max=20, message='Please enter a valid Email')])
    confirm_password = PasswordField('Confirm Password',
                            validators=[DataRequired(), Length(min=2, max=20, message='Please enter a valid Password'), EqualTo('password', message='The passwords do not match')])
    profesor_token = PasswordField('Profesor token', validators=[Length(min=0,max=20)], default=0)
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    """Creates the form for the login page"""
    email = StringField('Email',
                        validators=[DataRequired(), Email(message='Please enter a valid Email')])
    password = PasswordField('Password',
                            validators=[DataRequired(message='Please enter a password')])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class CloseForm(FlaskForm):
    close_button = SubmitField('Close')