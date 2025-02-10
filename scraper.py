import logging
from requests_html import HTMLSession


# Configurar logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# URL_PESQUISA = "https://www.tce.sp.gov.br/jurisprudencia/pesquisar?txtTdPalvs=fraude+em+prefeitura&processo=&acao=Executa&buscaRapida=true&ignorarEntrada=false"
# URL_OFFSET = "https://www.tce.sp.gov.br/jurisprudencia/pesquisar?txtTdPalvs=fraude+em+escolas&acao=Executa&offset={}"

def raspar_info(url):

    """
    ✅Faz a raspagem dos dados de uma única página da URL fornecida.
    🔵Retorna uma lista com os resultados encontrados.
    """

    # Declarar Headers
    session = HTMLSession()
    session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'
    session.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    session.headers['Accept-Language'] = 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
    session.headers['Connection'] = 'keep-alive'
    session.headers['Upgrade-Insecure-Requests'] = '1'

    response = session.get(url)
    print(response.status_code)

    if response.status_code != 200:

        print(f"Erro ao acessar {url}, Status Code: {response.status_code}")
        return []

    # Encontrar todas as linhas da tabela (cada <tr>)
    linhas = response.html.xpath('//table/tbody/tr[contains(@class, "borda-superior")]')

    if not linhas:
        print(f"Nenhuma linha encontrada na página: {url}")
        return []

    # Lista para armazenar os resultados
    resultados = []

    # Processar cada linha
    for linha in linhas:
        colunas = linha.xpath('.//td')  # Captura todas as colunas da linha
        if len(colunas) < 8:
            continue

        # Capturar os elementos dentro das colunas
        elemento_doc = colunas[0].xpath('.//a')

        if elemento_doc:
            elemento_doc = colunas[0].xpath('.//a')[0]
            nome_doc = elemento_doc.text.strip()  # Nome do documento
            link_doc = elemento_doc.attrs.get('href', '').strip()  # Link do PDF
        else:
            nome_doc = "N/A"
            link_doc = "N/A"


        # Caputurar cada elemento da coluna (N° Proc.|Autuação|Parte 1|Parte 2|Matéria|Objeto|Exercício)

        num_processo = colunas[1].text.strip().split("\n")[0]
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

def obter_total_paginas(url):
    """
    ✅Obtém o total de páginas da URL de pesquisa.
    🔵Retorna o total de páginas encontrado.
    """
    # Declarar Headers
    session = HTMLSession()
    session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'
    session.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    session.headers['Accept-Language'] = 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
    session.headers['Connection'] = 'keep-alive'
    session.headers['Upgrade-Insecure-Requests'] = '1'

    response = session.get(url)
    
    if response.status_code != 200:
        print(f"Erro ao acessar {url}, Status Code: {response.status_code}")
        return 1

    try:
        #caputurar o botão de paginação, posição last() para pegar o último link
        ultimo_link = response.html.xpath('//nav/ul[@class="pagination pagination-sm"]/li[last()]/a/@href')
        if not ultimo_link:
            return 1
        
        ultimo_offset = int(ultimo_link[0].split("offset=")[-1])
        total_paginas = (ultimo_offset // 10) + 1
        print(f"🕵️‍♂️Total de páginas encontradas: {total_paginas}")
        return total_paginas

    except Exception as e:
        print(f"Erro ao obter total de páginas: {e}")
        return 1

def raspar_todas_as_paginas(url, url_offset):
    """
    ✅Faz a raspagem de todas as páginas da URL fornecida.
    🔵Retorna uma lista com todos os resultados encontrados.
    """
    #total_paginas = obter_total_paginas(url)
    total_paginas = 3 # apenas para testes curtos
    dados_coletados = []

    for pagina in range(total_paginas):
        offset = pagina * 10 
        url_completa = url_offset.format(offset)
        print(f"Raspando página {pagina + 1}/{total_paginas} : {url_completa}")
        resultados = raspar_info(url)
        
        if resultados:
            dados_coletados.extend(resultados) # Adicionar os resultados a lista
    
    return dados_coletados


