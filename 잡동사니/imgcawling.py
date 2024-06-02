import re
import pytesseract
import requests
from PIL import Image
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# Tesseract-OCR 설치 경로 지정
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

def clean_text(extracted_text):
    # 추출된 텍스트 정리
    cleaned_text = re.sub(r'[^가-힣a-zA-Z0-9\s\.,?!]', '', extracted_text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    return cleaned_text

# 이미지 URL
image_url = "https://shop-cdn.sidiz.com/_outside/GC/GC-PRO_1.jpg"
response = requests.get(image_url)

if response.status_code == 200:
    image = Image.open(BytesIO(response.content))
    extracted_text = pytesseract.image_to_string(image, lang='eng+kor')
    cleaned_text = clean_text(extracted_text)

    # PDF 파일로 저장
    pdf_filename = "extracted_text.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    # TTF 글꼴 등록 및 설정
    pdfmetrics.registerFont(TTFont('NanumGothic', 'NanumGothic-Regular.ttf'))
    c.setFont("NanumGothic", 12)

    text_object = c.beginText(40, 750)
    for line in cleaned_text.split('\n'):
        text_object.textLine(line)
    c.drawText(text_object)

    c.save()
    print(f"Text successfully saved to '{pdf_filename}'")
else:
    print(f"Failed to retrieve image from {image_url}")
