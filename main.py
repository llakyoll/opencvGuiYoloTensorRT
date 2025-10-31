import cv2
import time
from ultralytics import NAS, YOLO
import torch

# YOLOv8 modelini GPU'ya yükle
model = YOLO("models/yolov8xFP16.engine")

cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# cap.set(cv2.CAP_PROP_FPS, 30)
# out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'XVID'), 60, (640, 480))

while cap.isOpened():
    start_time = time.time()
    success, im0 = cap.read()
    if not success:
        break

    #im1 = cv2.resize(im0, (640, 480))

    # Nesne takibi yap
    results = model.predict(im0, device="cuda:0", verbose=False)

    end_time = time.time()

    if len(results) > 0:  # Eğer sonuçlar varsa
        # Anotasyonlu görüntüyü al
        annotated_frame = results[0].plot()

        # FPS hesapla ve ekrana yaz
        fps = 1 / (end_time - start_time)
        cv2.putText(annotated_frame, f"FPS: {fps:.2f}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Video Dosyasını Kaydet
        # out.write(annotated_frame)

        # Anotasyonlu görüntüyü göster
        cv2.imshow('Tracking Frame', annotated_frame)

    # 'q' tuşuna basıldığında döngüyü bitir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

