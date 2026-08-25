import sqlite3

conexao = sqlite3.connect("data/cnpj.db")
cursor = conexao.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS empresa (
        cnpj_basico TEXT PRIMARY KEY,
        razao_social TEXT NOT NULL,
        natureza_juridica TEXT,
        qualificacao_responsavel TEXT,
        capital_social TEXT,
        porte TEXT,
        ente_federativa TEXT
    )
""")

conexao.commit()
conexao.close()