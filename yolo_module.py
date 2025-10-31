# yolo_module.py
import time
import cv2
from ultralytics import YOLO

class YOLOv8:
    def __init__(self, model_path="yolov8xInt8.engine", device="cuda:0"):
        self.model = YOLO(model_path)
        self.device = device

    def predict(self, frame):
        """
        Frame üzerinde YOLOv8 tahminini yap.
        Returns:
            annotated_frame: Anotasyonlu frame
            fps: FPS değeri
        """
        start_time = time.time()
        results = self.model.predict(frame, device=self.device, verbose=False)
        end_time = time.time()
        fps = 1 / (end_time - start_time)

        if len(results) > 0:
            annotated_frame = results[0].plot()
            return annotated_frame, fps
        return frame, fps
