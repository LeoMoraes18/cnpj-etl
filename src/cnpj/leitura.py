from decimal import Decimal
import csv

from cnpj.modelo import Empresa, COLUNAS


def para_decimal(valor: str) -> Decimal | None:
    """Converte valor com vírgula decimal para Decimal."""
    if not valor.strip():
        return None
    return Decimal(valor.replace(",", "."))

def ler_empresas(caminho_csv: str):
    with open(caminho_csv, encoding="latin-1") as f:
        leitor = csv.reader(f, delimiter=";")
        for campos in leitor:
            registro = dict(zip(COLUNAS, campos))
            registro["capital_social"] = para_decimal(registro["capital_social"])
            yield Empresa(**registro)
