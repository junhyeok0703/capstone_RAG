import requests
from bs4 import BeautifulSoup

# 페이지 URL
url = 'https://search.danawa.com/dsearch.php?query=ASUS+PRIME+B550M-A+%EB%8C%80%EC%9B%90CTS%5C'

# HTTP 요청을 보내고 응답을 받음
response = requests.get(url)

# 응답 내용을 HTML 파싱
soup = BeautifulSoup(response.text, 'html.parser')

# 필요한 정보를 포함하는 요소 찾기 (CSS 선택자 사용)
price_element = soup.select_one('.product_list ul li:first-child p.price_sect a strong')

# 가격 정보 추출
price = price_element.text.strip() + '원' if price_element else '가격 정보를 찾을 수 없습니다'

print(price)
