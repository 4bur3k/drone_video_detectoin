from ultralytics import YOLO
import cv2
import requests
import time
import os
import json
import yaml
import logging
import traceback

logging.basicConfig(
    filename='logs/detectorlog.log', 
    level=logging.INFO,      
    format='%(asctime)s [%(levelname)s] %(message)s',
)

# Настройки
with open('config.yaml') as f:
    cfg = yaml.safe_load(f)['inference']
    
MODEL = cfg['path']
CAM_INDEX = cfg['camera_index']
VIDEO_URL = cfg['video_url']
IMG_SIZE = cfg['img_size']
CONF = cfg['conf']
CHECK_CLASSES = cfg['classes']   
LOGFILE_PATH = cfg['log_path']
RES_DIR = cfg['res_img_dir']

def get_runnnig_state(self):
    with open('runtime.yaml') as f:
        runtime_flag = yaml.safe_load(f)['detector']['running']
        
    return runtime_flag

# DEPRECATED
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
    
    try:
        model = YOLO(MODEL)
        names = model.names
        logging.info(f'Model loaded: {model} for {list(names.values())}')
    except Exception as e:
        logging.error(f'Failed to load model: {e}\n{traceback.format_exc()}')
        return

    # получаем id нужных классов
    wanted_idxs = [k for k, v in names.items() if v in CHECK_CLASSES]
    
    try:
        results = model.track(
        source=CAM_INDEX,
        imgsz=IMG_SIZE,
        conf=CONF,
        classes=wanted_idxs,
        device="cpu",
        tracker="bytetrack.yaml",
        stream=True  
            )
    except Exception as e:
        logging.error(f'Failed to start tracking: {e}\n{traceback.format_exc()}')
        return
    
    #time for check runtime flags
    last_check = 0
    check_interval = 1.0

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
                    # print(f"[ALERT] Обнаружен {label} ({conf:.2f})")

                    logging.info(f'Detected: {label}, {conf}')

                    ts = int(time.time())
                    filename = os.path.join(RES_DIR, f"alert_{ts}.jpg")
                    cv2.imwrite(filename, frame)
        
        # Check if loop shall stop to stop
        now = time.time()
        if now - last_check > check_interval:
            # If running state == False -> stop
            if not get_runnnig_state():
                logging.info('Process stopped from UI')
                print('Stopped from UI')
                break
            
if __name__ == "__main__":
    detector()
