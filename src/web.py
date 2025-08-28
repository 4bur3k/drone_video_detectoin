import streamlit as st
import pandas as pd
import os
from pathlib import Path
import shutil
import time
import plotly.express as px
from report_generator import create_pdf
import yaml
import logging
import traceback

logging.basicConfig(
    filename='logs/uilog.log', 
    level=logging.INFO,      
    format='%(asctime)s [%(levelname)s] %(message)s',
)

def set_detector_running_state(state: bool):
    with open('runtime.yaml') as f:
        data = yaml.safe_load(f)
        
    if isinstance(state, bool):
        data['detector']['running'] = state
                
        with open('runtime.yaml', 'w') as f:
            yaml.safe_dump(data, f)
            
        logging.info(f'Runtime state detector:running changed to {state}')
            
    else: 
        logging.warning(f'State expected to be bool, got: {type(state)}: {state}')
        
        
        
def set_detector_fps_state(fps: int):
    with open('runtime.yaml') as f:
        data = yaml.safe_load(f)
        
    if isinstance(fps, int):
        data['detector']['fps'] = fps
        
        with open('runtime.yaml', 'w') as f:
            yaml.safe_dump(data, f)
            
    else: 
        logging.info(f'Runtime state detector:fps changed to {fps}')
        
        logging.warning(f'State expected to be int, got: {type(fps)}: {fps}')

REPORT_PATH = 'reports/report.pdf'
DETECTIONS_DIR = Path("detections")

# ----- Сайдбар -----
st.sidebar.title("Панель управления")

if "running_state" not in st.session_state:
    st.session_state.running_state = False

# Кнопки старт/стоп (логика будет твоя)
if st.sidebar.button("▶ Start"):
    logging.info('Start button pressed')
    set_detector_running_state(True)
    
if st.sidebar.button("⏹ Stop"):
    logging.info('Stop button pressed')
    # TURNED OFF FOR DEBUGGING
    # set_detector_running_state(False)
    create_pdf()
    

# Очистка папки detections
if st.sidebar.button("🗑 Очистить detections"):
    if DETECTIONS_DIR.exists():
        shutil.rmtree(DETECTIONS_DIR)
        DETECTIONS_DIR.mkdir(exist_ok=True)
        st.sidebar.success("Папка detections очищена")
        
        logging.info('detections/ cleared')

# Выбор FPS обработки
fps_option = st.sidebar.slider("Обрабатывать каждый N-й кадр", min_value=1, max_value=10, value=5)
logging.info(f'New fps value choosen: {fps_option}')

# Кнопка скачать отчет
if os.path.exists(REPORT_PATH):
    with open(REPORT_PATH, "rb") as f:
        st.sidebar.download_button(
            label="📥 Скачать отчет",
            data=f,
            file_name=os.path.basename(REPORT_PATH),
            mime="application/pdf"
        )
        
# ----- Центральная часть -----
st.title("Пример интерфейса")

# ----- Последнее изображение из detections -----
# st.subheader("Последнее обнаружение")
# if DETECTIONS_DIR.exists() and any(DETECTIONS_DIR.iterdir()):
#     latest_file = max(DETECTIONS_DIR.glob("*.jpg"), key=os.path.getctime)
#     st.image(str(latest_file), caption=f"Последний кадр: {latest_file.name}")
# else:
#     st.info("Нет сохранённых изображений в папке detections")

# ----- Информация по объектам -----
st.subheader("Последние объекты")
# Пример структуры (замени на реальную из детектора)
objects_data = [
    {"Тип": "Man", "Confidence": 0.95, "ID": 1, "Время": "12:34:56"},
    {"Тип": "Dog", "Confidence": 0.95, "ID": 1, "Время": "12:34:56"}
]
objects_df = pd.DataFrame(objects_data)
st.dataframe(objects_df)

# ----- Количество объектов по классам -----
st.subheader("Статистика по классам")

try:
    class_counts = objects_df['Тип'].value_counts().reset_index()
    class_counts.columns = ['Тип', 'Количество']

    fig = px.bar(class_counts, x='Тип', y='Количество', color='Тип',
                text='Тип', title="Количество объектов по классам")
    st.plotly_chart(fig, use_container_width=True)
    
except Exception as e:
    logging.error(f'Error with chart: {e}\n{traceback.format_exc()}')

