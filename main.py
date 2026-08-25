import sqlite3
import time

from cnpj.aquisicao import obter_csv
from cnpj.leitura import ler_empresas


if __name__ == "__main__":
    caminho_csv, extraiu = obter_csv("data/zips/Empresas0.zip", "data/csv")

    conexao = sqlite3.connect("data/cnpj.db")
    cursor = conexao.cursor()

    if extraiu:
        print("extraído")

    inicio = time.perf_counter()

    LOTE = 10_000
    lote = []
    total = 0
    for empresa in ler_empresas(caminho_csv):
        lote.append((
            empresa.cnpj_basico,
            empresa.razao_social,
            empresa.natureza_juridica,
            empresa.qualificacao_responsavel,
            str(empresa.capital_social),
            empresa.porte,
            empresa.ente_federativo,
        ))
        total += 1

        if len(lote) >= LOTE:
            cursor.executemany("INSERT INTO empresa VALUES (?, ?, ?, ?, ?, ?, ?)", lote)
            conexao.commit()
            lote.clear()


    if lote:
        cursor.executemany("INSERT INTO empresa VALUES (?, ?, ?, ?, ?, ?, ?)", lote)
        conexao.commit()

    duracao = time.perf_counter() - inicio
    print(f"{total} linhas em {duracao}")
