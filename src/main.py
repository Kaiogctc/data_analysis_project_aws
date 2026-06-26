
"""Arquivo principal que orquestra todo o pipeline de dados"""


from s3_handler import S3Handler
from glue_handler import GlueHandler
from athena_handler import AthenaHandler
from config import LOCAL_DATA_PATH, S3_DATA_PATH


def linha_separadora():
    
    print("\n" + "=" * 80 + "\n")


def main():
    """Função principal que executa todo o pipeline"""

    print(" INICIANDO PIPELINE DE ANÁLISE DE DADOS AWS")
   
    print("Etapas:")
    print("1. Vai criear bucket e fazer upload do CSV para S3")
    print("2. Criar database e crawler no Glue")
    print("3. Executa crawler para catalogar os dados")
    print("4. Executar consultas SQL no Athena")
    print("=" * 80)

    input("\nPressione ENTER para começar...")

    linha_separadora()
    print(" CONFIGURANDO S3")
    linha_separadora()

    s3 = S3Handler()

    # Cria o bucket
    if not s3.criar_bucket():
        print(" Erro ao criar bucket. Abortando...")
        return

    # Faz upload do arquivo
    if not s3.upload_arquivo(LOCAL_DATA_PATH, S3_DATA_PATH):
        print(" Erro ao fazer upload. Abortando...")
        return

    # Listari arquivos para confirmar
    s3.listar_arquivos()

    input("\n Etapa 1 concluída! Pressione ENTER para continuar...")

    linha_separadora()
    print(" ETAPA 2: CONFIGURANDO GLUE")
    linha_separadora()

    glue = GlueHandler()

    # Cria o database
    if not glue.criar_database():
        print(" Erro ao criar database. Abortando...")
        return

    # Cria o crawler
    if not glue.criar_crawler():
        print("  Atenção: Verifique a Role do Glue no código!")
        print("  Você precisa criar uma Role no IAM para o Glue.")
        print("   Veja as instruções abaixo")
        input("\nPressione ENTER para tentar continuar mesmo assim...")

    input("\nconcluído! Pressione ENTER para continuar...")

    
    linha_separadora()
    print(" EXECUTANDO CRAWLER")
    linha_separadora()

    if not glue.executar_crawler():
        print(" Erro ao executar crawler. Verifique as configurações.")
        print(" Verificasr se a Role do Glue está correta ")
        return

    # Lista tabelas criadas
    glue.listar_tabelas()

    input("\nPressione ENTER para continuar...")

    linha_separadora()
    print("EXECUTANDO CONSULTAS SQL")
    linha_separadora()

    athena = AthenaHandler()

    # Menu de consultas
    while True:
        print("\n MENU DE CONSULTAS:")
        print("1. Ver todas as vendas")
        print("2. Vendas por produto (agregado)")
        print("3. Vendas por região (agregado)")
        print("4. Top 5 clientes")
        print("5. Consulta personalizada")
        print("0. Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            athena.query_todas_vendas()

        elif opcao == "2":
            athena.query_vendas_por_produto()

        elif opcao == "3":
            athena.query_vendas_por_regiao()

        elif opcao == "4":
            athena.query_top_clientes()

        elif opcao == "5":
            print("\n A tabela se chama 'sales' no database 'sales_db'")
            query_custom = input("Digite sua query SQL: \n")
            athena.executar_query(query_custom)

        elif opcao == "0":
            break

        else:
            print(" Opção inválida!")

        input("\n Pressione ENTER para voltar ao menu...")

    
    linha_separadora()
    print(" PIPELINE CONCLUÍDO ")
    linha_separadora()
    print(" Dados carregados no S3")
    print(" Tabela catalogada no Glue")
    print(" Consultas executadas no Athena")
    print("\n É possivel acessar o console AWS para ver:")
    print("   - Bucket S3: https://s3.console.aws.amazon.com/")
    print("   - Glue Catalog: https://console.aws.amazon.com/glue/")
    print("   - Athena Query Editor: https://console.aws.amazon.com/athena/")
    linha_separadora()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Execução interrompida pelo usuário")
    except Exception as e:
        print(f"\n\n Erro inesperado: {e}")
        import traceback

        traceback.print_exc()