
""" AWS Glue (database, crawler, catalogação)"""

import boto3
import time
from botocore.exceptions import ClientError
from config import (
    DATABASE_NAME,
    CRAWLER_NAME,
    BUCKET_NAME,
    AWS_REGION
)


class GlueHandler:
    """Classe para gerenciar operações no Glue"""

    def __init__(self):
        """Inicializa o cliente Glue"""
        self.glue_client = boto3.client('glue', region_name=AWS_REGION)
        print(f" Cliente Glue inicializado na região {AWS_REGION}")

    def criar_database(self):
        """
        Cria um database no Glue Catalog.
        Database é como um "schema" que agrupa suas tabelas.
        """
        try:
            self.glue_client.create_database(
                DatabaseInput={
                    'Name': DATABASE_NAME,
                    'Description': 'Database para análise de vendas'
                }
            )
            print(f" Database '{DATABASE_NAME}' criado com sucesso!")
            return True

        except ClientError as e:
            if e.response['Error']['Code'] == 'AlreadyExistsException':
                print(f"️  Database '{DATABASE_NAME}' já existe!")
                return True
            else:
                print(f" Erro ao criar database: {e}")
                return False

    def criar_crawler(self):

        try:

            s3_target_path = f's3://{BUCKET_NAME}/data/'

            self.glue_client.create_crawler(
                Name=CRAWLER_NAME,
                Role='arn:aws:iam::747103386091:role/AWSGlueServiceRole-vendas',
                #  trocar isso
                DatabaseName=DATABASE_NAME,
                Description='Crawler para catalogar dados de vendas',
                Targets={
                    'S3Targets': [
                        {
                            'Path': s3_target_path
                        }
                    ]
                }
            )
            print(f" Crawler '{CRAWLER_NAME}' criado com sucesso!")
            return True

        except ClientError as e:
            if e.response['Error']['Code'] == 'AlreadyExistsException':
                print(f"️  Crawler '{CRAWLER_NAME}' já existe!")
                return True
            else:
                print(f" Erro ao criar crawler: {e}")
                return False

    def executar_crawler(self):
        """
        Executa o Crawler para escanear os dados e criar a tabela.
        """
        try:
            print(f" Iniciando crawler '{CRAWLER_NAME}'...")
            self.glue_client.start_crawler(Name=CRAWLER_NAME)


            print(" Aguardando crawler finalizar (isso pode levar alguns minutos)...")

            while True:
                response = self.glue_client.get_crawler(Name=CRAWLER_NAME)
                status = response['Crawler']['State']

                if status == 'READY':
                    print(f" Crawler finalizado com sucesso!")

                    last_crawl = response['Crawler'].get('LastCrawl', {})
                    if last_crawl:
                        print(f" Status: {last_crawl.get('Status')}")
                    return True

                elif status in ['STOPPING', 'RUNNING']:
                    print(f"   Status: {status}... aguardando...")
                    time.sleep(10)

                else:
                    print(f" Crawler parou com status: {status}")
                    return False

        except ClientError as e:
            if e.response['Error']['Code'] == 'CrawlerRunningException':
                print(f"️  Crawler já está executando!")
                return True
            else:
                print(f" Erro ao executar crawler: {e}")
                return False

    def listar_tabelas(self):
        """Lista todas as tabelas no database"""
        try:
            response = self.glue_client.get_tables(DatabaseName=DATABASE_NAME)

            if response['TableList']:
                print(f"\n Tabelas no database '{DATABASE_NAME}':")
                for table in response['TableList']:
                    print(f"   - {table['Name']}")
                    print(f"     Localização: {table['StorageDescriptor']['Location']}")
                    print(f"     Colunas: {len(table['StorageDescriptor']['Columns'])}")
            else:
                print(f"  Nenhuma tabela encontrada no database '{DATABASE_NAME}'")

        except ClientError as e:
            print(f" Erro ao listar tabelas: {e}")


if __name__ == "__main__":
    handler = GlueHandler()
    handler.criar_database()
    handler.listar_tabelas()