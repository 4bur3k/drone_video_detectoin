import streamlit as st
import pandas as pd
import os
from pathlib import Path
import shutil
import time

REPORT_PATH = 'reports/report.pdf'
DETECTIONS_DIR = Path("detections")

# ----- Сайдбар -----
st.sidebar.title("Панель управления")

# Кнопки старт/стоп (логика будет твоя)
if st.sidebar.button("▶ Start"):
    st.write("Запуск процесса...")  # вставь свою функцию

if st.sidebar.button("⏹ Stop"):
    st.write("Остановка процесса...")  # вставь свою функцию

# Очистка папки detections
if st.sidebar.button("🗑 Очистить detections"):
    if DETECTIONS_DIR.exists():
        shutil.rmtree(DETECTIONS_DIR)
        DETECTIONS_DIR.mkdir(exist_ok=True)
        st.sidebar.success("Папка detections очищена")

# Выбор FPS обработки
fps_option = st.sidebar.slider("Обрабатывать каждый N-й кадр", min_value=1, max_value=10, value=1)

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
st.write("Ниже таблица с данными:")

# Пример данных (ты будешь их наполнять из детектора)
data = {
    "Имя": ["Иван", "Мария", "Петр"],
    "Возраст": [25, 30, 22],
    "Город": ["Москва", "СПб", "Казань"]
}
df = pd.DataFrame(data)
st.dataframe(df)

# ----- Последнее изображение из detections -----
st.subheader("Последнее обнаружение")
if DETECTIONS_DIR.exists() and any(DETECTIONS_DIR.iterdir()):
    latest_file = max(DETECTIONS_DIR.glob("*.jpg"), key=os.path.getctime)
    st.image(str(latest_file), caption=f"Последний кадр: {latest_file.name}")
else:
    st.info("Нет сохранённых изображений в папке detections")

# ----- Информация по объектам -----
st.subheader("Последние объекты")
# Пример структуры (замени на реальную из детектора)
objects_data = [
    {"Класс": "person", "Confidence": 0.95, "ID": 1, "Время": "12:34:56"},
    {"Класс": "dog", "Confidence": 0.87, "ID": 2, "Время": "12:34:58"},
]
objects_df = pd.DataFrame(objects_data)
st.dataframe(objects_df)

# ----- Количество объектов по классам -----
st.subheader("Статистика по классам")
class_counts = objects_df['Класс'].value_counts().reset_index()
class_counts.columns = ['Класс', 'Количество']
st.table(class_counts)
