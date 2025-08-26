import streamlit as st
import pandas as pd
import os
from pathlib import Path

REPORT_PATH = 'reports/report.pdf'
DETECTIONS_DIR = Path("detections")

# ----- Сайдбар -----
st.sidebar.title("Панель управления")

# Кнопки старт/стоп (логика будет твоя)
if st.sidebar.button("▶ Start"):
    st.write("Запуск процесса...")  # тут вставишь свою функцию

if st.sidebar.button("⏹ Stop"):
    st.write("Остановка процесса...")  # тут вставишь свою функцию

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

# Пример данных
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
