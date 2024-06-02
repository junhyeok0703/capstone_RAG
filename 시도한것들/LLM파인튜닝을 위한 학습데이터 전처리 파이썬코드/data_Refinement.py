import pandas as pd
import os
# 파일 읽기
df_large = pd.read_csv('output_file.csv')

# 질문 템플릿 확장 및 추가
extended_templates = [
    ("최소사양은 무엇인가요?", "minimum_spec"),
    ("이 프로그램을 실행하기 위한 최소 요구 사항은?", "minimum_spec"),
    ("최소한으로 필요한 사양을 알려주세요.", "minimum_spec"),
    ("권장사양은 무엇인가요?", "recommended_spec"),
    ("이 프로그램의 최적 사양은 무엇인가요?", "recommended_spec"),
    ("권장하는 시스템 사양이 궁금합니다.", "recommended_spec"),
    ("FHD 해상도 추천 견적서는 어떻게 되나요?", "FHD_spec"),
    ("FHD 해상도에서 사용할 수 있는 컴퓨터 견적이 궁금해요.", "FHD_spec"),
    ("1920x1080 해상도에 최적화된 견적을 알려주세요.", "FHD_spec"),
    ("QHD 해상도 추천 견적서는 어떻게 되나요?", "QHD_spec"),
    ("QHD 해상도에 적합한 PC 구성을 알고 싶습니다.", "QHD_spec"),
    ("2560x1440 해상도용 추천 견적이 무엇인가요?", "QHD_spec"),
    ("4K 해상도 추천 견적서는 어떻게 되나요?", "4K_spec"),
    ("4K 해상도를 위한 최적의 컴퓨터 견적을 알려주세요.", "4K_spec"),
    ("3840x2160 해상도에서 사용하기 좋은 견적을 원해요.", "4K_spec")
    ]
additional_templates = [
    # 최소사양 관련 추가 질문
    ("이 게임을 플레이하려면 어떤 사양이 필요한가요?", "minimum_spec"),
    ("컴퓨터가 이 프로그램을 실행할 수 있을지 어떻게 알 수 있나요?", "minimum_spec"),
    ("게임을 실행하는 데 필요한 기본적인 하드웨어는 무엇인가요?", "minimum_spec"),
    ("이 프로그램을 가장 낮은 설정에서 실행하기 위해 필요한 것은?", "minimum_spec"),
    ("이 소프트웨어를 실행시키기 위한 최저 사양은?", "minimum_spec"),

    # 권장사양 관련 추가 질문
    ("이 프로그램을 최적으로 사용하기 위한 사양은?", "recommended_spec"),
    ("게임을 즐기기 위해 권장하는 하드웨어는 무엇인가요?", "recommended_spec"),
    ("이 게임을 풀옵션으로 즐기려면 어떤 사양이 필요한가요?", "recommended_spec"),
    ("프로그램 사용에 최적화된 컴퓨터 구성은 무엇인가요?", "recommended_spec"),
    ("이 게임의 권장 하드웨어 구성은 무엇인가요?", "recommended_spec"),

    # 해상도 및 견적 관련 추가 질문
    ("게임을 FHD 해상도에서 실행하기 위한 추천 PC는?", "FHD_spec"),
    ("FHD에서 최고의 성능을 내는 PC 구성은 어떻게 되나요?", "FHD_spec"),
    ("QHD 해상도에서 이 게임을 완벽하게 실행하려면?", "QHD_spec"),
    ("4K에서 이 프로그램을 부드럽게 실행하기 위해 추천하는 견적은?", "4K_spec"),
    ("최상의 그래픽으로 게임을 즐기기 위한 4K 견적서를 알려주세요.", "4K_spec")
]

# 추가된 질문 템플릿은 위에서 제공된 내용을 여기에 삽입

# 질문과 답변 쌍 생성 함수
def generate_extended_questions_answers(df, templates):
    qna_pairs = []
    for _, row in df.iterrows():
        program_name = row["program_name"]
        for question_template, column in templates:
            question = f"{program_name} {question_template}"
            answer = row[column]
            qna_pairs.append((question, answer))
    return qna_pairs

# 전체 질문-답변 쌍 생성
full_qna_data = generate_extended_questions_answers(df_large, extended_templates + additional_templates)

# 생성된 데이터를 DataFrame으로 변환 및 CSV 파일로 저장
df_full_qna = pd.DataFrame(full_qna_data, columns=['question', 'answer'])
full_finetuning_file_path = 'full_finetuning_dataset_for_koalpaca.csv'
df_full_qna.to_csv(full_finetuning_file_path, index=False, encoding='utf-8-sig')

# 완료 메시지 출력
print(f"Full dataset with {len(full_qna_data)} Q&A pairs has been saved to {full_finetuning_file_path}")
