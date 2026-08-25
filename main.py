import sqlite3
import time

from cnpj.aquisicao import obter_csv
from cnpj.leitura import ler_empresas
from cnpj.persistencia import gravar_empresas

if __name__ == "__main__":
    caminho_csv, extraiu = obter_csv("data/zips/Empresas0.zip", "data/csv")

    conexao = sqlite3.connect("data/cnpj.db")

    if extraiu:
        print("extraído")

    inicio = time.perf_counter()
    empresas = ler_empresas(caminho_csv)
    total = gravar_empresas(conexao, empresas)
    duracao = time.perf_counter() - inicio
    print(f"{total} linhas em {duracao}")
