import os
import shutil

from database.database import Database


class Admin:
    """Admin operations."""

    def __init__(self):
        self.database = Database()

    def view_students(self):
        students = self.database.get_all_students()

        if not students:
            print("\nNo students found.\n")
            return

        print("\nRegistered Students")
        print("-" * 70)
        print(f"{'ID':<10}{'Name':<25}{'Image Folder'}")
        print("-" * 70)

        for student in students:
            print(f"{student[0]:<10}{student[1]:<25}{student[2]}")

        print("-" * 70)

    def delete_student(self):
        student_id = input("\nEnter Student ID to delete: ")

        student = self.database.get_student(student_id)

        if student is None:
            print("\nStudent not found.")
            return

        folder_path = student[2]
        print(f"Folder path from database: {folder_path}")

        if os.path.exists(folder_path):
            print(f"Folder exists: {os.path.exists(folder_path)}")
            shutil.rmtree(folder_path)

        self.database.delete_student(student_id)

        print("\nStudent deleted successfully.")

    def close(self):
        self.database.close()