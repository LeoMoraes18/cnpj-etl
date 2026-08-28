import sqlite3

from cnpj.esquema import criar_tabelas

if __name__ == '__main__':
    conexao = sqlite3.connect("data/cnpj.db")
    criar_tabelas(conexao)
    conexao.close()
