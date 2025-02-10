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
        print("Conectado com sucesso ao banco de dados")
        return conexao
    except Exception as e:
        print(f"Erro na tentativa de conexao ao banco de dados: {e}")
        return None
    
# Criar tabela no banco de dados

def criar_tabela():
    conexao = conectar_banco()
    if not conexao:
        return
    
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fraudes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome_docuimento VARCHAR(255) NOT NULL,
            link_ducmento TEXT,
            numero_processo VARCHAR(50),
            data_autuacao DATE NOT NULL,
            parte_1 VARCHAR(255),
            parte_2 VARCHAR(255),
            materia VARCHAR(255) NOT NULL,
            objeto TEXT,
            ano INT
        )
    """)

    # Criando índices para otimiazr a recuperação de dados
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_data_autuacao ON fraudes (data_autuacao);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_materia ON fraudes (materia);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_nome_documento ON fraudes (nome_documento);")

    # Commitar as alterações
    conexao.commit()
    cursor.close()
    conexao.close()
    print("tabela 'fraudes' criada com sucesso!")