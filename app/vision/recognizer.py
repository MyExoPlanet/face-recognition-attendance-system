import numpy as np


class FaceRecognizer:
    """Compare normalized face embeddings."""

    def __init__(self, threshold=0.45):
        self.threshold = threshold

    def compare(self, live_embedding, stored_embeddings):
        """
        Compare a live face embedding with stored embeddings.

        Returns:
            student_id if a match is found,
            otherwise None.
        """

        best_student = None
        best_similarity = -1.0

        live_embedding = np.asarray(
            live_embedding,
            dtype=np.float32
        )

        # Normalize live embedding
        live_norm = np.linalg.norm(live_embedding)

        if live_norm == 0:
            return None

        live_embedding = live_embedding / live_norm

        for student_id, embedding in stored_embeddings:

            stored_embedding = np.frombuffer(
                embedding,
                dtype=np.float32
            )

            if stored_embedding.shape != live_embedding.shape:
                print(
                    f"Embedding shape mismatch for student {student_id}"
                )
                continue

            # Normalize stored embedding
            stored_norm = np.linalg.norm(stored_embedding)

            if stored_norm == 0:
                continue

            stored_embedding = (
                stored_embedding / stored_norm
            )

            # Cosine similarity
            similarity = float(
                np.dot(
                    live_embedding,
                    stored_embedding
                )
            )

            print(
                f"{student_id}: similarity = {similarity:.4f}"
            )

            if similarity > best_similarity:
                best_similarity = similarity
                best_student = student_id

        print(
            f"Best similarity: {best_similarity:.4f}"
        )

        if best_similarity >= self.threshold:
            return best_student

        return None