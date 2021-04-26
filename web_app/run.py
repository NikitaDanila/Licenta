from flask import Flask, render_template, Response, url_for, flash, redirect
from forms import LoginForm, SignupForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e0c2e77c7caec2a08617ff7f2df59d2c'

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