"""Configurações do projeto AWS"""


AWS_REGION = 'us-east-1'
BUCKET_NAME = 'vendas-python-Kaio-2025'
DATABASE_NAME = 'sales_db'
TABLE_NAME = 'sales'
CRAWLER_NAME = 'sales-crawler'


LOCAL_DATA_PATH = 'data/sales.csv'
S3_DATA_PATH = 'data/sales.csv'

# Configurações Athena
ATHENA_OUTPUT_BUCKET = f's3://{BUCKET_NAME}/athena-results/'