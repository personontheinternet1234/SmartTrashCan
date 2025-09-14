from ServoController import ServoController
from CameraController import CameraController
from flask import Flask, Response, render_template
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
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    try:
        servoController = ServoController()
        servoController.start_threads()

        cameraController = CameraController(servoController, "model_edgetpu.tflite", "labels.txt")
        cameraController.start_threads()

        app.run(host='172.20.10.7', port=5000, debug=False)
    except KeyboardInterrupt:
        servoController.setAngle(None, 0)
        servoController.setAngle(None, 1)
        servoController.setAngle(None, 2)
