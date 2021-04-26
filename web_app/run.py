from flask import Flask, render_template, Response, url_for
from forms import LoginForm, SignupForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e0c2e77c7caec2a08617ff7f2df59d2c'

@app.route('/')
def index():
    return render_template('index.html',title='index')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

@app.route('/register')
def register():
    form = SignupForm()
    return render_template('register.html',title='Sign Up', form=form)

@app.route('/stream')
def stream():
    return render_template('stream.html', title='Stream')

if __name__ == '__main__':
    app.run(debug=True)