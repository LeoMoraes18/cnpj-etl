from decimal import Decimal
import csv

from cnpj.modelo import Empresa, COLUNAS


def ler_empresas(caminho_csv: str):
    with open(caminho_csv, encoding="latin-1") as f:
        leitor = csv.reader(f, delimiter=";")
        for campos in leitor:
            registro = dict(zip(COLUNAS, campos))
            registro["capital_social"] = Decimal(registro["capital_social"].replace(",", "."))
            yield Empresa(**registro)
