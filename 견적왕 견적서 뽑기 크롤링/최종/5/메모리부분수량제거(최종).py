import json

# 파일 경로 정의
file_path = 'final_parts_details_with_prices.json'
output_file_path = 'final_메모리부분고친가격넣기전데이터.json'

# JSON 파일 로드
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 메모리 제품명에서 "x 2 개" 및 "용량 정보 없음" 제거
for quote in data:
    if "메모리" in quote["parts_price"]:
        memory_product_name = quote["parts_price"]["메모리"]["제품명"]
        # "x 2 개" 및 "용량 정보 없음" 제거
        cleaned_name = memory_product_name.replace("x 2 개", "").replace("용량 정보 없음", "").strip()
        # 수정된 제품명 저장
        quote["parts_price"]["메모리"]["제품명"] = cleaned_name

# 수정된 데이터를 새 JSON 파일로 저장
with open(output_file_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(f"Updated file saved to: {output_file_path}")
