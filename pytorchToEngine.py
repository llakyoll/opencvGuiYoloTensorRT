from ultralytics import YOLO

model = YOLO("models/yolov8n.pt")  # Load a model
# Fp32 quantization
#model.export(format="engine", device="cuda:0")
# Fp16 quantization
# model.export(format="engine", device="cuda:0", half=True)
# Int8 quantization
model.export(format="engine", device="cuda:0", int8=True)
