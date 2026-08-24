import zipfile
import csv
from decimal import Decimal
import time
import os


COLUNAS = (
    "cnpj_basico",
    "razao_social",
    "natureza_juridica",
    "qualificacao_responsavel",
    "capital_social",
    "porte",
    "ente_federativo",
)

def obter_csv(caminho_zip: str, pasta_destino: str) -> tuple[str, bool]:
    with zipfile.ZipFile(caminho_zip) as zf:
        nome = zf.namelist()[0]
        caminho = os.path.join(pasta_destino, nome)
        if os.path.exists(caminho):
            return caminho, False
        zf.extract(nome, path=pasta_destino)
    return caminho, True


def ler_empresas(caminho_csv: str):
    with open(caminho_csv, encoding="latin-1") as f:
        leitor = csv.reader(f, delimiter=";")
        for campos in leitor:
            registro = dict(zip(COLUNAS, campos))
            registro["capital_social"] = Decimal(registro["capital_social"].replace(",", "."))
            yield registro


caminho_csv, extraiu = obter_csv("data/zips/Empresas1.zip", "data/csv")

if extraiu:
    print("extraído")

inicio = time.perf_counter()

total = 0
for empresa in ler_empresas(caminho_csv):
    total += 1

duracao = time.perf_counter() - inicio
print(f"{total} linhas em {duracao}")
