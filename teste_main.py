import unittest
from database import conectar_banco, criar_tabela
from scraper import raspar_info

class TestProjeto(unittest.TestCase):

    def test_conexao_banco(self):
        """ Testa se a conexão com o banco de dados é bem-sucedida """
        conexao = conectar_banco()
        self.assertIsNotNone(conexao)
        conexao.close()

    def test_criacao_tabela(self):
        """ Testa se a tabela é criada corretamente """
        criar_tabela()
        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("SHOW TABLES LIKE 'fraudes';")
        tabela_existe = cursor.fetchone()
        self.assertIsNotNone(tabela_existe)
        conexao.close()

    def test_raspagem(self):
        """ Testa se a raspagem de dados retorna pelo menos um resultado """
        url_teste = "https://www.tce.sp.gov.br/jurisprudencia/pesquisar?txtTdPalvs=fraude+em+prefeitura&acao=Executa"
        resultados = raspar_info(url_teste)
        self.assertGreater(len(resultados), 0)

if __name__ == "__main__":
    unittest.main()
