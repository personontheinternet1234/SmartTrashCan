import time
from adafruit_servokit import ServoKit

class ServoController:

    def __init__(self):
        kit = ServoKit(channels=16, frequency=333)
        kit.servo[0].angle = 0
        kit.servo[1].angle = 0
