import os
import base64
import cv2
import numpy as np
from django.shortcuts import render
from django.http import JsonResponse
from .detector.detector import detectar_placa

# Caminho absoluto para salvar o arquivo na raiz do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
output_file = os.path.join(BASE_DIR, 'placas_detectadas.txt')

# Conjunto para evitar salvar placas repetidas
placas_detectadas_set = set()

# Rota para exibir a página da câmera
def camera_view(request):
    return render(request, 'placas/camera.html')

# Função que detecta placas de forma contínua
def detectar_placa_continua(frame):
    placa = detectar_placa(frame)
    if placa and placa not in placas_detectadas_set:
        placas_detectadas_set.add(placa)
        # Abre (ou cria) o arquivo e adiciona a nova placa
        with open(output_file, 'a') as f:
            f.write(f"{placa}\n")
        print(f"Placa detectada e salva: {placa}")
    else:
        print("Placa já registrada ou não detectada.")

# Rota para processar a imagem e detectar a placa (Agora contínuo)
def detectar_placa_view(request):
    if request.method == 'POST':
        import json
        # Carrega os dados da imagem em base64
        data = json.loads(request.body)
        img_data = data['imagem'].split(',')[1]
        img_bytes = base64.b64decode(img_data)
        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Detecta a placa e processa automaticamente
        detectar_placa_continua(frame)

        return JsonResponse({'status': 'Placa detectada e salva automaticamente'})

