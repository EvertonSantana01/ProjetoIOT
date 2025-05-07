from ultralytics import YOLO

def treinar_stage2():
    modelo = YOLO("yolov8n.pt")  # ou yolov8s.pt, se quiser mais precisão
    modelo.train(
        data="placas/detector/ia/dataset/stage2_caracteres/data_caracteres.yaml",
        epochs=50,
        imgsz=640,
        batch=4,
        name="caracteres_stage2"
    )

if __name__ == "__main__":
    treinar_stage2()
