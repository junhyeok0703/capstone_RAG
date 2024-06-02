import json

# 파일 로드 함수
def load_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

# 성능 분류 함수
def classify_performance(price):
    # 가격 변환 (문자열에서 정수로)
    price = int(price.replace("원", "").replace(",", ""))
    if price > 2000000:
        return '고성능'
    else:
        return '저성능'

# 데이터 처리 및 카테고리 추가 함수
def process_data(data):
    for item in data:
        # 가격을 이용한 성능 분류
        item['Performance'] = classify_performance(item['total_price'])
    return data

# 메인 함수
def main():
    # 입력 파일명 지정
    input_filename = '총가격데이터sample.json'
    # 출력 파일명 지정
    output_filename = 'processed_data.json'
    # 데이터 로드
    data = load_data(input_filename)
    # 데이터 처리
    processed_data = process_data(data)
    # 결과를 JSON 파일로 저장
    with open(output_filename, 'w', encoding='utf-8') as file:
        json.dump(processed_data, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
