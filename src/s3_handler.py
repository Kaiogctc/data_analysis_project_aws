""" acessar o s3 bucket"""

import boto3
from botocore.exceptions import ClientError
from config import BUCKET_NAME, AWS_REGION


class S3Handler:
    """Classe para gerenciar operações no S3"""

    def __init__(self):
        """Inicializa o cliente S3"""
        self.s3_client = boto3.client('s3', region_name=AWS_REGION)
        print(f" Cliente S3 inicializado na região {AWS_REGION}")

    def criar_bucket(self):
        """
        Cria o bucket no S3 se ele não existir
        """
        try:
            # Verifica se o bucket já existe
            self.s3_client.head_bucket(Bucket=BUCKET_NAME)
            print(f"️  Bucket '{BUCKET_NAME}' já existe!")
            return True

        except ClientError as e:
            error_code = e.response['Error']['Code']

            if error_code == '404':
                # O bucket não existe, criar 
                try:
                    # Na região us-east-1 não precisa especificar LocationConstraint
                    if AWS_REGION == 'us-east-1':
                        self.s3_client.create_bucket(Bucket=BUCKET_NAME)
                    else:
                        self.s3_client.create_bucket(
                            Bucket=BUCKET_NAME,
                            CreateBucketConfiguration={'LocationConstraint': AWS_REGION}
                        )

                    print(f" Bucket '{BUCKET_NAME}' criado com sucesso!")
                    return True

                except ClientError as create_error:
                    print(f" Erro ao criar bucket: {create_error}")
                    return False
            else:
                print(f" Erro ao verificar bucket: {e}")
                return False

    def upload_arquivo(self, arquivo_local, caminho_s3):
        """
         upload de um arquivo para o S3.

        Args:
            arquivo_local: caminho do arquivo no meu computador
            caminho_s3: onde o arquivo vai ficar no S3
        """
        try:
            print(f" Fazendo upload de '{arquivo_local}' para s3://{BUCKET_NAME}/{caminho_s3}")

            self.s3_client.upload_file(
                Filename=arquivo_local,
                Bucket=BUCKET_NAME,
                Key=caminho_s3
            )

            print(f" Upload concluído com sucesso!")
            return True

        except FileNotFoundError:
            print(f" Erro: Arquivo '{arquivo_local}' não encontrado!")
            return False

        except ClientError as e:
            print(f" Erro ao fazer upload: {e}")
            return False

    def listar_arquivos(self):
        """Lista todos os arquivos no bucket"""
        try:
            response = self.s3_client.list_objects_v2(Bucket=BUCKET_NAME)

            if 'Contents' in response:
                print(f"\n Arquivos no bucket '{BUCKET_NAME}':")
                for obj in response['Contents']:
                    print(f"   - {obj['Key']} ({obj['Size']} bytes)")
            else:
                print(f"️  Bucket '{BUCKET_NAME}' está vazio")

        except ClientError as e:
            print(f" Erro ao listar arquivos: {e}")



if __name__ == "__main__":
    handler = S3Handler()
    handler.criar_bucket()
    handler.listar_arquivos()