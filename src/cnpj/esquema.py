import sqlite3


DDL_EMPRESA = """
    CREATE TABLE IF NOT EXISTS empresa (
        cnpj_basico TEXT PRIMARY KEY,
        razao_social TEXT NOT NULL,
        natureza_juridica TEXT,
        qualificacao_responsavel TEXT,
        capital_social INTEGER,
        porte TEXT,
        ente_federativo TEXT
    )
"""

def criar_tabelas(conexao: sqlite3.Connection) -> None:
    """Cria o schema se ainda não existir."""
    conexao.execute(DDL_EMPRESA)
    conexao.commit()

