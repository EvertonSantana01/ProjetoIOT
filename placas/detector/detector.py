import cv2
import numpy as np
from ultralytics import YOLO
from .ocr import aplicar_ocr
from .utils import preprocess

model = YOLO('license_plate_detector.pt')

def detectar_placa(frame):
    results = model.predict(frame, conf=0.25, iou=0.5)[0]
    for result in results.boxes:
        x1, y1, x2, y2 = map(int, result.xyxy[0])
        padding = 30
        x1 = max(0, x1 - padding)
        y1 = max(0, y1 - padding)
        x2 = min(frame.shape[1], x2 + padding)
        y2 = min(frame.shape[0], y2 + padding)

        cropped = frame[y1:y2, x1:x2]
        pre = preprocess(cropped)
        placa = aplicar_ocr(pre)
        if placa:
            return placa
    return None