from decimal import Decimal
import csv

from cnpj.modelo import Empresa
from cnpj.layout import ENCODING, DELIMITADOR


def para_decimal(valor: str) -> Decimal | None:
    """Converte valor com vírgula decimal para Decimal."""
    if not valor.strip():
        return None
    return Decimal(valor.replace(",", "."))

def ler_empresas(caminho_csv: str):
    with open(caminho_csv, encoding=ENCODING) as f:
        for campos in csv.reader(f, delimiter=DELIMITADOR):
            cnpj, razao, natureza, qualificacao, capital, porte, ente = campos
            yield Empresa(cnpj, razao, natureza, qualificacao, para_decimal(capital), porte, ente)