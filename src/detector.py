# yolov11_event_detector.py
from ultralytics import YOLO
import cv2
import requests
import time
import os
import json

# Настройки
MODEL = "yolo11n.pt"
CAM_INDEX = 0
IMG_SIZE = 320
CONF = 0.35
CHECK_CLASSES = ["person"]   # интересующие классы
LOGFILE_PATH = 'alerts.json'
SAVE_DIR = 'detections'

def log_alert(label, conf):
    entry = {'class': label, 'conf:': conf, 'time': time.time()}
    
    if not os.path.exists(LOGFILE_PATH):
        with open(LOGFILE_PATH, "w", encoding="utf-8") as f:
            json.dump([], f)

    # читаем текущие записи
    with open(LOGFILE_PATH, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []

    # добавляем новое событие
    data.append(entry)

    # сохраняем обратно
    with open(LOGFILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def detector():
            
    model = YOLO(MODEL)
    names = model.names

    # получаем id нужных классов
    wanted_idxs = [k for k, v in names.items() if v in CHECK_CLASSES]
    
    
    results = model.track(
    source=CAM_INDEX,
    imgsz=IMG_SIZE,
    conf=CONF,
    classes=wanted_idxs,
    device="cpu",
    tracker="bytetrack.yaml",
    stream=True  
        )

    seen_ids = set()
    for r in results:
        frame = r.orig_img
        if len(r.boxes) > 0:
            for box in r.boxes:
                cls = int(box.cls[0].cpu().numpy())
                label = names.get(cls, str(cls))
                track_id = int(box.id[0].cpu().numpy()) if box.id is not None else -1
                conf = float(box.conf[0].cpu().numpy())

                if track_id not in seen_ids:
                    seen_ids.add(track_id)
                    print(f"[ALERT] Обнаружен {label} ({conf:.2f})")
                    log_alert(label, conf)

                    ts = int(time.time())
                    filename = os.path.join(SAVE_DIR, f"alert_{ts}.jpg")
                    cv2.imwrite(filename, frame)
                    print(f"[IMG] Сохранено: {filename}")

if __name__ == "__main__":
    detector()
