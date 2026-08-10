import os
import sqlite3


class Database:
    """Handles all database operations."""

    def __init__(self):
        db_folder = os.path.join("data", "database")
        os.makedirs(db_folder, exist_ok=True)

        self.db_path = os.path.join(db_folder, "attendance.db")
        self.connection = sqlite3.connect(self.db_path)
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.connection.cursor()

        self.create_student_table()
        self.create_embedding_table()
        self.create_attendance_table()

    def create_student_table(self):
        """Create the students table."""

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                student_name TEXT NOT NULL,
                image_folder TEXT NOT NULL
            )
        """)

        self.connection.commit()

    def create_embedding_table(self):
        """Create the face embeddings table."""

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS face_embeddings (

                embedding_id INTEGER PRIMARY KEY AUTOINCREMENT,

                student_id TEXT NOT NULL,

                embedding BLOB NOT NULL,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY(student_id)
                REFERENCES students(student_id)

            )
        """)

        self.connection.commit()

    def create_attendance_table(self):
        """Create the attendance table."""

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (

                attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,

                student_id TEXT NOT NULL,

                date TEXT NOT NULL,

                time TEXT NOT NULL,

                status TEXT NOT NULL,

                FOREIGN KEY(student_id)
                REFERENCES students(student_id)

            )
        """)

        self.connection.commit()

    def student_exists(self, student_id):
        """Check whether a student already exists."""

        self.cursor.execute(
            "SELECT 1 FROM students WHERE student_id = ?",
            (student_id,)
        )

        return self.cursor.fetchone() is not None

    def add_student(self, student_id, student_name, image_folder):
        """Add a student."""

        self.cursor.execute("""
            INSERT INTO students
            (student_id, student_name, image_folder)
            VALUES (?, ?, ?)
        """, (
            student_id,
            student_name,
            image_folder
        ))

        self.connection.commit()

    def save_embedding(self, student_id, embedding):
        """Save a student's face embedding."""

        self.cursor.execute("""
            INSERT INTO face_embeddings
            (student_id, embedding)
            VALUES (?, ?)
        """, (
            student_id,
            embedding.tobytes()
        ))

        self.connection.commit()

    def get_all_embeddings(self):
        """Return all stored embeddings."""

        self.cursor.execute("""
            SELECT student_id, embedding
            FROM face_embeddings
        """)

        return self.cursor.fetchall()

    def get_student(self, student_id):
        """Return one student."""

        self.cursor.execute("""
            SELECT *
            FROM students
            WHERE student_id = ?
        """, (student_id,))

        return self.cursor.fetchone()

    def get_student_name(self, student_id):
        """Return a student's name."""

        self.cursor.execute("""
            SELECT student_name
            FROM students
            WHERE student_id = ?
        """, (student_id,))

        result = self.cursor.fetchone()

        if result:
            return result[0]

        return None

    def get_all_students(self):
        """Return all students."""

        self.cursor.execute("""
            SELECT
                student_id,
                student_name,
                image_folder
            FROM students
            ORDER BY student_id
        """)

        return self.cursor.fetchall()

    def delete_student(self, student_id):
        """Delete a student and related records."""

        self.cursor.execute(
        "DELETE FROM face_embeddings WHERE student_id = ?",
        (student_id,)
          )
        self.cursor.execute(
        "DELETE FROM attendance WHERE student_id = ?",
        (student_id,)
          )

        self.cursor.execute(
        "DELETE FROM students WHERE student_id = ?",
        (student_id,)
          )
        self.connection.commit()

    def mark_attendance(self, student_id):
        """Mark attendance for a student."""

        from datetime import datetime

        now = datetime.now()

        self.cursor.execute("""
            INSERT INTO attendance
            (student_id, date, time, status)
            VALUES (?, ?, ?, ?)
        """, (
            student_id,
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S"),
            "Present"
        ))

        self.connection.commit()

    def close(self):
        """Close the database connection."""

        self.connection.close()