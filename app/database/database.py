import os
import sqlite3


class Database:
    """Handles all database operations."""

    def __init__(self):
        db_folder = os.path.join("data", "database")
        os.makedirs(db_folder, exist_ok=True)

        self.db_path = os.path.join(db_folder, "attendance.db")
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

        self.create_student_table()

    def create_student_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                student_name TEXT NOT NULL,
                image_folder TEXT NOT NULL
            )
        """)
        self.connection.commit()

    def student_exists(self, student_id):
        self.cursor.execute(
            "SELECT 1 FROM students WHERE student_id = ?",
            (student_id,)
        )
        return self.cursor.fetchone() is not None

    def add_student(self, student_id, student_name, image_folder):
        self.cursor.execute("""
            INSERT INTO students
            (student_id, student_name, image_folder)
            VALUES (?, ?, ?)
        """, (student_id, student_name, image_folder))
        self.connection.commit()

    def get_student(self, student_id):
        self.cursor.execute(
            "SELECT * FROM students WHERE student_id = ?",
            (student_id,)
        )
        return self.cursor.fetchone()

    def get_all_students(self):
        self.cursor.execute("""
            SELECT student_id, student_name, image_folder
            FROM students
            ORDER BY student_id
        """)
        return self.cursor.fetchall()

    def delete_student(self, student_id):
        self.cursor.execute(
            "DELETE FROM students WHERE student_id = ?",
            (student_id,)
        )
        self.connection.commit()

    def close(self):
        self.connection.close()