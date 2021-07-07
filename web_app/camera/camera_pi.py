
import io
import time
import picamera
from camera.base_camera import BaseCamera


class Camera(BaseCamera):
    @staticmethod
    def frames():
        with picamera.PiCamera() as camera:
            camera.resolution = (1280, 720)
            camera.awb_mode = 'auto'
            camera.rotation = 270
            # carema trebuie lasata 2sec sa porneasca
            time.sleep(2)

            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                # returnam frame-ull curent
                stream.seek(0)
                yield stream.read()

                # resetam buffer-ul
                stream.seek(0)
                stream.truncate()
                