import email
from flask_login.utils import login_required
from web_app import app, db, bcrypt, mail
from flask import render_template, url_for, flash, redirect, Response
from web_app.forms import LoginForm, SignupForm, RequestResetForm, ResetPasswordForm
from database.models import ExperimentData, User, Experiments
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from camera.camera_pi import Camera
from sensors.distance import distance, run
from time import sleep



""" Web pages (routes)"""

@app.route('/')
def index():
    form=LoginForm()
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
        
    return render_template('login.html', title='Login', form=form)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('experiment_select'))
    form = LoginForm()
    if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash(f'logged in as {form.email.data}', 'success')
                return(redirect(url_for('experiment_select')))
            else:
                flash('Login Unsuccessful. Please check email and password', 'warning')
        
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
    flash("Succesfully logged out", 'success')
    return redirect(url_for('login'))

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/experiment-select')
def experiment_select():
    number_of_experiments = Experiments.query.count()
    descriptions = Experiments.query.all()
    if current_user.is_authenticated:
        return render_template('experiment_templates.html', title='Experiment Templates', 
                                number_of_experiments=number_of_experiments, descriptions=list(descriptions))
    else:
        flash('Please log in to access', 'danger')
        return redirect(url_for('login'))

@app.route('/live-video')
def live_video():
    if not current_user.is_authenticated:
        flash('Please log in to access', 'danger')
        return redirect(url_for('login'))
    return render_template('only_stream.html', title="Stream Page")

@app.route('/live-video/<experiment_name>/<id>', methods=['GET','POST'])
def live_video_experiment(experiment_name,id):
    if not current_user.is_authenticated:
        flash('Please log in to access', 'danger')
        return redirect(url_for('login'))
    headers = Experiments.get_headers()
    data = Experiments.get_data(id)
    distance_data = distance()
    return render_template('stream.html', title='Live Video',data=data, headers=headers,distance_data=distance_data)

@app.route('/stream')
def stream():
    if not current_user.is_authenticated:
        flash('Please log in to access', 'danger')
        return redirect(url_for('login'))
    else:
        return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/admin')
@login_required
def admin():
    if current_user.admin == 1:
        return render_template('admin.html', title='Admin Page')
    else:
        flash('Please log in to access', 'danger')
        return redirect(url_for('login'))

@app.route('/to-do')
def to_do():
    return render_template('to-do.html', title='To do')

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
                    sender='danila.nikitamihai@gmail.com', recipients=[user.email])
    msg.body = f''' To reset your password, please visit the following link:
{url_for('reset_token', token=token, _external=True)}
'''
    mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('experiment_select'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent to your adress.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('experiment_select'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired Token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)