import json
import re


def parse_component_details(part, component_string):
    # 제품명에서 불필요한 괄호와 괄호 안의 내용을 제거
    cleaned_string = re.sub(r'\s*\([^)]*\)', '', component_string).strip()

    # 가격 정보 추출
    price_match = re.search(r'(\d+원)', component_string)
    price = price_match.group(1) if price_match else '가격 정보 없음'

    # SSD 및 메모리에서 GB나 TB 용량을 포함시키기 위한 처리
    if 'SSD' in part or '메모리' in part:
        # 용량 정보만 유지
        capacity_match = re.search(r'(\d+GB|\d+TB)', component_string)
        capacity = capacity_match.group(1) if capacity_match else '용량 정보 없음'
        product_name = f"{cleaned_string} {capacity}"
    else:
        product_name = cleaned_string

    # 수량 정보 추출, 메모리의 경우 특별 처리
    quantity_match = re.search(r'x\s*(\d+)\s*개', component_string)
    quantity = quantity_match.group(1) if quantity_match else '1'

    return {'제품명': product_name, '가격': price, '수량': quantity}


def process_data(file_path):
    # 파일에서 JSON 데이터를 로드
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 각 항목의 'computer_estimate_data'를 파싱하여 'parts_price' 업데이트
    for entry in data:
        estimate_data = entry.get('computer_estimate_data', '')
        parts = re.findall(r'\[(.*?)\](.*?)(?=\[|$)', estimate_data)
        parts_price = {}
        for part, details in parts:
            if part not in ['조립PC관련', '견적왕']:  # 불필요한 파트 제거
                if '상세보기' in details:
                    details = details.split('상세보기')[0]
                component_info = parse_component_details(part, details)
                parts_price[part] = component_info

        # 업데이트된 'parts_price' 객체를 원래 데이터에 추가
        entry['parts_price'] = parts_price

    # 업데이트된 데이터를 다시 파일로 저장
    with open('updated_parts_details.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


# 파일 경로를 지정하고 데이터 처리 함수를 호출
file_path = 'processed_parts_details.json'
process_data(file_path)
