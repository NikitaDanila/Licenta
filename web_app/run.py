from flask import Flask, render_template, Response
from flask.helpers import url_for
from forms import LoginForm, SignupForm
# from hardware import Camera
# import cv2
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
    form = LoginForm
    return render_template('login.html', title='Login', form=form)

@app.route('/register')
def register():
    form = SignupForm()
    return render_template('register.html',title='Sign Up', form=form)

# @app.route('/stream')
# def stream():
#     def gen(camera):
#         while True:
#             success, frame = camera.read()  # read the camera frame
#             if not success:
#                 break
#             else:
#                 ret, buffer = cv2.imencode('.jpg', frame)
#                 frame = buffer.tobytes()
#                 yield (b'--frame\r\n'
#                     b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 
    
#     return Response(gen(Camera.camera),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')
#     # return render_template('stream.html', title='Stream')

if __name__ == '__main__':
    app.run(debug=True)