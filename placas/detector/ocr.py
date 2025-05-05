import easyocr
import re
import numpy as np
import cv2  # Certifique-se de que cv2 está importado
from placas.detector.ia.validador_pandas import validar_placa
from placas.detector.ia.preprocessador_imagem import melhorar_imagem_placa


reader = easyocr.Reader(['pt', 'en'], gpu=False)

def validar_placa_completa(texto):
    """Valida placas nos formatos Mercosul (ABC1D23) e Antigo (ABC1234)."""
    if len(texto) == 7:
        # Validação para Mercosul (ABC1D23)
        if (texto[0].isalpha() and texto[0].isupper() and
            texto[1].isalpha() and texto[1].isupper() and
            texto[2].isalpha() and texto[2].isupper() and
            texto[3].isdigit() and
            texto[4].isalpha() and texto[4].isupper() and
            texto[5].isdigit() and
            texto[6].isdigit()):
            return True
        # Validação para Antigo (ABC1234)
        elif (texto[0].isalpha() and texto[0].isupper() and
              texto[1].isalpha() and texto[1].isupper() and
              texto[2].isalpha() and texto[2].isupper() and
              texto[3].isdigit() and
              texto[4].isdigit() and
              texto[5].isdigit() and
              texto[6].isdigit()):
            return True
    return False

def substituir_similares(texto):
    """Substitui caracteres semelhantes COM MAIOR CAUTELA, focando em erros comuns em placas (SEM 'I'/'1')."""
    substituicoes_especificas = {
        'O': '0',
        '0': 'O',
        'l': '1',
        'L': '1',
        '5': 'S',
        'S': '5',
        '2': 'Z',
        'Z': '2',
        '8': 'B',
        'B': '8',
    }
    novo_texto = ""
    for char in texto:
        novo_texto += substituicoes_especificas.get(char, char)
    return novo_texto



def aplicar_ocr(img_np_array):
    """
    Aplica OCR e usa heurística com Pandas para validar e corrigir placas.
    """
    leitura_mais_confiável = None
    confiança_mais_alta = 0.0
    leitura_placa_tamanho_correto = None
    confiança_placa_tamanho_correto = 0.0

    try:
        # 🔧 Pré-processamento da imagem
        imagem_preprocessada = melhorar_imagem_placa(img_np_array)

        # OCR na imagem melhorada
        ocr_results = reader.readtext(imagem_preprocessada, allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

        for _, text, conf in ocr_results:
            text_limpo = text.upper().replace('-', '').replace(' ', '')
            print(f"🔠 OCR detectou (limpo): {text_limpo} (confiança {conf:.2f})")

            texto_corrigido_o_zero = "".join(['0' if i in [3, 4, 5, 6] and c == 'O' else c for i, c in enumerate(text_limpo)])

            if conf > confiança_mais_alta:
                confiança_mais_alta = conf
                leitura_mais_confiável = texto_corrigido_o_zero

            if len(texto_corrigido_o_zero) == 7:
                if conf > confiança_placa_tamanho_correto:
                    confiança_placa_tamanho_correto = conf
                    leitura_placa_tamanho_correto = texto_corrigido_o_zero

                if conf > 0.8 and validar_placa_completa(texto_corrigido_o_zero):
                    print(f"✅ Placa válida detectada (alta confiança): {texto_corrigido_o_zero}")
                    return texto_corrigido_o_zero

                elif conf <= 0.7:
                    texto_substituido = substituir_similares(texto_corrigido_o_zero)
                    if validar_placa_completa(texto_substituido):
                        print(f"✅ Placa válida com substituições: {texto_substituido}")
                        return texto_substituido
                    elif validar_placa_completa(texto_corrigido_o_zero):
                        return texto_corrigido_o_zero

        if leitura_placa_tamanho_correto:
            resultado_validacao = validar_placa(leitura_placa_tamanho_correto)
            if resultado_validacao and resultado_validacao["placa_corrigida"]:
                print(f"✅ Validação Pandas aplicada: {resultado_validacao}")
                placa = resultado_validacao["placa_corrigida"]
                tipo = resultado_validacao["tipo"]
                print(f"🔍 Tipo de placa detectado: {tipo}")
                return placa

        elif leitura_mais_confiável:
            resultado_validacao = validar_placa(leitura_mais_confiável)
            if resultado_validacao and resultado_validacao["placa_corrigida"]:
                print(f"✅ Validação Pandas fallback: {resultado_validacao}")
                return resultado_validacao["placa_corrigida"]

        print("❌ Nenhuma placa válida encontrada.")
        return None

    except Exception as e:
        print(f"Erro ao processar a imagem OCR: {e}")
        return None
