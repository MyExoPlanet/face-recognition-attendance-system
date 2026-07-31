import cv2


class Camera:
    """Handles all webcam operations."""

    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.capture = None

    def open(self):
        """Open the webcam."""

        self.capture = cv2.VideoCapture(self.camera_index)

        if not self.capture.isOpened():
            raise RuntimeError("Unable to access the webcam.")

    def read(self):
        """Read a frame from the webcam."""

        if self.capture is None:
            raise RuntimeError("Camera has not been opened.")

        success, frame = self.capture.read()

        if not success:
            raise RuntimeError("Failed to capture frame.")

        return frame

    def show(self, window_name="Camera"):
        """Display one frame and return the frame and key pressed."""

        frame = self.read()

        # Flip horizontally so the preview behaves like a mirror.
        # Remove this line if you prefer the non-mirrored view.
        frame = cv2.flip(frame, 1)

        cv2.imshow(window_name, frame)

        key = cv2.waitKey(1) & 0xFF

        return frame, key

    def release(self):
        """Release the webcam."""

        if self.capture is not None:
            self.capture.release()
            self.capture = None

        cv2.destroyAllWindows()

        # Allow OpenCV to process the window close event
        cv2.waitKey(1)