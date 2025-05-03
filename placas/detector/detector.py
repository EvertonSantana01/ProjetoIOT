import cv2
import numpy as np
from ultralytics import YOLO
from .ocr import aplicar_ocr
from .utils import preprocess
import easyocr  # Importe easyocr aqui para o teste

model = YOLO('license_plate_detector.pt')
reader_test = easyocr.Reader(['pt', 'en'], gpu=False) # Inicialize um leitor local para o teste

def detectar_placa(frame):
    results = model.predict(frame, conf=0.15, iou=0.5)[0] # Limiar de confiança reduzido para 0.15
    high_confidence_ocr = None
    for result in results.boxes:
        x1, y1, x2, y2 = map(int, result.xyxy[0])
        padding = 30
        x1 = max(0, x1 - padding)
        y1 = max(0, y1 - padding)
        x2 = min(frame.shape[1], x2 + padding)
        y2 = min(frame.shape[0], y2 + padding)

        cropped = frame[y1:y2, x1:x2]
        pre = preprocess(cropped)

        cv2.imwrite("ultima_placa.jpg", cropped)
        cv2.imwrite("ultima_placa_pre.jpg", pre)

        print(f"Tipo de 'pre': {type(pre)}")
        print(f"Shape de 'pre': {pre.shape}")
        print(f"Tipo de dado de 'pre': {pre.dtype}")

        # --- Bloco de teste do easyocr com array NumPy ---
        try:
            print("--- Teste direto com easyocr ---")
            detection_result_test = reader_test.readtext(pre, allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            print("Resultado do teste OCR:", detection_result_test)
            for _, text, conf in detection_result_test:
                if conf > 0.45:
                    high_confidence_ocr = text.upper().replace('-', '').replace(' ', '')
                    break # Pega a primeira leitura com alta confiança
        except Exception as e:
            print(f"Erro no teste direto do easyocr: {e}")
        # --- Fim do bloco de teste ---

        placa = aplicar_ocr(pre)
        print("🔍 Resultado OCR:", placa)

        if placa:
            return placa
        elif high_confidence_ocr:
            print(f"⚠️ Retornando leitura de alta confiança '{high_confidence_ocr}' mesmo sem validação formal.")
            return high_confidence_ocr

    return None