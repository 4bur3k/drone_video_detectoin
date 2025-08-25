import streamlit as st
import pandas as pd
import os

REPORT_PATH = 'reports/report.pdf'
VIDEO_PATH = 'video/video.mp4'

# ----- Сайдбар -----
st.sidebar.title("Панель управления")

if os.path.exists(REPORT_PATH):
    with open(REPORT_PATH, "rb") as f:
        st.sidebar.download_button(
            label="📥 Скачать отчет",
            data=f,
            file_name=os.path.basename(REPORT_PATH),
            mime="text/plain"
        )
        
if os.path.exists(VIDEO_PATH):
    with open(VIDEO_PATH, "rb") as f:
        st.sidebar.download_button(
            label="📥 Скачать видео",
            data=f,
            file_name=os.path.basename(VIDEO_PATH),
            mime="text/plain"
        )
# ----- Центральная часть -----
st.title("Пример интерфейса")
st.write("Ниже таблица с данными:")

# Пример данных (замени на свои)
data = {
    "Имя": ["Иван", "Мария", "Петр"],
    "Возраст": [25, 30, 22],
    "Город": ["Москва", "СПб", "Казань"]
}
df = pd.DataFrame(data)

st.dataframe(df)
