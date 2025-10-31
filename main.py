# main.py
import cv2
import numpy as np
import cvui
from camera_module import Camera
from yolo_module import YOLOv8

WINDOW_NAME = "cvui - Camera Interface"

def main():
    # -------------------------------
    # Camera ve YOLO Class
    # -------------------------------
    cam = Camera()
    running_model = "yolov8xInt8.engine"
    yolo = YOLOv8(model_path=f"models/{running_model}")
    cam.start()

    # -------------------------------
    # GUI için pencere boyutu
    # -------------------------------
    window_width, window_height = 1024, 780
    system_status = "Welcome to the YOLO inference application."
    frame = np.zeros((window_height, window_width, 3), np.uint8)

    cvui.init(WINDOW_NAME)
    is_cam_running = True
    cam_button_string = "Pause Camera"

    # Checkboxlar
    checkbox1 = [True]
    checkbox2 = [False]
    checkbox3 = [False]

    while True:
        # -------------------------------
        # Kamera görüntüsü al
        # -------------------------------
        if is_cam_running:
            ret, img = cam.read()
            if not ret:
                is_cam_running = False

        frame[:] = (49, 52, 49)

        # -------------------------------
        # Kamera bölgesi
        # -------------------------------
        cam_w = int(window_width * 0.45)
        cam_h = int(window_height * 0.55)
        cam_x = int(window_width * 0.03)
        cam_y = int(window_height * 0.13)
        cvui.window(frame, cam_x - 5, cam_y - 35, cam_w + 10, cam_h + 40, "Camera View")

        if is_cam_running and ret:
            # YOLO tahmini
            annotated_frame, fps = yolo.predict(img)
            resized = cv2.resize(annotated_frame, (cam_w, cam_h))
            frame[cam_y:cam_y+cam_h, cam_x:cam_x+cam_w] = resized

        # -------------------------------
        # Control panel
        # -------------------------------
        panel_w = int(window_width * 0.45)
        panel_h = int(window_height * 0.60)
        panel_x = cam_x + cam_w + int(window_width * 0.03)
        panel_y = cam_y - 35
        cvui.window(frame, panel_x, panel_y, panel_w, panel_h, "Control Panel")

        btn_w = int(panel_w * 0.45)
        btn_h = int(panel_h * 0.12)
        btn_x_offset = int(panel_w*0.05)
        btn_x_offset_2 = int(panel_w*0.52)

        # Take Snapshot
        if cvui.button(frame, panel_x + btn_x_offset, panel_y + int(panel_h*0.1), btn_w, btn_h, "Take Snapshot"):
            cv2.imwrite("capture.jpg", img)
            print("Snapshot saved!")

        if cvui.button(frame, panel_x + btn_x_offset_2, panel_y + int(panel_h*0.1), btn_w, btn_h, "Take2"):
            print("Take2 pushed!")
        # Pause / Resume Camera
        if cvui.button(frame, panel_x + btn_x_offset, panel_y + int(panel_h*0.25), btn_w, btn_h, cam_button_string):
            if is_cam_running:
                is_cam_running = False
                cam_button_string = "Start Camera"
                system_status = "Camera Stopped!"
                cam.stop()
            else:
                is_cam_running = True
                cam_button_string = "Pause Camera"
                system_status = "Camera Working"
                cam.start()
        if cvui.button(frame, panel_x + btn_x_offset_2, panel_y + int(panel_h * 0.25), btn_w, btn_h, "Take3"):
            print("Take2 pushed!")
        if cvui.button(frame, panel_x + btn_x_offset, panel_y + int(panel_h*0.40), btn_w, btn_h, "Apply Filter"):
            print("Apply Filter clicked")
        if cvui.button(frame, panel_x + btn_x_offset_2, panel_y + int(panel_h*0.40), btn_w, btn_h, "Take 4"):
            print("Apply Filter clicked")

        # Checkbox başlığı ve çizgi
        checkbox_y_start = panel_y + int(panel_h * 0.7)
        checkbox_spacing = 30
        title_y = checkbox_y_start - 30
        cvui.text(frame, panel_x + btn_x_offset, title_y, "Model Selection", 0.7, 0xffffff)
        line_color = (136, 136, 136)
        cv2.line(frame,
                 (panel_x + btn_x_offset, title_y + 25),
                 (panel_x + btn_x_offset + int(panel_w * 0.85), title_y + 25),
                 line_color, 1)

        # Checkboxlar
        if cvui.checkbox(frame, panel_x + btn_x_offset, checkbox_y_start, "Model 1", checkbox1):
            checkbox1[0] = True
            checkbox2[0] = False
            checkbox3[0] = False
        if cvui.checkbox(frame, panel_x + btn_x_offset, checkbox_y_start + checkbox_spacing, "Model 2", checkbox2):
            checkbox1[0] = False
            checkbox2[0] = True
            checkbox3[0] = False
        if cvui.checkbox(frame, panel_x + btn_x_offset, checkbox_y_start + 2 * checkbox_spacing, "Model 3", checkbox3):
            checkbox1[0] = False
            checkbox2[0] = False
            checkbox3[0] = True

        # Exit butonu
        exit_btn_x = panel_x + panel_w - btn_w - 20
        exit_btn_y = panel_y + panel_h - btn_h - 20
        if cvui.button(frame, exit_btn_x, exit_btn_y, btn_w, btn_h, "Exit"):
            break
        # -------------------------------
        # Alt Durum Paneli (Relative)
        # -------------------------------
        info_x = cam_x - 5
        info_y = cam_y + cam_h + int(window_height * 0.05)
        info_w = int(window_width * 0.94)
        info_h = int(window_height * 0.25)

        # Pencere çerçevesi
        cvui.window(frame, info_x, info_y, info_w, info_h, "System Status")

        # 🔹 Text boyutu panel boyutuna göre
        text_scale = info_h / 300  # panel yüksekliğine göre ölçeklendirme

        # 🔹 İç tablo alanı sınırları
        inner_x = info_x + 10
        inner_y = info_y + 30
        inner_w = info_w - 20
        inner_h = info_h - 40

        # 🔹 Renk (BGR formatında)
        line_color = (136, 136, 136)  # gri çizgi

        # 🔹 3 satırlık tablo için satır yüksekliği
        row_h = inner_h // 3

        # Dış çerçeve çizgileri
        cv2.line(frame, (inner_x, inner_y), (inner_x + inner_w, inner_y), line_color, 1)
        cv2.line(frame, (inner_x, inner_y + inner_h), (inner_x + inner_w, inner_y + inner_h), line_color, 1)
        cv2.line(frame, (inner_x, inner_y), (inner_x, inner_y + inner_h), line_color, 1)
        cv2.line(frame, (inner_x + inner_w, inner_y), (inner_x + inner_w, inner_y + inner_h), line_color, 1)

        # Satır ayırıcı çizgiler
        cv2.line(frame, (inner_x, inner_y + row_h), (inner_x + inner_w, inner_y + row_h), line_color, 1)
        cv2.line(frame, (inner_x, inner_y + 2 * row_h), (inner_x + inner_w, inner_y + 2 * row_h), line_color, 1)
        # Metinler
        cvui.text(frame, inner_x + 15, inner_y + int(row_h * 0.4), f"System: {system_status}", text_scale, 0xffffff)
        cvui.text(frame, inner_x + 15, inner_y + row_h + int(row_h * 0.4), f"Yolo Model: {running_model}", text_scale,
                  0xffffff)
        cvui.text(frame, inner_x + 15, inner_y + 2 * row_h + int(row_h * 0.4), f"Fps: {int(fps)}", text_scale, 0xffffff)

        cvui.update()
        cv2.imshow(WINDOW_NAME, frame)

        if cv2.waitKey(20) == 27:
            break

    cam.stop()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
