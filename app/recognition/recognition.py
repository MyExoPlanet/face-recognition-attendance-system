import cv2

from camera.camera import Camera
from database.database import Database
from vision.detector import FaceDetector
from vision.encoder import FaceEncoder
from vision.recognizer import FaceRecognizer


class Recognition:
    """Recognize registered students."""

    def __init__(self):
        self.camera = Camera()
        self.detector = FaceDetector()
        self.encoder = FaceEncoder()
        self.recognizer = FaceRecognizer()
        self.database = Database()

    def start(self):
        """Start live recognition."""

        self.camera.open()

        print("\nRecognition Mode")
        print("Press Q to return to the menu.\n")

        try:

            while True:

                frame = self.camera.read()
                frame = cv2.flip(frame, 1)

                faces = self.detector.detect(frame)

                stored_embeddings = self.database.get_all_embeddings()

                for face in faces:

                    x1, y1, x2, y2 = face.bbox.astype(int)

                    embedding = self.encoder.get_embedding(face)

                    student_id = self.recognizer.compare(
                        embedding,
                        stored_embeddings
                    )

                    if student_id:

                        student_name = self.database.get_student_name(
                            student_id
                        )

                        label = student_name

                    else:

                        label = "Unknown"

                    cv2.rectangle(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 255, 0),
                        2
                    )

                    cv2.putText(
                        frame,
                        label,
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 0),
                        2
                    )

                cv2.imshow(
                    "Face Recognition",
                    frame
                )

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

        finally:

            self.camera.release()
            self.database.close()