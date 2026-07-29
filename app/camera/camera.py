import cv2


class Camera:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.capture = None

    def open(self):
        self.capture = cv2.VideoCapture(self.camera_index)

        if not self.capture.isOpened():
            raise RuntimeError("Unable to access the webcam.")

    def read(self):
        if self.capture is None:
            raise RuntimeError("Camera has not been opened.")

        success, frame = self.capture.read()

        if not success:
            raise RuntimeError("Failed to capture frame.")

        return frame

    def release(self):
        if self.capture is not None:
            self.capture.release()
            self.capture = None

        cv2.destroyAllWindows()