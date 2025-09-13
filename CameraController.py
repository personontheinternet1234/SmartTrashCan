import cv2
import numpy as np
import tensorflow.lite as tflite
import threading
import time

class CameraController:
    def __init__(self, servoController, model_path, labels_path):
        self.cap = cv2.VideoCapture(0)
        self.servoController = servoController
        self.latest_frame = None
        self.dispose = False

        self.interpreter = tflite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        with open(labels_path, "r") as f:
            self.labels = [line.strip() for line in f.readlines()]

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
            time.sleep(1)

    def take_picture_and_classify(self):
        ret, frame = self.cap.read()
        self.latest_frame = frame

        # if ret:
        #     class_data = self.classify(frame)
        #     if class_data[1] > 0.3:
        #         self.servoController.status = class_data[0]


    def classify(self, frame):
        input_data = self.preprocess(frame)

        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()

        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])[0]

        predicted_id = int(np.argmax(output_data))
        confidence = float(output_data[predicted_id])

        return self.labels[predicted_id], confidence

    def preprocess(self, frame):
        # Get model input shape (e.g., (1, 224, 224, 3))
        input_shape = self.input_details[0]['shape']
        height, width = input_shape[1], input_shape[2]

        # Resize and convert to RGB
        resized = cv2.resize(frame, (width, height))
        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

        # Normalize to [0,1] float32
        input_data = np.expand_dims(rgb.astype(np.float32) / 255.0, axis=0)
        return input_data

    def stop(self):
        self.running = False
        self.release()

    def release(self):
        if self.cap.isOpened():
            self.cap.release()
