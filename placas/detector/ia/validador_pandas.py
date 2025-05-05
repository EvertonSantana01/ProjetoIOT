import pandas as pd
import re

def validar_placa(placa_ocr):
    """
    Valida e corrige a placa detectada com base em padrões brasileiros
    e sugere substituições para caracteres semelhantes.
    """

    if not placa_ocr or not isinstance(placa_ocr, str):
        return None

    placa = placa_ocr.upper().replace(" ", "").strip()

    # Dicionário de caracteres comumente confundidos (OCR vs Placa real)
    substituicoes = {
        "0": "O", "1": "I", "2": "Z", "5": "S", "8": "B",
        "O": "0", "I": "1", "Z": "2", "S": "5", "B": "8"
    }

    # Geração de variações possíveis com substituições mapeadas
    variacoes = {placa}
    for i, c in enumerate(placa):
        if c in substituicoes:
            nova = placa[:i] + substituicoes[c] + placa[i+1:]
            variacoes.add(nova)

    # Regex dos padrões de placa
    regex_mercosul = r"^[A-Z]{3}[0-9][A-Z][0-9]{2}$"
    regex_antiga = r"^[A-Z]{3}[0-9]{4}$"

    # Cria DataFrame com todas variações
    df = pd.DataFrame({"placa_variante": list(variacoes)})

    # Valida se alguma variante bate com os padrões
    df["tipo"] = df["placa_variante"].apply(lambda x: "mercosul" if re.match(regex_mercosul, x)
                                            else ("antiga" if re.match(regex_antiga, x) else None))
    df = df.dropna(subset=["tipo"])

    if df.empty:
        return None

    # Retorna a primeira placa válida com tipo
    resultado = df.iloc[0]
    return {
        "placa_corrigida": resultado["placa_variante"],
        "tipo": resultado["tipo"]
    }
