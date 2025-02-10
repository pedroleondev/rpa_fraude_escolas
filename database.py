import os
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
    try:
        conexao = mysql.connector.connect(**DB_CONFIG)
        print("✅ Conectado com sucesso ao banco de dados.")
        return conexao
    except Exception as e:
        print(f"❌ Erro na tentativa de conexao ao banco de dados: {e}")
        return None
    
# Criar tabela no banco de dados

def criar_tabela():
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
                link_documento TEXT,
                numero_processo VARCHAR(50),
                data_autuacao DATE NOT NULL,
                parte_1 VARCHAR(255),
                parte_2 VARCHAR(255),
                materia VARCHAR(255) NOT NULL,
                objeto TEXT,
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
    conexao = conectar_banco()
    if not conexao:
        return
    
    cursor = conexao.cursor()


    query = """ 
    INSERT INTO fraudes
    (nome_documento, link_documento, numero_processo, data_autuacao, parte_1, parte_2, materia, objeto, ano)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    try:
        cursor.executemany(query, dados)
        conexao.commit()
        print(f"✅ {cursor.rowcount} registro inseridos com sucesso!")
    except mysql.connector.Error as e:
        print(f"Erro ao inserir dados: {e}.")
    finally:
        cursor.close()
        conexao.close()

