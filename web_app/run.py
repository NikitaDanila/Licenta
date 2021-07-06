from web_app import app
import os
app.config['FLASK_APP']='run.py'
app.config['FLASK_ENV']='development'
# app.config['SECRET_KEY'] = 'e0c2e77c7caec2a08617ff7f2df59d2c'
app.config['SECRET_KEY'] = os.environ.get('WEB_APP_SECRET_KEY')
if __name__ == '__main__':
    app.run(debug=True)