import cv2

from camera.camera import Camera
from vision.detector import FaceDetector


class VisionDemo:

    def __init__(self):

        self.camera = Camera()
        self.detector = FaceDetector()

    def start(self):

        self.camera.open()

        try:

            while True:

                frame = self.camera.read()

                faces = self.detector.detect(frame)

                for face in faces:

                    x1, y1, x2, y2 = face.bbox.astype(int)

                    cv2.rectangle(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 255, 0),
                        2
                    )

                frame = cv2.flip(frame, 1)

                cv2.imshow("Vision Demo", frame)

                key = cv2.waitKey(1) & 0xFF

                if key == ord("q"):
                    break

        finally:

            self.camera.release()