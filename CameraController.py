import cv2
import numpy as np
import threading
import time
import re
import os
from pycoral.utils.dataset import read_label_file
from pycoral.adapters import common
from pycoral.adapters import classify
import tflite_runtime.interpreter as tflite  # Add this import


class CameraController:
    def __init__(self, servoController, modelPath, labelPath):
        self.cap = cv2.VideoCapture(0, cv2.CAP_ANY)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.servoController = servoController
        self.latest_frame = None

        self.interpreter = tflite.Interpreter(modelPath)
        self.interpreter.allocate_tensors()
        labels = read_label_file(labelPath)

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
            class_data = self.classifyImage(frame)
            if class_data[0].score > 0.1:
                self.servoController.status = class_data[0].id
                print(self.servoController.status)

    def classifyImage(self, image):
        size = common.input_size(self.interpreter)
        common.set_input(self.interpreter, cv2.resize(image, size, fx=0, fy=0,
                                                interpolation=cv2.INTER_CUBIC))
        self.interpreter.invoke()
        return classify.get_classes(self.interpreter)
