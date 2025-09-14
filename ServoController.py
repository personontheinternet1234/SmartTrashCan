import time
from adafruit_servokit import ServoKit
import threading
import os

class ServoController:

    def __init__(self):
        kit = ServoKit(channels=16, frequency=333)
        self.status = "none"
        self.disposing = False

        self.angleOffset = 50
        self.neutralAngle = 90

        self.servos = [CustomServo(kit.servo[0]), CustomServo(kit.servo[1]), CustomServo(kit.servo[2])]

        self.setAngle(self.neutralAngle, 0)
        self.setAngle(self.neutralAngle, 1)
        self.setAngle(self.neutralAngle, 2)

        self.filename = "disposals.txt"
        self.disposals = 0
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                self.disposals = (int) (f.read().strip())
        else:
            with open(self.filename, "w") as f:
                f.write("0")


    def setAngle(self, angle, channel):
        if angle == None:
            self.servos[channel].angle = None
            return

        if angle < 0 or angle > 180:
            return

        self.servos[channel].servo.angle = angle
        self.servos[channel].angle = angle

    def updatePlate(self):
        if self.status == "trash":
            self.setAngle(self.neutralAngle + self.angleOffset, 0)
            self.setAngle(self.neutralAngle - self.angleOffset, 1)
            self.setAngle(self.neutralAngle, 2)
            self.disposals += 1
            with open(self.filename, "w") as f:
                f.write(str(self.disposals))
        elif self.status == "recycle":
            self.setAngle(self.neutralAngle - self.angleOffset, 0)
            self.setAngle(self.neutralAngle, 1)
            self.setAngle(self.neutralAngle + self.angleOffset, 2)
        elif self.status == "food":
            self.setAngle(self.neutralAngle, 0)
            self.setAngle(self.neutralAngle + self.angleOffset, 1)
            self.setAngle(self.neutralAngle - self.angleOffset, 2)
        elif self.status == "none":
            # no need to do anything
            self.setAngle(self.neutralAngle, 0)
            self.setAngle(self.neutralAngle, 1)
            self.setAngle(self.neutralAngle, 2)


    def start_threads(self):
        threading.Thread(target=self.run, daemon=True).start()
        print("Servo Thread Started!")

    def run(self):

        while True:
            if self.disposing == False:
                self.disposing = True
                self.updatePlate()
                time.sleep(2)
                self.disposing = False


class CustomServo:
    def __init__(self, servo):
        self.angle = 90
        self.servo = servo
