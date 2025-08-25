from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
import os

def create_pdf(filename="report.pdf"):
    images = os.listdir(conf['res_images_dir'])
    # Создаём PDF-документ
    doc = SimpleDocTemplate(filename, pagesize=A4)

    # Заготовка для элементов (текст, таблицы, картинки и т.д.)
    elements = []

    # Используем стандартные стили
    styles = getSampleStyleSheet()

    # Заголовок
    title = Paragraph("Project report", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 20))  # отступ

    # Текст абзаца
    text = Paragraph(
        "Just yet another paragraph"
        "Some more text",
        styles['Normal']
    )
    elements.append(text)

    # Генерация PDF
    doc.build(elements)
    print(f"PDF файл '{filename}' успешно создан!")

if __name__ == "__main__":
    create_pdf()
