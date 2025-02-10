# Documentação do Robô de Automação de Processos (RPA) para Extração de Dados

## Introdução
Este projeto tem como objetivo desenvolver um robô de automação de processos (RPA) para extrair documentos do site do Tribunal de Contas do Estado de São Paulo (TCE-SP) relacionados a "fraude em escolas". Os dados extraídos serão armazenados em um banco de dados MySQL para posterior análise.

## Tecnologias Utilizadas
- **Linguagem:** Python
- **Bibliotecas de raspagem:** `requests-html`, `lxml`
- **Banco de dados:** MySQL
- **Gerenciamento de ambiente:** Docker e Docker Compose
- **Gerenciamento de dependências:** `pip` e `requirements.txt`
- **Variáveis de ambiente:** `dotenv`

## Estrutura do Projeto
```
/
├── database.py          # Gerenciamento do banco de dados
├── scraper.py           # Raspagem de dados do site do TCE-SP
├── main.py              # Orquestração do processo
├── requirements.txt     # Dependências do projeto
├── docker-compose.yml   # Configuração do ambiente Docker
├── Dockerfile           # Configuração do container Python
├── .env                 # Configuração do banco de dados
├── teste_main.py        # Testes unitários
```

## Instalação e Configuração

### Clonando o Repositório
```sh
git clone https://github.com/seu-repositorio.git
cd seu-repositorio
```

### Configuração do Ambiente
Antes de iniciar o projeto, configure as variáveis de ambiente no arquivo `.env`:
```ini
MYSQL_HOST=mysql
MYSQL_PORT=3306
MYSQL_DATABASE=fraudes_info_db
MYSQL_USER=admin
MYSQL_PASSWORD=admin
MYSQL_ROOT_PASSWORD=root
```

### Instalando Dependências
Se estiver rodando localmente:
```sh
pip install -r requirements.txt
```

Se estiver utilizando Docker:
```sh
docker-compose up --build
```

## Execução do Robô
### Execução Local
```sh
python main.py
```

### Execução com Docker
```sh
docker-compose up -d  # Inicia os containers em modo detach (em segundo plano)
```
O container ficará ativo, mas sem executar automaticamente o código.

### Executando o Código dentro do Container
Se precisar rodar o script manualmente dentro do container:
```sh
docker exec -it python_app /bin/sh  # Acessa o shell do container
python main.py  # Executa o código manualmente
```
Isso permite controle manual sobre quando rodar a extração de dados.

## Detalhamento dos Módulos

### `scraper.py` (Raspagem de Dados)
- Utiliza a biblioteca `requests-html` para navegar no site.
- Coleta informações como Documento, Processo, Data, Partes envolvidas, Matéria e URL do documento.
- Possui funções de raspagem paginada para coletar todos os registros.

### `database.py` (Banco de Dados)
- Configuração da conexão MySQL.
- Criação da tabela `fraudes` com índices otimizados.
- Inserção de dados evitando duplicatas.

### `main.py` (Orquestração)
- Garante que a tabela esteja criada.
- Realiza a raspagem completa.
- Insere os dados extraídos no banco.

### `teste_main.py` (Testes)
- Testa conexão com o banco de dados.
- Testa criação de tabelas.
- Testa a raspagem de dados.

## Critérios de Avaliação
- **Funcionalidade:** O robô deve extrair corretamente os dados.
- **Qualidade do código:** Deve seguir boas práticas do Python (PEP8).
- **Eficiência:** Uso adequado das bibliotecas de raspagem.
- **Resiliência:** O sistema deve lidar bem com falhas de conexão e mudanças no site.

## Considerações Finais
Este projeto serve como uma base para extração automatizada de informações de sites governamentais. Melhorias podem incluir:
- Uso de Selenium para interações mais complexas.
- API para consultas ao banco.
- Automatizar execução periódica via cron job.

Para sugestões ou melhorias, contribua com pull requests!

