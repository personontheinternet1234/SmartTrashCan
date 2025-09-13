from ServoController import ServoController
from CameraController import CameraController
from flask import Flask, Response
import time
import cv2

app = Flask(__name__)

def generate_frames():
    while True:
        if hasattr(cameraController, "latest_frame") and cameraController.latest_frame is not None:
            frame = cameraController.latest_frame.copy()

            # Encode frame to JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return "<h1>Live Video Stream</h1><img src='/video_feed'>"

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    servoController = ServoController()
    servoController.start_threads()

    cameraController = CameraController(servoController,"lol","lol")
    time.sleep(1)
    cameraController.start_threads()

    app.run(host='172.20.10.7', port=5000, debug=False)
