import requests
from bs4 import BeautifulSoup
import csv
import re
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def extract_gpu_details(url):
    try:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

        chrome_options = Options()
        chrome_options.add_argument(f'user-agent={user_agent}')  # Setting the User-Agent

        service = Service()
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)
        html_content = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html_content, 'html.parser')

        product_name_tag = soup.find("h1", class_="gpudb-name")
        if not product_name_tag:
            print(f"Product name error {url}")
            return None, None, None, None

        product_name = product_name_tag.text.strip()

        main_specs_div = soup.find("dl", class_="gpudb-specs-large")
        main_specs = "\n".join([f"{spec.find('dt').text.strip()}: {spec.find('dd').text.strip()}" for spec in
                                main_specs_div.find_all("div", class_="gpudb-specs-large__entry")])

        additional_specs = ""
        additional_specs_sections = soup.find_all("section", class_="details")
        for section in additional_specs_sections:
            section_title = section.find("h2").text.strip()
            specs = []
            for spec in section.find_all("dl", class_="clearfix"):
                dt_text = spec.find("dt").text.strip()
                dd_text = ' '.join(spec.find("dd").stripped_strings)
                dd_text = re.sub(r'\s+', ' ', dd_text)
                specs.append(f"{dt_text}: {dd_text}")
            if specs:
                additional_specs += f"{section_title}:\n" + "\n".join(specs) + "\n\n"

        retail_boards_section = soup.find("section", class_="details customboards")
        if retail_boards_section is not None:
            retail_boards_rows = retail_boards_section.find("tbody").find_all("tr")
            retail_boards_data = ""
            for row in retail_boards_rows:
                cols = row.find_all("td")
                if len(cols) != 5:
                    print("형식이 다름")
                    break
                board_name = cols[0].text.strip()
                gpu_clock = cols[1].text.strip()
                boost_clock = cols[2].text.strip()
                memory_clock = cols[3].text.strip()
                other_changes = cols[4].text.strip()
                retail_boards_data += f"기반 제품명:{board_name} -해당 제품의 바뀐 사항 GPU Clock: {gpu_clock}, Boost Clock: {boost_clock}, Memory Clock: {memory_clock}, 외의 바뀐 사항: {other_changes}\n"
        else:
            retail_boards_data = "없음"
        return product_name, main_specs, additional_specs, retail_boards_data
    except Exception as e:
        print(f"Error fetching details for URL {url}: {e}")
        return None, None, None, None

