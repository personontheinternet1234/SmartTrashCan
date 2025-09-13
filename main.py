from ServoController import ServoController
from CameraController import CameraController

if __name__ == "__main__":
    servoController = ServoController()
    servoController.start_threads()

    cameraController = CameraController(servoController,"lol","lol")
    cameraController.start_threads()
