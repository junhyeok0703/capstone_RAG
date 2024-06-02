import re
import pytesseract
import requests
from PIL import Image
from io import BytesIO

pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

def clean_text(extracted_text):
    cleaned_text = re.sub(r'[^가-힣a-zA-Z0-9\s\.,?!]', '', extracted_text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    return cleaned_text


image_url = "https://shop-cdn.sidiz.com/_outside/GC/GC-PRO_1.jpg"

response = requests.get(image_url)
if response.status_code == 200:
    image = Image.open(BytesIO(response.content))
    extracted_text = pytesseract.image_to_string(image, lang='eng+kor')
    cleaned_text = clean_text(extracted_text)

    print(f"Extracted and Cleaned Text:\n{cleaned_text}\n")


    with open("extracted_text.txt", "w", encoding="utf-8") as text_file:
        text_file.write(cleaned_text)
    print("Text successfully saved to 'extracted_text.txt'")
else:
    print(f"Failed to retrieve image from {image_url}")
