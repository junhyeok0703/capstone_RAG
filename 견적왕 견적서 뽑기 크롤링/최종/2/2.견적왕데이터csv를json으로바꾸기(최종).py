import csv
import json

def csv_to_json(csv_file_path, json_file_path):

    with open(csv_file_path, mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        data = []

        for row in csv_reader:
            data.append(row)

    with open(json_file_path, mode='w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


csv_file_path = '../1/crawling_estimated_data.csv'
json_file_path = '1year_crawling_estimated_data.json'

csv_to_json(csv_file_path, json_file_path)
