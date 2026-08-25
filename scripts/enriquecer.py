import time

from cnpj.aquisicao import obter_csv
from cnpj.leitura import ler_empresas
from cnpj.referencia import carregar_naturezas


if __name__ == "__main__":
    caminho_nat, _ = obter_csv("data/zips/Naturezas.zip", "data/csv")
    naturezas, ignoradas = carregar_naturezas(caminho_nat)

    print(f"{len(naturezas)} naturezas carregadas")
    if ignoradas:
        print(f"atenção: {ignoradas} linhas ignoradas")
        
    caminho_csv, _ = obter_csv("data/zips/Empresas0.zip", "data/csv")

    inicio = time.perf_counter()
    total = 0

    for empresa in ler_empresas(caminho_csv):
        descricao = naturezas.get(empresa.natureza_juridica)
        total += 1
        if total >= 200_000:
            break

    duracao = time.perf_counter() - inicio
    print(f"{total:_} linhas em {duracao:.2f}s")
