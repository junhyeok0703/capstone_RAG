import pandas as pd
import re

# 새로 업로드된 파일 경로 업데이트
new_file_path = 'List_of_program_specifications1.csv'

# 인코딩을 'utf-8-sig'로 설정하여 파일 읽기
df_new = pd.read_csv(new_file_path, encoding='utf-8-sig')


# 카테고리별로 데이터를 분리하는 함수 정의
def extract_data(data):
    # 카테고리 분류를 위한 키워드 리스트
    keywords = ["최소사양", "권장사양", "FHD 해상도", "QHD 해상도", "4K UHD 해상도"]
    pattern = "|".join(keywords)

    # 데이터를 줄 단위로 분리
    lines = data.split('\n')

    # 결과를 저장할 딕셔너리
    result = {
        "program_name": "",
        "minimum_spec": "",
        "recommended_spec": "",
        "FHD_spec": "",
        "QHD_spec": "",
        "4K_spec": ""
    }

    current_key = None
    for line in lines:
        # 프로그램 이름 추출
        if result["program_name"] == "":
            result["program_name"] = line.split(" ")[0]

        # 카테고리 키워드를 찾으면 현재 키 변경
        if re.search(pattern, line):
            if "최소사양" in line:
                current_key = "minimum_spec"
            elif "권장사양" in line:
                current_key = "recommended_spec"
            elif "FHD 해상도" in line:
                current_key = "FHD_spec"
            elif "QHD 해상도" in line:
                current_key = "QHD_spec"
            elif "4K UHD 해상도" in line:
                current_key = "4K_spec"
        else:
            # 현재 키에 해당하는 카테고리에 줄 추가
            if current_key:
                result[current_key] += line + '\n'

    return result


# 새로운 데이터 프레임을 생성하기 위한 준비
data_columns = ["program_name", "minimum_spec", "recommended_spec", "FHD_spec", "QHD_spec", "4K_spec"]
data_rows = []

# 모든 셀 데이터에 대해 처리
for cell_data in df_new.iloc[:, 0]:
    data_rows.append(extract_data(cell_data))

# 결과를 데이터 프레임으로 변환
df_extracted = pd.DataFrame(data_rows, columns=data_columns)

# 데이터 프레임을 CSV 파일로 저장 (UTF-8-SIG 인코딩 사용)
output_file_path = 'output_file.csv'
df_extracted.to_csv(output_file_path, index=False, encoding='utf-8-sig')

print(f"Data has been successfully saved to {output_file_path}")
