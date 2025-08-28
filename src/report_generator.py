from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Image, Spacer
from reportlab.lib.units import inch
import os
import yaml

# Настройки
with open('config.yaml') as f:
    cfg = yaml.safe_load(f)

def create_pdf(filename="reports/report.pdf"):
    img_dir = cfg['inference']['res_img_dir']
    images = sorted(os.listdir(img_dir)) 
    
    if not images:
        print("В папке detections нет изображений")
        return
    
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []

    max_width, max_height = A4  

    for img_name in images:
        img_path = os.path.join(img_dir, img_name)

        try:
            im = Image(img_path)
            # подгонкой под ширину страницы
            im._restrictSize(max_width - inch, max_height - inch) 
            elements.append(im)
            elements.append(Spacer(1, 0.3 * inch))  
        except Exception as e:
            print(f"Ошибка при добавлении {img_path}: {e}")

    # Генерация PDF
    doc.build(elements)
    print(f"'{filename}' создан!")

if __name__ == "__main__":
    create_pdf()
