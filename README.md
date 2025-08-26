# Запуск:
*Запускаем все из корня ```cd /drone_video_detection/```*

### Запуск детекции
1. Активируем виртуальную среду ```source venv/bin/activate```

2. Запускаем ```python3 src/export_model.py```

3. Переносим содержимое ./models/ в ./src/models/ (потом зафикшу)

4. Запускаем TCP поток командой: 
```
rpicam-vid -t 0 -n --vflip --codec libav --libav-format mpegts -o tcp://0.0.0.0:8888?listen=1
```
Либо в `detection.py` указываем в парамеры модели `source=CAM_INDEX`

5. Теперь можно запустить деткцию ```python3 src/detector.py```
Запускается трекинг. Каждый уникальный объект в сцене сохраняется в `./detections/`. 
Для экспериментов можно редактировать ./config.yaml, в т.ч. img_size, device, 


