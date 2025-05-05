import cv2
import numpy as np

def melhorar_imagem_placa(img):
    """
    Aplica filtros adaptativos e morfológicos para melhorar a legibilidade da placa.
    """
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Filtro bilateral para preservar bordas e reduzir ruído
        blur = cv2.bilateralFilter(gray, 11, 17, 17)

        # Aumentar contraste
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        contrast = clahe.apply(blur)

        # Binarização adaptativa
        thresh = cv2.adaptiveThreshold(contrast, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 25, 15)

        # Morfologia para fechar espaços
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        morf = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        return morf

    except Exception as e:
        print(f"Erro ao melhorar imagem: {e}")
        return img
