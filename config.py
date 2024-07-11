import psycopg2

# Configuration de la base de données PostgreSQL
DB_HOST = 'localhost'
DB_NAME = 'PromptDB'
DB_USER = 'postgres'
DB_PASS = 'Toto123'

def get_db():
    conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
    return conn
