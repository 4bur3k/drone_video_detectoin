from ultralytics import YOLO
import yaml
    
model = YOLO('models/yolo11n.pt').export(format='ncnn')
