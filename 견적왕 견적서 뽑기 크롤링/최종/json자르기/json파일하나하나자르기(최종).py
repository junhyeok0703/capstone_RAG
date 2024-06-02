import os
import json

directory = 'Estimated_json_data'
if not os.path.exists(directory):
    os.makedirs(directory)

with open('processed_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    quote_number = item['quote_number']


    filename = os.path.join(directory, f'{quote_number}.json')
    with open(filename, 'w', encoding='utf-8') as f:

        json.dump(item, f, ensure_ascii=False, indent=4)
