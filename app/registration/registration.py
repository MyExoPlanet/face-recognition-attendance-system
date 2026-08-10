import os
import cv2

from camera.camera import Camera
from database.database import Database
from vision.detector import FaceDetector
from vision.encoder import FaceEncoder


class Registration:
    """Handles student registration."""

    def __init__(self):
        self.camera = Camera()
        self.detector = FaceDetector()
        self.database = Database()
        self.encoder = FaceEncoder()

    def create_student_folder(self, student_id, student_name):
        """Create a folder for storing student images."""

        folder_name = f"{student_id}_{student_name.replace(' ', '_')}"

        folder_path = os.path.join(
            "data",
            "students",
            folder_name
        )

        os.makedirs(folder_path, exist_ok=True)

        return folder_path

    def register_student(self):
        """Register a new student."""

        student_id = input("Enter Student ID: ")
        student_name = input("Enter Student Name: ")

        if self.database.student_exists(student_id):
            print("\nStudent ID already exists!")
            self.database.close()
            return

        folder_path = self.create_student_folder(
            student_id,
            student_name
        )

        self.database.add_student(
            student_id,
            student_name,
            folder_path
        )

        print("\nRegistration Mode")
        print("Press SPACE to capture a face.")
        print("Press Q to cancel.\n")

        image_count = 0
        max_images = 5

        self.camera.open()

        try:

            while True:

                frame = self.camera.read()
                frame = cv2.flip(frame, 1)

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

                cv2.imshow("Student Registration", frame)

                key = cv2.waitKey(1) & 0xFF

                if key == ord(" "):

                    if len(faces) == 0:
                        print("No face detected.")
                        continue

                    face = faces[0]

                    x1, y1, x2, y2 = face.bbox.astype(int)

                    cropped_face = frame[y1:y2, x1:x2]

                    embedding = self.encoder.get_embedding(face)

                    image_count += 1

                    image_path = os.path.join(
                        folder_path,
                        f"face_{image_count:02d}.jpg"
                    )

                    cv2.imwrite(
                        image_path,
                        cropped_face
                    )
                    self.database.save_embedding(
                         student_id,
                         embedding
                         )

                    print(
                        f"Captured {image_count}/{max_images}"
                    )

                    if image_count >= max_images:

                        print("\nRegistration completed!")
                        break

                elif key == ord("q"):

                    print("\nRegistration cancelled.")
                    break

        finally:

            self.camera.release()
            self.database.close()