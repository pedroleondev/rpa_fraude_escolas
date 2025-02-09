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

# URL de raspagem

URL_BASE = os.getenv("URL_BASE")

def verificar_site():
    session = HTMLSession()
    response = session.get(URL_BASE)
    
    if response.status_code == 200:
        logging.info(f"Site:  {URL_BASE} | está acessível.")
        return response
    else:
        logging.error(f"Erro ao acessar o site: {response.status_code}")
        return False
    
# def configurar_busca(palavras_chave="fraude em escolas"):

verificar_site()