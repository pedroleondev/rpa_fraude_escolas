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
URL_PESQUISA = "https://www.tce.sp.gov.br/jurisprudencia/pesquisar?txtTdPalvs=fraude+em+prefeitura&processo=&acao=Executa&buscaRapida=true&ignorarEntrada=false"
URL_OFFSET = "https://www.tce.sp.gov.br/jurisprudencia/pesquisar?acao=Executa&offset={}"
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

        
        resultado = {
            "Nome_Documento": nome_doc,
            "Link_Documento": link_doc,
            "Numero_Processo": num_processo,
            "Data_Autuacao": data_autuacao,
            "Parte_1": parte_1,
            "Parte_2": parte_2,
            "Materia": materia,
            "Objeto": objeto,
            "Ano": ano
        }
        
        # Adicionar ao resultado
        resultados.append(resultado)

    # Exibir os resultados
    return resultados


def obter_total_paginas():
    # Declarar Headers
    session = HTMLSession()
    session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'
    session.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    session.headers['Accept-Language'] = 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
    session.headers['Connection'] = 'keep-alive'
    session.headers['Upgrade-Insecure-Requests'] = '1'

    response=session.get(URL_PESQUISA)
    

    try:
        #caputurar o botão de paginação, posição -1
        ultimo_link = response.html.xpath('//nav/ul[@class="pagination pagination-sm"]/li[last()]/a/@href')

        if not ultimo_link:
            return 1 # se não encontrar, assume que há apenas 1 página
        
        ultimo_offset = int(ultimo_link[0].split("offset=")[-1])
        print(ultimo_offset)

        # offset contato de 10 em 10

        total_paginas = (ultimo_offset // 10) + 1

        print(f"Total de páginas encontradas: {total_paginas}")
        return total_paginas

    except Exception as e:
        print(f"Erro ao obter total de páginas: {e}")
        return 1

def raspar_todas_as_paginas(url):
    
    #total_paginas = obter_total_paginas()
    total_paginas = 3
    dados_coletados = []

    for pagina in range(total_paginas):
        offset = pagina * 10 # aumentar offset de 10 em 10, confome a paginação
        url = URL_OFFSET.format(offset)
        print(f"Raspando página {pagina + 1}/{total_paginas} : {url}")

        resultados = raspar_info(url)
        if resultados:
            dados_coletados.extend(resultados) # Adicionar os resultados a lista
    
    return dados_coletados


# 🟢 Executando a raspagem

dados = raspar_todas_as_paginas(URL_PESQUISA)

if dados:
    for item in dados[:5]:
        print(item)
else:
    print("Nenhum dado encontrado")


#dados = raspar_info(URL_PESQUISA)
#obter_total_paginas()

# for item in dados:
#     print(item)