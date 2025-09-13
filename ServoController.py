import time
from adafruit_servokit import ServoKit
import threading

class ServoController:

    def __init__(self):
        kit = ServoKit(channels=16, frequency=333)
        self.status = None

        self.angleOffset = 25
        self.neutralAngle = 90

        self.servos = [CustomServo(kit.servo[0]), CustomServo(kit.servo[1]), CustomServo(kit.servo[2])]

    def setAngle(self, angle, channel):
        if angle < 0 or angle > 180:
            return

        self.servos[channel].servo.angle = angle
        self.servos[channel].angle = angle

    def updatePlate(self):
        if self.status == "recycle":
            self.setAngle(self.neutralAngle - self.angleOffset, 0)
            self.setAngle(self.neutralAngle + self.angleOffset, 1)
            self.setAngle(self.neutralAngle + self.angleOffset, 2)

        elif self.status == "food":
            self.setAngle(self.neutralAngle + self.angleOffset, 0)
            self.setAngle(self.neutralAngle - self.angleOffset, 1)
            self.setAngle(self.neutralAngle + self.angleOffset, 2)

        elif self.status == "neutral":
            self.setAngle(self.neutralAngle, 0)
            self.setAngle(self.neutralAngle, 1)
            self.setAngle(self.neutralAngle, 2)

        else:
            #trash
            self.setAngle(self.neutralAngle + self.angleOffset, 0)
            self.setAngle(self.neutralAngle + self.angleOffset, 1)
            self.setAngle(self.neutralAngle - self.angleOffset, 2)


    def start_threads(self):
        threading.Thread(target=self.run, daemon=True).start()
        print("Servo Thread Started!")

    def run(self):
        ...

class CustomServo:
    def __init__(self, servo):
        self.angle = 90
        self.servo = servo
