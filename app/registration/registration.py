import os
import cv2

from camera.camera import Camera
from database.database import Database


class Registration:
    """Handles student registration."""

    def __init__(self):
        self.camera = Camera()
        self.database = Database()

    def create_student_folder(self, student_id, student_name):
        """Create a folder for storing a student's images."""

        folder_name = f"{student_id}_{student_name.replace(' ', '_')}"

        folder_path = os.path.join(
            "data",
            "students",
            folder_name
        )

        os.makedirs(folder_path, exist_ok=True)

        return folder_path

    def register_student(self):
        """Register a new student and capture face images."""

        student_id = input("Enter Student ID: ")
        student_name = input("Enter Student Name: ")

        # Check if student already exists
        if self.database.student_exists(student_id):
            print("\nStudent ID already exists!")
            self.database.close()
            return

        # Create folder
        folder_path = self.create_student_folder(
            student_id,
            student_name
        )

        # Save student in database
        self.database.add_student(
            student_id,
            student_name,
            folder_path
        )

        print(f"\nStudent folder created at:\n{folder_path}")

        image_count = 0
        max_images = 30

        try:
            self.camera.open()

            print("\nInstructions:")
            print("Press SPACE to capture an image.")
            print("Press ESC to cancel registration.\n")

            while image_count < max_images:

                frame, key = self.camera.show()

                if key == 32:  # SPACE

                    image_count += 1

                    image_path = os.path.join(
                        folder_path,
                        f"{image_count}.jpg"
                    )

                    cv2.imwrite(image_path, frame)

                    print(f"Captured {image_count}/{max_images}")

                elif key == 27:  # ESC

                    print("\nRegistration cancelled.")
                    break

            if image_count == max_images:
                print("\nRegistration completed successfully!")

        finally:
            self.camera.release()
            self.database.close()