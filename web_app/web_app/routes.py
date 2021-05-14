from web_app import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, Response
from web_app.forms import LoginForm, SignupForm, CloseForm
from database.models import User
from flask_login import login_user, current_user, logout_user
from camera import Camera

""" Web pages (routes)"""

@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('register'))

    return render_template('index.html',title='index')

@app.route('/about')
def about():
    return render_template('about.html', title='About')
@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash(f'logged in as {form.email.data}')
                return(redirect(url_for('index')))
            else:
                flash('Login Unsuccessful. Please check emails and possword', 'danger')
        
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Validation for the profesor token, if the token is correct then it gives admin
        if form.profesor_token.data == "1":
            user = User(email=form.email.data,username=form.username.data,
                                first_name=form.first_name.data, last_name=form.last_name.data,password=hashed_password, admin=1)
            db.session.add(user)
        else:
            user = User(email=form.email.data,username=form.username.data,
                              first_name=form.first_name.data, last_name=form.last_name.data,password=hashed_password)
            db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Sign Up', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/live-video', methods=['GET','POST'])
def live():
    form = CloseForm()
    return render_template('stream.html',form=form, title='Live Video')

@app.route('/stream')
def stream():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    # return render_template('stream.html', title='Stream')
