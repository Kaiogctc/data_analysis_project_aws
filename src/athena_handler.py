"""consultas SQL no Amazon Athena."""

import boto3
import time
from botocore.exceptions import ClientError
from config import DATABASE_NAME, ATHENA_OUTPUT_BUCKET, AWS_REGION


class AthenaHandler:
    """Classe para executar consultas SQL no Athena"""

    def __init__(self):
        """Inicializa o cliente Athena"""
        self.athena_client = boto3.client('athena', region_name=AWS_REGION)
        print(f" Cliente Athena inicializado na região {AWS_REGION}")

    def executar_query(self, query_sql):
        """
        Executa uma query SQL no Athena.

        Args:
            query_sql: A consulta SQL que você quer executar

        Returns:
            Lista de resultados ou None se houver erro
        """
        try:
            print(f"\n Executando query:")
            print(f"   {query_sql}")
            print()


            response = self.athena_client.start_query_execution(
                QueryString=query_sql,
                QueryExecutionContext={
                    'Database': DATABASE_NAME
                },
                ResultConfiguration={
                    'OutputLocation': ATHENA_OUTPUT_BUCKET
                }
            )

            query_execution_id = response['QueryExecutionId']
            print(f" Query iniciada (ID: {query_execution_id})")


            print(" Aguardando execução...")

            while True:
                result = self.athena_client.get_query_execution(
                    QueryExecutionId=query_execution_id
                )

                status = result['QueryExecution']['Status']['State']

                if status == 'SUCCEEDED':
                    print(" Query executada com sucesso!\n")
                    break

                elif status in ['RUNNING', 'QUEUED']:
                    time.sleep(2)

                elif status == 'FAILED':
                    reason = result['QueryExecution']['Status']['StateChangeReason']
                    print(f" Query falhou: {reason}")
                    return None

                else:
                    print(f" Status inesperado: {status}")
                    return None


            results = self.athena_client.get_query_results(
                QueryExecutionId=query_execution_id
            )

            return self._formatar_resultados(results)

        except ClientError as e:
            print(f" Erro ao executar query: {e}")
            return None

    def _formatar_resultados(self, results):
        """
        Formata os resultados da query de forma legível.

        Args:
            results: Resultados brutos do Athena

        Returns:
            Lista de dicionários com os resultados
        """
        rows = results['ResultSet']['Rows']

        if not rows:
            print("️  Nenhum resultado encontrado")
            return []


        headers = [col['VarCharValue'] for col in rows[0]['Data']]


        data = []
        for row in rows[1:]:
            values = [col.get('VarCharValue', 'NULL') for col in row['Data']]
            data.append(dict(zip(headers, values)))


        print(" RESULTADOS:")



        header_line = " | ".join(f"{h:<20}" for h in headers)
        print(header_line)



        for row_dict in data:
            row_line = " | ".join(f"{str(v):<20}" for v in row_dict.values())
            print(row_line)

        print("=" * 80)
        print(f"Total de linhas: {len(data)}\n")

        return data

    def query_todas_vendas(self):
        """Consulta simples: retorna todas as vendas"""
        query = """
        SELECT * 
        FROM data
        LIMIT 10
        """
        return self.executar_query(query)

    def query_vendas_por_produto(self):
        """Agrupa vendas por produto"""
        query = """
        SELECT 
            product,
            COUNT(*) as total_vendas,
            SUM(quantity) as quantidade_total,
            ROUND(SUM(price * quantity), 2) as receita_total
        FROM data
        GROUP BY product
        ORDER BY receita_total DESC
        """
        return self.executar_query(query)

    def query_vendas_por_regiao(self):
        """Agrupa vendas por região"""
        query = """
        SELECT 
            region,
            COUNT(*) as total_vendas,
            ROUND(AVG(price * quantity), 2) as ticket_medio,
            ROUND(SUM(price * quantity), 2) as receita_total
        FROM data
        GROUP BY region
        ORDER BY receita_total DESC
        """
        return self.executar_query(query)

    def query_top_clientes(self):
        """Top clientes por receita"""
        query = """
        SELECT 
            customer,
            COUNT(*) as num_compras,
            ROUND(SUM(price * quantity), 2) as total_gasto
        FROM data
        GROUP BY customer
        ORDER BY total_gasto DESC
        LIMIT 5
        """
        return self.executar_query(query)



if __name__ == "__main__":
    handler = AthenaHandler()


    handler.query_todas_vendas()