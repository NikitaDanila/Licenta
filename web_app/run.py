from enum import unique
from flask import Flask, render_template, Response, url_for, flash, redirect
from forms import LoginForm, SignupForm
from flask_sqlalchemy import SQLAlchemy

# Creating aplication
app = Flask(__name__)
app.config['SECRET_KEY'] = 'e0c2e77c7caec2a08617ff7f2df59d2c'
# Database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Profesor(db.Model):
    id_profesor = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    admin = db.Column(db.Boolean, nullable=True, default=1)

    def __repr__(self):
        return f"Profesor:\nid_profesor: {self.id_prosefor}\nfirst_name: {self.first_name}\nlast_name: {self.last_name}"


class Elev(db.Model):
    id_elev= db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=0)

    def __repr__(self):
        return f"Elev:\nid_elev: {self.id_elev}\nfirst_name: {self.first_name}\nlast_name: {self.last_name}"


# Web pages (routes)
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
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html',title='Sign Up', form=form)

@app.route('/stream')
def stream():
    return render_template('stream.html', title='Stream')

if __name__ == '__main__':
    app.run(debug=True)