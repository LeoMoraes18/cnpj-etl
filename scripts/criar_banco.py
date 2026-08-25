import sqlite3

conexao = sqlite3.connect("data/cnpj.db")
cursor = conexao.cursor()

"""capital_social migrado para inteiro, para trabalhar com integer cents
    sendo necessario sempre na gravação multiplicar por 100
    e na leitura dividir por 100, previsto por uma limitação do sqlite
"""
cursor.execute("""
    CREATE TABLE IF NOT EXISTS empresa (
        cnpj_basico TEXT PRIMARY KEY,
        razao_social TEXT NOT NULL,
        natureza_juridica TEXT,
        qualificacao_responsavel TEXT,
        capital_social INTEGER,
        porte TEXT,
        ente_federativo TEXT
    )
""")

conexao.commit()
conexao.close()
