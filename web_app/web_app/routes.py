from web_app import app, db, bcrypt
from flask import render_template, url_for, flash, redirect
from web_app.forms import LoginForm, SignupForm
from database.models import Profesor, Student
""" Web pages (routes)"""

@app.route('/')
def index():
    return render_template('index.html',title='index')

@app.route('/about')
def about():
    return render_template('about.html', title='About')
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # This needs to be modified
        if form.email.data == 'a@hamil.com' and form.password.data == 'asa':
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
    else:
        flash('Login Unsuccessful. Please check username and possword', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if form.profesor_token.data == "1":
            profesor = Profesor(email=form.email.data,username=form.username.data,
                                first_name=form.first_name.data, last_name=form.last_name.data,password=hashed_password)
            db.session.add(profesor)
        else:
            student = Student(email=form.email.data,username=form.username.data,
                              first_name=form.first_name.data, last_name=form.last_name.data,password=hashed_password)
            db.session.add(student)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Sign Up', form=form)

@app.route('/stream')
def stream():
    return render_template('stream.html', title='Stream')
