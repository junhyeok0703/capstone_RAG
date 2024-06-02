import json
import re

def load_data(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return json.load(file)

def extract_keywords(part_name, category):
    # 파워 서플라이의 경우 와트수와 제조사가 중요
    if category == '파워서플라이':
        watt_match = re.search(r'(\d+)W', part_name)
        watt = watt_match.group(0) if watt_match else ''
        brand_match = re.search(r'([a-zA-Z\s]+)\d+W', part_name)
        brand = brand_match.group(1).stripx() if brand_match else ''
        return f'{brand} {watt}'.strip()
    elif category == 'CPU':
        return re.search(r'(i[3579]-\d+|\d{4,5}X?)', part_name).group(0) if re.search(r'(i[3579]-\d+|\d{4,5}X?)', part_name) else part_name
    elif category == '메모리':
        return re.search(r'(DDR[34]-\d+)', part_name).group(0) if re.search(r'(DDR[34]-\d+)', part_name) else part_name
    elif category == '그래픽카드':
        return re.search(r'(RTX \d+|GTX \d+)', part_name).group(0) if re.search(r'(RTX \d+|GTX \d+)', part_name) else part_name
    return part_name  # 최소한의 이름을 반환

def find_price(part_name, category, prices):
    keyword = extract_keywords(part_name, category)
    for price_info in prices:
        if keyword.lower() in price_info['product'].lower():
            price = int(re.sub(r'[^\d]', '', price_info['price']))
            return price
    return 0

def process_estimates(estimate_data, price_data):
    for estimate in estimate_data:
        parts_description = estimate['computer_estimate_data']
        parts_price = {}
        total_price = 0

        for match in re.finditer(r'\[(.*?)\](.*?)상세보기', parts_description):
            category, part_name = match.groups()
            part_name = part_name.strip()
            part_price = find_price(part_name, category, price_data)
            parts_price[category] = f'{part_price}원'
            total_price += part_price

        estimate['parts_price'] = parts_price
        estimate['total_price'] = f'{total_price}원'

    return estimate_data


estimate_data = load_data('../견적왕 견적서 뽑기 크롤링/최종/3/updated_1year_crawling_estimated_data.json')
price_data = load_data('../견적왕 견적서 뽑기 크롤링/price.json')

# 계산
updated_estimates = process_estimates(estimate_data, price_data)


with open('final_estimates_with_prices.json', 'w', encoding='utf-8') as f:
    json.dump(updated_estimates, f, ensure_ascii=False, indent=4)
