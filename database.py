import os
from datetime import datetime
import mysql.connector
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do banco de dados
DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "port": os.getenv("MYSQL_PORT"),
    "database": os.getenv("MYSQL_DATABASE"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
}

# Conectar ao banco de dados

def conectar_banco():
    """
    ✅Faz a conexão com o banco de dados.
    🔵Retorna a conexão.
    """
    try:
        conexao = mysql.connector.connect(**DB_CONFIG)
        print("✅ Conectado com sucesso ao banco de dados.")
        return conexao
    except Exception as e:
        print(f"❌ Erro na tentativa de conexao ao banco de dados: {e}")
        return None
    
# Criar tabela no banco de dados

def criar_tabela():
    """
    ✅Cria a tabela 'fraudes'
    🔵No banco de dados
    """
    conexao = conectar_banco()
    if not conexao:
        return

    cursor = conexao.cursor()
        # verificar se a tabela jã existe
    cursor.execute("SHOW TABLES LIKE 'fraudes';")
    tabela_existe = cursor.fetchone()

    if not tabela_existe:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fraudes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome_documento VARCHAR(255) NOT NULL,
                numero_processo VARCHAR(50),
                data_autuacao DATE NOT NULL,
                partes VARCHAR(255),
                materia VARCHAR(255) NOT NULL,
                link_documento TEXT,
                ano INT
            )
        """)
        print("✅ Tabela 'fraudes' criada com sucesso!")

    # Criando índices para otimiazr a recuperação de dados
    # 🟡 Mysql não aceita IF NOT EXISTS - necessário alteração

    try:
        cursor.execute("ALTER TABLE fraudes ADD INDEX idx_data_autuacao ON fraudes (data_autuacao);") 
        cursor.execute("ALTER TABLE fraudes ADD INDEX idx_materia ON fraudes (materia);")
        cursor.execute("ALTER TABLE fraudes ADD INDEX idx_nome_documento ON fraudes (nome_documento);")
    except mysql.connector.Error:
        pass
    
    # Commitar as alterações
    conexao.commit()
    cursor.close()
    conexao.close()

# Inserir dados na no banco de dados

def inserir_dados(dados):
    """
    ✅Insere múltiplos registros na tabela 'fraudes'.
    🔵Verifica duplicatas antes da inserção.
    """
    conexao = conectar_banco()
    if not conexao:
        return
    
    cursor = conexao.cursor()
    
    query = """
        INSERT INTO fraudes 
        (nome_documento, numero_processo, data_autuacao, 
        partes, materia, link_documento, ano)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    try:
        dados_formatados = []
        
        for d in dados:
            num_processo = " ".join(d["Numero_Processo"].split("\n")).strip()

            # 🔍 Verifica se o número do processo já existe no banco
            cursor.execute("SELECT EXISTS(SELECT 1 FROM fraudes WHERE numero_processo = %s)", (num_processo,))
            existe = cursor.fetchone()[0]
            
            if existe:
                print(f"⚠ Registro já existe para o processo {num_processo}. Pulando inserção.")
                continue  # Pula para o próximo dado
            
            # Formatar os dados corretamente e adicionar à lista
            dados_formatados.append((
                d["Nome_Documento"],
                num_processo,
                datetime.strptime(d["Data_Autuacao"], "%d/%m/%Y").date() if d["Data_Autuacao"] else None,
                str(d["Partes"]),  # 🔥 Converte lista para string antes de salvar no banco
                d["Materia"].strip(),
                d["URL"].strip(),
                int(d["Ano"]) if d["Ano"].isdigit() else None
            ))

        # 🔥 Só executa `executemany()` se houver registros novos
        if dados_formatados:
            cursor.executemany(query, dados_formatados)
            conexao.commit()
            print(f"✅ {cursor.rowcount} registros inseridos com sucesso!")
        else:
            print("⚠ Nenhum novo registro para inserir.")

    except mysql.connector.Error as e:
        print(f"❌ Erro ao inserir dados: {e}.")
    finally:
        cursor.close()
        conexao.close()


