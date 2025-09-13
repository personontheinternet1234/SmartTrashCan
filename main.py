from ServoController import ServoController
from CameraController import CameraController

if __name__ == "__main__":
    servoController = ServoController()
    servoController.run()

    cameraController = CameraController(servoController,"lol","lol")
    cameraController.run()
