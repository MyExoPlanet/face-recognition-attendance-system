from insightface.app import FaceAnalysis


class FaceDetector:
    """Detect faces using InsightFace."""

    def __init__(self):

        self.app = FaceAnalysis(
            providers=["CPUExecutionProvider"]
        )

        self.app.prepare(
            ctx_id=0,
            det_size=(320, 320)
        )

    def detect(self, frame):
        """
        Detect faces.

        Returns:
            List of detected faces.
        """

        return self.app.get(frame)