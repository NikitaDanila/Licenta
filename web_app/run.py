from web_app import app
import os
app.config['FLASK_APP']='run.py'
app.config['FLASK_ENV']='development'
app.config['SECRET_KEY'] = os.environ.get('WEB_APP_SECRET_KEY')
if __name__ == '__main__':
    app.run(debug=True, threaded=True)