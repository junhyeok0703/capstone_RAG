import pandas as pd


xlsx_path = '4월 견적 (2024).xlsx'
df_xlsx = pd.read_excel(xlsx_path)


csv_path = 'crawling_견적(견적서 23년10월부터 24년 4월 11일까지).csv'
df_csv = pd.read_csv(csv_path)

df_xlsx_head = df_xlsx.head()
df_csv_head = df_csv.head()

df_xlsx_head, df_csv_head