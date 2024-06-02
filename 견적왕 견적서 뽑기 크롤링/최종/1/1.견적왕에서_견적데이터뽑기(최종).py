import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool, current_process
import pandas as pd
from datetime import datetime


def crawl_es_sn(es_sn):
    print(f"Process {current_process().name} is crawling es_sn: {es_sn}")
    start_time = datetime.now()

    classes_to_crawl = ['cpu_vga', 'box summary', 'box greeting', 'box product', 'box reason', 'box office']
    url = f"https://kjwwang.com/shop/pc_estimate.html?action=view&es_sn={es_sn}"
    row = {'es_sn': es_sn}
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            subject_content = soup.find('h1', class_='subject')
            row['subject'] = subject_content.get_text(strip=True) if subject_content else ''

            date_content = soup.find('span', class_='date')
            row['date'] = date_content.get_text(strip=True) if date_content else ''

            for class_name in classes_to_crawl:
                content = soup.find(class_=class_name)
                row[class_name] = content.get_text(strip=True) if content else ''
    except Exception as e:
        print(f"Error while processing es_sn={es_sn}: {e}")

    end_time = datetime.now()
    print(f"es_sn: {es_sn} - Crawling completed in {end_time - start_time}")
    return row



def multiprocess_crawling(start, end, num_processes):
    with Pool(processes=num_processes) as pool:
        results = pool.map(crawl_es_sn, range(start, end + 1))
    return results



if __name__ == '__main__':
    # 멀티프로세싱을 이용하여 크롤링
    start_es_sn = 1200
    end_es_sn = 1210
    num_processes = 5  # 시스템에 맞게 프로세스 개수를 설정할 수 있습니다.
    print(f"Starting crawling from es_sn {start_es_sn} to {end_es_sn} using {num_processes} processes.")

    start_time = datetime.now()
    sorted_results = multiprocess_crawling(start_es_sn, end_es_sn, num_processes)
    end_time = datetime.now()


    df = pd.DataFrame(sorted_results)
    csv_file_path = 'crawling_estimated_data.csv'
    df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')

    print(f"Crawling completed in {end_time - start_time}")
    print(f"Saved crawling results to {csv_file_path}")
