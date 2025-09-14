import cv2
import threading
import time
import os
from datetime import datetime
from pycoral.utils.dataset import read_label_file
from pycoral.adapters import common
from pycoral.adapters import classify
import tflite_runtime.interpreter as tflite  # Add this import


class CameraController:
    def __init__(self, servoController, modelPath, labelPath, trainingFolder="training_images"):
        self.cap = cv2.VideoCapture(0, cv2.CAP_ANY)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.servoController = servoController
        self.latest_frame = None

        self.interpreter = tflite.Interpreter(modelPath)
        self.interpreter.allocate_tensors()
        self.labels = read_label_file(labelPath)

        self.save_training_images = False
        self.training_folder = trainingFolder
        self.save_interval = 1
        self.last_save_time = 0
        self.image_counter = 0

        self.running = False

    def start_threads(self):
        if not self.cap.isOpened():
            print("Error: Camera could not be opened.")
            return
        self.running = True
        threading.Thread(target=self.run, daemon=True).start()
        print("Camera Thread Started!")

    def run(self):
        while self.running:
            self.take_picture_and_classify()

    def take_picture_and_classify(self):
        ret, frame = self.cap.read()
        self.latest_frame = frame

        if self.save_training_images:
                self._save_training_image(frame)

        if ret:
            class_data = self.classifyImage(frame)
            if class_data[0].score > 0.4:
                self.servoController.status = self.labels[class_data[0].id]
            else:
                self.servoController.status = "none"

    def classifyImage(self, image):
        size = common.input_size(self.interpreter)
        common.set_input(self.interpreter, cv2.resize(image, size, fx=0, fy=0,
                                                interpolation=cv2.INTER_CUBIC))
        self.interpreter.invoke()
        return classify.get_classes(self.interpreter)

    def _save_training_image(self, frame):
        """Save a training image with metadata"""
        current_time = time.time()

        if current_time - self.last_save_time >= self.save_interval:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.image_counter += 1
            filename = f"train_{timestamp}_{self.image_counter:04d}.jpg"
            filepath = os.path.join(self.training_folder, filename)
            cv2.imwrite(filepath, frame)

            self.last_save_time = current_time
