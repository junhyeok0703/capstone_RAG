import json


def split_and_remove_estimates(file_path):

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    updated_data = []

    for item in data:
        quotation_description = item['quotations_quotations_description']


        if '1년 출장 A/S상세보기' in quotation_description:
            parts = quotation_description.split('1년 출장 A/S상세보기', 1)
            computer_estimate_data = parts[0] + '1년 출장 A/S상세보기'
            quote_description = parts[1] if len(parts) > 1 else ""
        else:

            parts = quotation_description.rsplit('상세보기', 1)
            computer_estimate_data = parts[0] + '상세보기'
            quote_description = parts[1] if len(parts) > 1 else ""


        del item['quotations_quotations_description']


        item['Computer_Estimate_Data'] = computer_estimate_data.strip()
        item['Quote Description'] = quote_description.strip()
        updated_data.append(item)


    with open('updated_1year_crawling_estimated_data.json', 'w', encoding='utf-8') as file:
        json.dump(updated_data, file, ensure_ascii=False, indent=4)


# 함수 호출
split_and_remove_estimates('../2/1year_crawling_estimated_data.json')
