import time
from adafruit_servokit import ServoKit

class ServoController:

    def __init__(self):
        kit = ServoKit(channels=16, frequency=333)

        self.angle1 = 0
        self.angle2 = 0
        self.status = None

        self.servo1 = kit.servo[0]
        self.servo2 = kit.servo[1]

        self.servo1.angle = self.angle1
        self.servo2.angle = self.angle2

    def sefAngle1(self, angle):
        if angle < 0 or angle > 180:
            return
        
        self.angle1 = angle
        self.servo1.angle = self.angle1
    
    def setAngle2(self, angle):
        if angle < 0 or angle > 180:
            return
        
        self.angle2 = angle
        self.servo2.angle = self.angle2

    def updatePlate(self):
        #add actual plate values here
        if self.status == "recycle":
            self.setAngle1(0)
            self.setAngle2(90)

        elif self.status == "trash":
            self.setAngle1(90)
            self.setAngle2(0)
        
    def run(self):
        ...

        
