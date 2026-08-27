import sqlite3


from cnpj.schema import criar_tabelas

conexao = sqlite3.connect("data/cnpj.db")
criar_tabelas(conexao)
conexao.close()
