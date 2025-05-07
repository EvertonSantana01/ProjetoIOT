from ultralytics import YOLO

def treinar_modelo():
    modelo = YOLO("yolov8n.pt")  # ou "yolov5s.pt" se preferir

    modelo.train(
        data="placas/detector/ia/dataset/stage1_placa_veiculo/data.yaml",
        epochs=50,
        imgsz=640,
        batch=4,
        name="placa_stage1_treino"
    )

if __name__ == "__main__":
    treinar_modelo()