def extract_gpu_urls(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    table = soup.find('table', class_='processors')
    product_urls = {}

    for tr in table.find_all('tr'):
        td = tr.find('td', class_='vendor-AMD')
        if td:
            a_tag = td.find('a')
            if a_tag:
                product_name = a_tag.text.strip()
                product_url = 'https://www.techpowerup.com' + a_tag['href']
                product_urls[product_name] = product_url

    return product_urls

html_content = """
<table class="processors">
				<thead>
			<tr>
				<th colspan="8" class="mfgr" id="Intel">Intel</th>
			</tr>
		</thead>
		<thead class="colheader">
	<tr>
		<th>Product Name</th>
		<th>GPU Chip</th>
		<th>Released</th>
		<th>Bus</th>
		<th>Memory</th>
		<th>GPU clock</th>
		<th>Memory clock</th>
		<th>Shaders / TMUs / ROPs</th>
	</tr>
</thead>

										<tbody><tr>
	<td class="vendor-Intel">
		<a href="/gpu-specs/h3c-xg310.c3745">H3C XG310</a>

			</td>
	<td>
		<a href="/gpu-specs/intel-dg1.g986">DG1</a>

			</td>
	<td>Nov 11th, 2020</td>
	<td>PCIe 3.0 x16</td>
	<td>8 GB, LPDDR4X, 128 bit</td>
	<td>1050 MHz</td>
	<td>2133 MHz</td>
	<td>768 / 48 / 24</td>
</tr>
								<tr>
	<td class="vendor-Intel">
		<a href="/gpu-specs/iris-plus-graphics-g7-64eu-mobile.c3444">Iris Plus Graphics G7 64EU Mobile</a>
			</td>
	<td>
		<a href="/gpu-specs/intel-ice-lake-gt2.g894">Ice Lake GT2</a>

			</td>
	<td>May 4th, 2020</td>
	<td>Ring Bus</td>
	<td>System Shared</td>
	<td>300 MHz</td>
	<td>System Shared</td>
	<td>512 / 32 / 8</td>
</tr>
								<tr>
	<td class="vendor-Intel">
		<a href="/gpu-specs/iris-xe-graphics-g4-48eu-mobile.c3679">Iris Xe Graphics G4 48EU Mobile</a>
			</td>
	<td>
		<a href="/gpu-specs/intel-tiger-lake-gt2.g906">Tiger Lake GT2</a>

			</td>
	<td>Sep 2nd, 2020</td>
	<td>Ring Bus</td>
	<td>System Shared</td>
	<td>300 MHz</td>
	<td>System Shared</td>
	<td>384 / 24 / 12</td>
</tr>
								<tr>
	<td class="vendor-Intel">
		<a href="/gpu-specs/iris-xe-graphics-g7-80eu-mobile.c3678">Iris Xe Graphics G7 80EU Mobile</a>
			</td>
	<td>
		<a href="/gpu-specs/intel-tiger-lake-gt2.g906">Tiger Lake GT2</a>

			</td>
	<td>Sep 2nd, 2020</td>
	<td>Ring Bus</td>
	<td>System Shared</td>
	<td>300 MHz</td>
	<td>System Shared</td>
	<td>640 / 40 / 20</td>
</tr>
								<tr>
	<td class="vendor-Intel">
		<a href="/gpu-specs/iris-xe-graphics-g7-96eu-mobile.c3677">Iris Xe Graphics G7 96EU Mobile</a>
			</td>
	<td>
		<a href="/gpu-specs/intel-tiger-lake-gt2.g906">Tiger Lake GT2</a>

			</td>
	<td>Sep 2nd, 2020</td>
	<td>Ring Bus</td>
	<td>System Shared</td>
	<td>300 MHz</td>
	<td>System Shared</td>
	<td>768 / 48 / 24</td>
</tr>
								<tr>
	<td class="vendor-Intel">
		<a href="/gpu-specs/iris-xe-max-graphics.c3737">Iris Xe MAX Graphics</a>

			</td>
	<td>
		<a href="/gpu-specs/intel-dg1.g986">DG1</a>

			</td>
	<td>Oct 31st, 2020</td>
	<td>PCIe 4.0 x8</td>
	<td>4 GB, LPDDR4X, 128 bit</td>
	<td>300 MHz</td>
	<td>2133 MHz</td>
	<td>768 / 48 / 24</td>
</tr>
								<tr>
	<td class="vendor-Intel">
		<a href="/gpu-specs/uhd-graphics-16eu-mobile.c4090">UHD Graphics 16EU Mobile</a>
			</td>
	<td>
		<a href="/gpu-specs/intel-elkhart-lake-gt1.g910">Elkhart Lake GT1</a>

			</td>
	<td>Sep 23rd, 2020</td>
	<td>Ring Bus</td>
	<td>System Shared</td>
	<td>250 MHz</td>
	<td>System Shared</td>
	<td>128 / 8 / 4</td>
</tr>
								<tr>
	<td class="vendor-Intel">
		<a href="/gpu-specs/uhd-graphics-32eu-mobile.c4114">UHD Graphics 32EU Mobile</a>
			</td>
	<td>
		<a href="/gpu-specs/intel-elkhart-lake-gt1.g910">Elkhart Lake GT1</a>

			</td>
	<td>Sep 23rd, 2020</td>
	<td>Ring Bus</td>
	<td>System Shared</td>
	<td>400 MHz</td>
	<td>System Shared</td>
	<td>256 / 16 / 8</td>
</tr>
								<tr>
	<td class="vendor-Intel">
		<a href="/gpu-specs/uhd-graphics-610.c3602">UHD Graphics 610</a>
			</td>
	<td>
		<a href="/gpu-specs/intel-comet-lake-gt1.g950">Comet Lake GT1</a>

			</td>
	<td>Apr 30th, 2020</td>
	<td>Ring Bus</td>
	<td>System Shared</td>
	<td>350 MHz</td>
	<td>System Shared</td>
	<td>96 / 12 / 2</td>
</tr>
								<tr>
	<td class="vendor-Intel">
		<a href="/gpu-specs/uhd-graphics-630.c3600">UHD Graphics 630</a>
			</td>
	<td>
		<a href="/gpu-specs/intel-comet-lake-gt2.g925">Comet Lake GT2</a>

			</td>
	<td>Apr 30th, 2020</td>
	<td>Ring Bus</td>
	<td>System Shared</td>
	<td>350 MHz</td>
	<td>System Shared</td>
	<td>192 / 24 / 3</td>
</tr>
								<tr>
	<td class="vendor-Intel">
		<a href="/gpu-specs/uhd-graphics-630.c3601">UHD Graphics 630</a>
			</td>
	<td>
		<a href="/gpu-specs/intel-comet-lake-gt2.g925">Comet Lake GT2</a>

			</td>
	<td>Apr 30th, 2020</td>
	<td>Ring Bus</td>
	<td>System Shared</td>
	<td>350 MHz</td>
	<td>System Shared</td>
	<td>184 / 23 / 3</td>
</tr>
								<tr>
	<td class="vendor-Intel">
		<a href="/gpu-specs/uhd-graphics-g4-48eu-mobile.c3692">UHD Graphics G4 48EU Mobile</a>
			</td>
	<td>
		<a href="/gpu-specs/intel-lakefield-gt1.g897">Lakefield GT1</a>

			</td>
	<td>May 28th, 2020</td>
	<td>Ring Bus</td>
	<td>System Shared</td>
	<td>200 MHz</td>
	<td>System Shared</td>
	<td>384 / 32 / 8</td>
</tr>
								<tr>
	<td class="vendor-Intel">
		<a href="/gpu-specs/uhd-graphics-g7-64eu-mobile.c3691">UHD Graphics G7 64EU Mobile</a>
			</td>
	<td>
		<a href="/gpu-specs/intel-lakefield-gt2.g895">Lakefield GT2</a>

			</td>
	<td>May 28th, 2020</td>
	<td>Ring Bus</td>
	<td>System Shared</td>
	<td>200 MHz</td>
	<td>System Shared</td>
	<td>512 / 32 / 8</td>
</tr>
								<tr>
	<td class="vendor-Intel">
		<a href="/gpu-specs/uhd-graphics-p630.c3676">UHD Graphics P630</a>
			</td>
	<td>
		<a href="/gpu-specs/intel-comet-lake-gt2.g925">Comet Lake GT2</a>

			</td>
	<td>May 13th, 2020</td>
	<td>Ring Bus</td>
	<td>System Shared</td>
	<td>350 MHz</td>
	<td>System Shared</td>
	<td>192 / 24 / 3</td>
</tr>
								<tr>
	<td class="vendor-Intel">
		<a href="/gpu-specs/uhd-graphics-p630-mobile.c3730">UHD Graphics P630 Mobile</a>
			</td>
	<td>
		<a href="/gpu-specs/intel-comet-lake-gt2.g925">Comet Lake GT2</a>

			</td>
	<td>May 13th, 2020</td>
	<td>Ring Bus</td>
	<td>System Shared</td>
	<td>350 MHz</td>
	<td>System Shared</td>
	<td>192 / 24 / 3</td>
</tr>
								<tr>
	<td class="vendor-Intel">
		<a href="/gpu-specs/xe-dg1.c3718">Xe DG1</a>

			</td>
	<td>
		<a href="/gpu-specs/intel-dg1.g986">DG1</a>

			</td>
	<td>2020</td>
	<td>PCIe 4.0 x8</td>
	<td>4 GB, LPDDR4X, 128 bit</td>
	<td>900 MHz</td>
	<td>2133 MHz</td>
	<td>640 / 40 / 20</td>
</tr>
								<tr>
	<td class="vendor-Intel">
		<a href="/gpu-specs/xe-dg1-sdv.c3483">Xe DG1-SDV</a>

			</td>
	<td>
		<a href="/gpu-specs/intel-dg1.g986">DG1</a>

			</td>
	<td>Never Released</td>
	<td>PCIe 4.0 x8</td>
	<td>8 GB, LPDDR4X, 128 bit</td>
	<td>900 MHz</td>
	<td>2133 MHz</td>
	<td>768 / 48 / 24</td>
</tr>
		
			</tbody></table>
"""



csv_file_path = 'Intel_2020.csv'
product_urls = extract_gpu_urls(html_content)
with open(csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Product Name', 'Main Specs', 'Additional Specs', 'Derived Models'])

counter = 0
for name, url in product_urls.items():
    result = extract_gpu_details(url)
    if None in result:
        if result[0] is not None:
            print(f"Product Name: {result[0]}")
        continue
    product_name, main_specs, additional_specs, retail_boards_data = result
    with open(csv_file_path, 'a', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([product_name, main_specs, additional_specs, retail_boards_data])
    counter += 1
    print(product_name)
    print(counter)
    if counter % 10 == 0:
        sleep(40)  # Be mindful of the target website's resources

print(f'Data has been saved to {csv_file_path}')
