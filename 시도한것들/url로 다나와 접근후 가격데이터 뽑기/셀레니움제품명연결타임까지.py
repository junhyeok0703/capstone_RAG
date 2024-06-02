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
file_path = '../견적왕 견적서 뽑기 크롤링/최종/RAG샘플데이터테스트/sample.json'
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
                    time.sleep(5)  # 페이지 로딩 대기

                    try:
                        price_element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located(
                                (By.CSS_SELECTOR, '.product_list ul li:first-child p.price_sect a strong'))
                        )
                        new_price = price_element.text + '원'
                        part_value["가격"] = new_price  # 가격 업데이트
                        print(f"Updated {product_name}: {new_price} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    except Exception as e:
                        part_value["가격"] = '가격 정보를 찾을 수 없습니다'
                        print(f"Failed to update {product_name} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {e}")
            else:
                print(f"Unexpected data type for {part_key} in parts_price: {part_value}")

    driver.quit()
    end_time = time.time()  # 전체 프로그램 실행 종료 시간
    print(f"Program completed in {end_time - start_time:.2f} seconds")


# 파일을 읽고 JSON 구조를 로드
with open('../견적왕 견적서 뽑기 크롤링/최종/RAG샘플데이터테스트/sample.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 가격 정보 업데이트
updated_data = update_prices(data)

# 결과를 새 JSON 파일에 저장
with open('../../견적왕 견적서 뽑기 크롤링/최종/RAG샘플데이터테스트/가격데이터넣은sample.json', 'w', encoding='utf-8') as file:
    json.dump(updated_data, file, indent=4, ensure_ascii=False)
