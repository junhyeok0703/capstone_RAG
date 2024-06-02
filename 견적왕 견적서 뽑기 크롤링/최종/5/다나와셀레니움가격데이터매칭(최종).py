from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
from datetime import datetime

# JSON 데이터 로드
file_path = 'final_메모리부분고친가격넣기전데이터.json'
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Selenium WebDriver 설정
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 창 없이 실행
driver = webdriver.Chrome(service=service, options=options)

def update_prices(data):
    base_url = 'https://search.danawa.com/dsearch.php?query='
    start_time = time.time()  # 전체 프로그램 실행 시작 시간
    for quote in data:
        parts = quote.get("parts_price", {})  # parts_price를 사전으로 가져오고, 없으면 빈 사전 반환
        for part_key, part_value in parts.items():
            if isinstance(part_value, dict):  # part_value가 사전 형식인지 확인
                product_name = part_value.get("제품명")  # 각 부품의 '제품명'을 가져옴
                if product_name:  # 제품명이 있는 경우에만 실행
                    search_url = base_url + product_name.replace(" ", "+")
                    driver.get(search_url)
                    time.sleep(4)  # 페이지 로딩 대기

                    try:
                        price_element = WebDriverWait(driver, 8).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, '.product_list ul li:first-child p.price_sect a strong'))
                        )
                        part_value["가격"] = price_element.text + '원'  # 가격 업데이트
                    except Exception as e:
                        part_value["가격"] = '가격 정보를 찾을 수 없습니다'
                        print(f"{product_name}의 가격 정보를 찾을 수 없습니다: {e}")
            else:
                print(f"Unexpected data type for {part_key} in parts_price: {part_value}")

    driver.quit()
    return data

# 파일을 읽고 JSON 구조를 로드
with open('./final_메모리부분고친가격넣기전데이터.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 가격 정보 업데이트
updated_data = update_prices(data)

# 결과를 새 JSON 파일에 저장
with open('./최종가격데이터넣은데이터.json', 'w', encoding='utf-8') as file:
    json.dump(updated_data, file, indent=4, ensure_ascii=False)

