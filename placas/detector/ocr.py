import easyocr
import re

reader = easyocr.Reader(['pt', 'en'], gpu=False)

def validar_placa(texto):
    padrao = r'^[A-Z]{3}[0-9][0-9A-Z][0-9]{2}$'
    return re.match(padrao, texto)

def aplicar_ocr(img):
    ocr_results = reader.readtext(img, allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    for _, text, conf in ocr_results:
        text = text.upper().replace('-', '').replace(' ', '')
        print(f"🔠 OCR detectou: {text} (confiança {conf:.2f})")
        if conf > 0.4 and validar_placa(text):
            return text
    return None
