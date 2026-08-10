import numpy as np


class FaceEncoder:
    """Extract normalized face embeddings."""

    def get_embedding(self, face):
        """Return a normalized 512-dimensional face embedding."""

        embedding = np.asarray(
            face.normed_embedding,
            dtype=np.float32
        )

        return embedding