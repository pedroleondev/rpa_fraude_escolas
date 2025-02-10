from database import criar_tabela, inserir_dados
from scraper import raspar_todas_as_paginas

# Definir URLs da pesquisa
URL_PESQUISA = "https://www.tce.sp.gov.br/jurisprudencia/pesquisar?txtTdPalvs=fraude+em+prefeitura&acao=Executa"
URL_OFFSET = "https://www.tce.sp.gov.br/jurisprudencia/pesquisar?txtTdPalvs=fraude+em+escolas&acao=Executa&offset={}"

# Criar a tabela se ainda não existir
criar_tabela()

# Executar raspagem
dados = raspar_todas_as_paginas(URL_PESQUISA, URL_OFFSET)

# print("\n🔍 Dados coletados para inserção:")
# for dado in dados[:5]:  # Exibir os 5 primeiros para depuração
#     print(dado)


# Inserir dados no banco
if dados:
    inserir_dados(dados)
    print("✅ Dados inseridos no banco com sucesso!")
else:
    print("❌ Nenhum dado encontrado para inserir.")
