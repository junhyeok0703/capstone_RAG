import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# 시작과 끝 es_sn 값 설정
start_es_sn = 1500
end_es_sn = 1520


classes_to_crawl = ['cpu_vga', 'compos_prd_table2', 'box summary', 'box greeting', 'box product', 'box reason',
                    'box office']
additional_classes = ['subject']
ids_to_crawl = ['table1']

rows = []


start_time = datetime.now()

for es_sn in range(start_es_sn, end_es_sn + 1):
    url = f"https://kjwwang.com/shop/pc_estimate.html?action=view&es_sn={es_sn}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            row = {'es_sn': es_sn}
            for class_name in classes_to_crawl:
                elements = soup.find_all(class_=class_name)
                texts = ' '.join([element.get_text(strip=True) for element in elements])
                row[class_name] = texts
            for class_name in additional_classes:
                elements = soup.find_all(class_=class_name)
                texts = ' '.join([element.get_text(strip=True) for element in elements])
                row[class_name] = texts


            table1 = soup.find(id='table1')
            if table1:
                tr_data = []
                for tr in table1.find_all('tr'):
                    cells = tr.find_all(['td', 'th'])
                    row_data = [cell.get_text(strip=True) for cell in cells]
                    tr_data.append(' | '.join(row_data))
                row['table1'] = ' // '.join(tr_data)

            rows.append(row)
    except Exception as e:
        print(f"Error while processing es_sn={es_sn}: {e}")


end_time = datetime.now()

elapsed_time = end_time - start_time


df = pd.DataFrame(rows)


csv_file_path = 'crawling_results.csv'
df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')

print(f"Saved crawling results to {csv_file_path}")
print(f"Total crawling time: {elapsed_time}")
