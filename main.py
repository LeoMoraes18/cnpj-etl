import time

from cnpj.aquisicao import obter_csv
from cnpj.leitura import ler_empresas


if __name__ == "__main__":
    caminho_csv, extraiu = obter_csv("data/zips/Empresas0.zip", "data/csv")

    if extraiu:
        print("extraído")

    inicio = time.perf_counter()

    total = 0
    for empresa in ler_empresas(caminho_csv):
        total += 1

    duracao = time.perf_counter() - inicio
    print(f"{total} linhas em {duracao}")
