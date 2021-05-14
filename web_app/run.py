from web_app import app
app.config['FLASK_APP']='run.py'
app.config['FLASK_ENV']='development'
app.config['SECRET_KEY'] = 'e0c2e77c7caec2a08617ff7f2df59d2c'

if __name__ == '__main__':
    app.run(debug=True)