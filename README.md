# data_analysis_project_aws
📋 Índice

Sobre o Projeto luciano

Arquitetura

Tecnologias Utilizadas

Pré-requisitos

Instalação

Configuração AWS

Estrutura do Projeto

Como Usar

Funcionalidades

Queries Disponíveis

Custos Estimados

Melhorias Futuras

Aprendizados

Licença

Contato



Sobre o Projeto

Este projeto implementa um pipeline completo de análise de dados utilizando serviços da AWS. O objetivo é demonstrar como automatizar o processo de ingestão, catalogação e análise de dados usando infraestrutura cloud.

O que o projeto faz:

📦 Armazena dados (CSV) no Amazon S3

🔍 Cataloga automaticamente os dados usando AWS Glue Crawler

💻 Consulta os dados usando SQL via Amazon Athena

🧹 Gerencia recursos cloud com scripts de automação

Caso de Uso:
Análise de dados de vendas com queries SQL para obter insights sobre:

Vendas por produto
Desempenho por região
Top clientes
Métricas de receita


🏗️ Arquitetura



🛠️ Tecnologias Utilizadas
Serviços AWS:

Amazon S3: Armazenamento de objetos (data lake)

AWS Glue: Serviço de ETL e catalogação de dados

AWS Glue Crawler: Descoberta automática de schema

Amazon Athena: Query engine serverless (SQL)

AWS IAM: Gerenciamento de identidade e acesso

Ferramentas e Linguagens:

Python 3.9+: Linguagem principal

boto3: AWS SDK para Python

PyCharm: IDE de desenvolvimento

AWS CLI: Interface de linha de comando

✅ Pré-requisitos
Antes de começar, você precisa ter instalado:

Python 3.9 ou superior
pip (gerenciador de pacotes Python)
Conta AWS (Free Tier é suficiente)
AWS CLI configurado

📥 Instalação
 
Clone o repositório:
bashgit clone https://github.com/seu-usuario/aws-data-analysis-pipeline.git
cd aws-data-analysis-pipeline
 
Instale as dependências:
bashpip install -r requirements.txt

Verifique a estrutura:
bashtree

Deve aparecer:
data_analysis_project_aws/

├── data/
│   
└── sales.csv

├── queries/

├── src/

│   ├── __init__.py

│   ├── config.py

│   ├── s3_handler.py

│   ├── glue_handler.py

│   ├── athena_handler.py

│   ├── main.py

├── requirements.txt

└── README.md

⚙️ Configuração AWS
Criar usuário IAM:

Acesse o Console AWS → IAM

Crie um novo usuário: aws-data-pipeline-user

Anexe as seguintes policies:

AmazonS3FullAccess

AWSGlueConsoleFullAccess

AmazonAthenaFullAccess

Configurar AWS CLI:

bash:
 aws configure

Insira:

AWS Access Key ID

AWS Secret Access Key

Default region: us-east-1

Default output format: json


Criar IAM Role para Glue:

Console AWS → IAM → Roles → Create Role

Trusted entity: AWS service

Use case: Glue

Attach policies:

AWSGlueServiceRole

AmazonS3FullAccess


Nome da Role: AWSGlueServiceRole-vendas

Copie a ARN da Role

 Configurar a ARN no código:

Abra src/glue_handler.py e na linha 41, cole sua ARN:

pythonRole='arn:aws:iam::SEU_ACCOUNT_ID:role/AWSGlueServiceRole-vendas',

Ajustar configurações:

Edite src/config.py:

BUCKET_NAME = 'seu-bucket-unico-123'  # Nome único globalmente
AWS_REGION = 'us-east-1'               # Sua região preferida
DATABASE_NAME = 'sales_db'             # Nome do database

 Estrutura do Projeto
 
src/
│

├── config.py             # Configurações centralizadas

├── s3_handler.py         # Gerenciamento do S3

├── glue_handler.py       # Gerenciamento do Glue

├── athena_handler.py     # Execução de queries SQL

├── main.py               # Orquestrador principal


Módulos:

*config.py

Centraliza todas as configurações do projeto (nomes de recursos, região, paths).

*s3_handler.py

*Classe responsável por:

Criar buckets no S3

Fazer upload de arquivos

Listar objetos no bucket

*glue_handler.py

Classe responsável por:

Criar database no Glue Catalog

Criar e configurar Crawlers

Executar Crawlers para catalogação

Listar tabelas catalogadas

*athena_handler.py

*Classe responsável por:

Executar queries SQL

Formatar resultados

Queries pré-definidas (vendas por produto, região, etc.)

*main.py

Orquestra todo o pipeline:

Upload de dados para S3

Catalogação com Glue

Menu interativo de consultas SQL



🚀 Como Usar

Execução Completa do Pipeline:

cd src

python main.py


🎯 Funcionalidades

✅ Automação Completa

Setup automatizado de recursos AWS

Catalogação automática de schema


✅ Gerenciamento de Dados

Upload de arquivos CSV para S3

Versionamento de dados

Organização em data lake

✅ Análise SQL

Queries interativas via Athena

Agregações e métricas

Consultas personalizadas

✅ Tratamento de Erros

Validação de recursos existentes

Mensagens de erro descritivas

Rollback em caso de falhas

✅ Otimização de Custos


Uso eficiente de recursos

Monitoramento de execuções


📊 Queries Disponíveis
1. Ver todas as vendas
2. Vendas por produto (Agregado)
3. Vendas por região
4. Top 5 clientes
5. Consulta personalizada digite qualquer query SQL válida!

💰 Custos Estimados
Free Tier (primeiros 12 meses):

S3: 5 GB grátis
Athena: 10 GB escaneados/mês grátis (primeiros 30 dias em algumas regiões)
IAM: Sempre grátis

Custos Reais (após Free Tier):
ServiçoPreçoEste ProjetoS3 
StorageUS$ 0.023/GB~US$ 0.00 (< 1 MB)

Glue CrawlerUS$ 0.44/DPU-Hour~US$ 0.07/execução

AthenaUS$ 5.00/TB escaneado~US$ 0.00 (< 1 MB)TOTAL-~US$ 0.20

Dicas para Minimizar Custos:

✅ Delete recursos após usar 

✅ Use região us-east-1 (mais barata)

✅ Configure Billing Alarms

✅ Não deixe Crawlers rodando continuamente

📚 Aprendizados
Este projeto me permitiu aprender e aplicar:
Conceitos de Cloud:

✅ Arquitetura de data lake

✅ Serviços serverless (Athena, Glue)

✅ Gerenciamento de IAM e permissões

✅ Otimização de custos

Programação:

✅ Python orientado a objetos

✅ Integração com APIs AWS (boto3)

✅ Tratamento de erros e exceções

✅ Automação de infraestrutura

Engenharia de Dados:

✅ Pipeline ETL (Extract, Transform, Load)

✅ Catalogação de metadados

✅ Queries SQL analíticas

✅ Modelagem de dados

📄 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

📬 Contatos Kaio

LinkedIn: https://www.linkedin.com/in/kaio-correa/

GitHub: https://github.com/Kaiogctc

Email: kaiocorrea34@gmail.com


🙏 Agradecimentos

AWS Free Tier pela infraestrutura
Comunidade Python pelo boto3
Documentação oficial da AWS


Desenvolvido com ❤️ e ☕ por Kaio