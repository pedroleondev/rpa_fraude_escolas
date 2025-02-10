import os
import logging
import psycopg2
from dotenv import load_dotenv
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd

# Configurar logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Carregar variãveis de ambiente
load_dotenv()

# Configurações banco de dados
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}
url = "https://www.tce.sp.gov.br/jurisprudencia/pesquisar?txtTdPalvs=fraude+em+prefeitura&processo=&acao=Executa&buscaRapida=true&ignorarEntrada=false"

def raspar_info(url):

    """
    🟢🟡🔴
    ✅Faz a raspagem dos dados de uma única página da URL fornecida.
    Retorna uma lista com os resultados encontrados.

    🔵 Falta realizar a configuração para popular o BD;
    


    🟢🟡🔴

    """

    # Declarar Headers
    session = HTMLSession()
    session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'
    session.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    session.headers['Accept-Language'] = 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
    session.headers['Connection'] = 'keep-alive'
    session.headers['Upgrade-Insecure-Requests'] = '1'

    response=session.get(url)
    print(response.status_code)

    if response.status_code != 200:

        print(f"Erro ao acessar {url}, Status Code: {response.status_code}")
        return []
    
    # Encontrar todas as linhas da tabela (cada <tr>)
    linhas = response.html.xpath('//tbody/tr[contains(@class, "borda-superior")]')

    # Lista para armazenar os resultados
    resultados = []

    # Processar cada linha
    for linha in linhas:
        colunas = linha.xpath('.//td')  # Captura todas as colunas da linha

        # Garantir que há colunas suficientes antes de tentar acessar os índices
        if len(colunas) < 8:
            continue

        elemento_doc = colunas[0].xpath('.//a')

        if elemento_doc:
            # Capturar os elementos dentro das colunas
            elemento_doc = colunas[0].xpath('.//a')[0]  # Primeiro <a> dentro da 1ª coluna
            nome_doc = elemento_doc.text.strip()  # Nome do documento
            link_doc = elemento_doc.attrs.get('href', '').strip()  # Link do PDF
        else:
            nome_doc = "N/A"
            link_doc = "N/A"


        # Caputurar cada elemento da coluna (N° Proc. | Autuação	| Parte 1 | Parte 2 | Matéria | | Objeto | 	Exercício)

        num_processo = colunas[1].text.strip()
        data_autuacao = colunas[2].text.strip()
        parte_1 = colunas[3].text.strip()
        parte_2 = colunas[4].text.strip()
        materia = colunas[5].text.strip()
        objeto = colunas[6].text.strip()
        ano = colunas[7].text.strip()

        # Adicionar ao resultado
        resultados.append({
            "Nome_Documento": nome_doc,
            "Link_Documento": link_doc,
            "Numero_Processo": num_processo,
            "Data_Autuacao": data_autuacao,
            "Parte_1": parte_1,
            "Parte_2": parte_2,
            "Materia": materia,
            "Objeto": objeto,
            "Ano": ano
        })

    # Exibir os resultados
    for resultado in resultados:
        print(resultado)



raspar_info(url)