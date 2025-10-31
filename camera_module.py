# camera_module.py
import cv2

class Camera:
    def __init__(self, cam_index=0, width=None, height=None, fps=None):
        self.cam_index = cam_index
        self.cap = None
        self.is_running = False
        self.width = width
        self.height = height
        self.fps = fps

    def start(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(self.cam_index)
            if self.width:
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            if self.height:
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            if self.fps:
                self.cap.set(cv2.CAP_PROP_FPS, self.fps)

        if not self.cap.isOpened():
            raise RuntimeError("Camera could not be opened!")
        self.is_running = True

    def stop(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        self.is_running = False

    def read(self):
        if self.is_running and self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
            return ret, frame
        return False, None

    def __del__(self):
        self.stop()
