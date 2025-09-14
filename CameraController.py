import cv2
import numpy as np
import threading
import time
import re
import os
# from pycoral.utils.dataset import read_label_file
# from pycoral.utils.edgetpu import make_interpreter
# from pycoral.adapters import common
# from pycoral.adapters import classify

from keras.models import load_model  # TensorFlow is required for Keras to work

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

class CameraController:
    def __init__(self, servoController, modelPath, labelPath):
        self.cap = cv2.VideoCapture(0, cv2.CAP_ANY)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.servoController = servoController
        self.latest_frame = None

        self.model = load_model(modelPath, compile=False)
        self.class_names = open(labelPath, "r").readlines()

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

        if ret:
            image = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)
            image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
            image = (image / 127.5) - 1

            prediction = self.model.predict(image)
            index = np.argmax(prediction)
            class_name = self.class_names[index]
            confidence_score = prediction[0][index]

            label = class_name[2:]
            confidence = np.round(confidence_score * 100)[:-2]
            if confidence > 0.3:
                self.servoController.status = label
