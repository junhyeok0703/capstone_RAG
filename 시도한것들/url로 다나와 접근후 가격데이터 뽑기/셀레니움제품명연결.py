from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import json

# Load your JSON data here
data = {
    "parts_price": [
        {"제품명": "AMD 라이젠5-4세대 5600", "가격": "131,540원", "수량": "1"},
        {"제품명": "ASUS PRIME B550M-A 대원CTS", "가격": "121,990원", "수량": "1"},
        # Add all other parts as per your actual JSON structure
    ]
}

# Setting up WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Function to update prices
def update_prices(data):
    base_url = 'https://search.danawa.com/dsearch.php?query='

    for part in data["parts_price"]:
        product_name = part["제품명"]
        url = base_url + product_name
        driver.get(url)
        driver.implicitly_wait(10)  # Wait for the page to load

        try:
            price_element = driver.find_element(By.CSS_SELECTOR, '.product_list ul li:first-child p.price_sect a strong')
            new_price = price_element.text + '원' if price_element else '가격 정보를 찾을 수 없습니다'
            part["가격"] = new_price  # Update the price in the JSON
        except Exception as e:
            print(f"Error updating price for {product_name}: {str(e)}")

    driver.quit()
    return data

# Update the prices
updated_data = update_prices(data)

# Print the updated JSON data
print(json.dumps(updated_data, indent=2, ensure_ascii=False))
