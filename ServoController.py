import time
from adafruit_servokit import ServoKit
import threading

class ServoController:

    def __init__(self):
        kit = ServoKit(channels=16, frequency=333)

        self.angle1 = 0
        self.angle2 = 0
        self.status = None

        self.servos = [CustomServo(kit.servo[0]), CustomServo(kit.servo[1])]

    def setAngle(self, angle, channel):
        if angle < 0 or angle > 180:
            return

        self.servos[channel].servo.angle = angle
        self.servos[channel].angle = angle

    def updatePlate(self):
        #add actual plate values here
        if self.status == "recycle":
            self.setAngle(0,0)
            self.setAngle(90,1)

        elif self.status == "trash":
            self.setAngle(90, 0)
            self.setAngle(0, 1)

    def start_threads(self):
        threading.Thread(target=self.run, daemon=True).start()
        print("Servo Thread Started!")

    def run(self):
        ...

class CustomServo:

    def __init__(self, servo):
        self.angle = None
        self.servo = servo
