from picamera import PiCamera, camera
from time import sleep
camera_path = '/home/pi/Licenta/web_app/web_app/hardware.py'

camera = PiCamera()
# camera.resolution = ( 300, 300)
# camera.framerate = (30)



def take_photo():
    camera.start_preview()
    sleep(3)
    camera.capture('/home/pi/Licenta/web_app/web_app/static/images/test.jpg')
    
# take_photo()
