from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Selenium 드라이버 설정
service = Service()
driver = webdriver.Chrome(service=service)

# 웹페이지 URL
url = 'https://search.danawa.com/dsearch.php?query={제품명}'

# 웹페이지 열기
driver.get(url)

# 페이지가 완전히 로드될 때까지 기다림
driver.implicitly_wait(10)

# 'product_list' 클래스 내부의 첫 번째 'li' 태그 내의 'price_sect' 클래스를 가진 'p' 태그 안의 'a' 태그 내의 'strong' 태그를 찾기
price_element = driver.find_element(By.CSS_SELECTOR, '.product_list ul li:first-child p.price_sect a strong')

# 가격 텍스트 추출
price = price_element.text if price_element else '가격 정보를 찾을 수 없습니다'

print(price)

# 드라이버 종료
driver.quit()
