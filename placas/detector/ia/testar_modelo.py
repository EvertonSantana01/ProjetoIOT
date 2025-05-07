from ultralytics import YOLO
import cv2

# Caminho do modelo treinado
modelo = YOLO("runs/detect/placa_stage1_treino2/weights/best.pt")

# Caminho da imagem para testar
imagem_teste = "placas/detector/ia/dataset/stage1_placa_veiculo/images/placa_01.png"

# Fazendo a predição
resultados = modelo.predict(source=imagem_teste, save=True, conf=0.3)

# Exibindo a imagem com as detecções
for r in resultados:
    im_bgr = r.plot()  # desenha as detecções
    cv2.imshow("Resultado da Detecção", im_bgr)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
