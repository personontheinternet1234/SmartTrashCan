import cv2
import numpy as np
import threading
import time
import re
import os
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
from pycoral.adapters import common
from pycoral.adapters import classify


class CameraController:
    def __init__(self, servoController, modelPath, labelPath):
        self.cap = cv2.VideoCapture(0, cv2.CAP_ANY)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.servoController = servoController
        self.latest_frame = None

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

        # if ret:
        #     class_data = self.classify(frame)
        #     if class_data[1] > 0.3:
        #         self.servoController.status = class_data[0]

    def classifyImage(interpreter, image):
        size = common.input_size(interpreter)
        common.set_input(interpreter, cv2.resize(image, size, fx=0, fy=0,
                                                interpolation=cv2.INTER_CUBIC))
        interpreter.invoke()
        return classify.get_classes(interpreter)

    def main():
        # Load your model onto the TF Lite Interpreter
        interpreter = make_interpreter(modelPath)
        interpreter.allocate_tensors()
        labels = read_label_file(labelPath)

        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Flip image so it matches the training input
            frame = cv2.flip(frame, 1)

            # Classify and display image
            results = classifyImage(interpreter, frame)
            cv2.imshow('frame', frame)
            print(f'Label: {labels[results[0].id]}, Score: {results[0].score}')
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
