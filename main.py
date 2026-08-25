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

    total = 0
    for empresa in ler_empresas(caminho_csv):
        cursor.execute(
            "INSERT INTO empresa VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                empresa.cnpj_basico,
                empresa.razao_social,
                empresa.natureza_juridica,
                empresa.qualificacao_responsavel,
                str(empresa.capital_social),
                empresa.porte,
                empresa.ente_federativo,
            ),
        )
        total += 1

        if total % 10000 == 0:
            conexao.commit()
            print(total)

    conexao.commit()
    conexao.close()

    duracao = time.perf_counter() - inicio
    print(f"{total} linhas em {duracao}")
