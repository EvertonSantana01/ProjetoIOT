import cv2
import easyocr
import numpy as np
from ultralytics import YOLO
import re
import os

# Carrega o modelo YOLO especializado para detecção de placas
model = YOLO('license_plate_detector.pt')

# Inicia o OCR
reader = easyocr.Reader(['pt', 'en'], gpu=False)

# Arquivo de saída
output_file = "placas_detectadas.txt"
if not os.path.exists(output_file):
    open(output_file, 'w').close()

# Abre a câmera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Aumentar resolução
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

def preprocess(cropped_img):
    """Aplica filtros para melhorar a imagem antes do OCR"""
    gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    gray = cv2.equalizeHist(gray)
    return gray

def validar_placa(texto):
    """Confere se o texto parece uma placa BR"""
    padrao = r'^[A-Z]{3}[0-9][0-9A-Z][0-9]{2}$'
    return re.match(padrao, texto)

# Set de placas já detectadas (para evitar duplicadas)
placas_detectadas_set = set()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (1280, 720))

    # Aumenta sensibilidade: conf_threshold menor
    results = model.predict(frame, conf=0.25, iou=0.5)[0]
    placas_detectadas = []

    for result in results.boxes:
        x1, y1, x2, y2 = map(int, result.xyxy[0])

        padding = 30  # Mais padding para motos/placas pequenas
        x1_p = max(0, x1 - padding)
        y1_p = max(0, y1 - padding)
        x2_p = min(frame.shape[1], x2 + padding)
        y2_p = min(frame.shape[0], y2 + padding)

        cropped = frame[y1_p:y2_p, x1_p:x2_p]
        pre_cropped = preprocess(cropped)

        # OCR
        ocr_results = reader.readtext(pre_cropped)

        for bbox, text, conf in ocr_results:
            text = text.upper().replace(' ', '').replace('-', '')

            if conf > 0.4 and validar_placa(text):  # Aumenta chance de detectar
                placas_detectadas.append((text, (x1, y1, x2, y2)))

    # Desenhar as detecções
    for placa_texto, (x1, y1, x2, y2) in placas_detectadas:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, placa_texto, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Salvar se for uma placa nova
        if placa_texto not in placas_detectadas_set:
            placas_detectadas_set.add(placa_texto)
            with open(output_file, 'a') as f:
                f.write(f"{placa_texto}\n")
            print(f"Placa detectada e salva: {placa_texto}")

    # Mostrar o frame
    cv2.imshow('Detecção de Placas', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()