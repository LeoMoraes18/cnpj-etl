from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Empresa:
    cnpj_basico: str
    razao_social: str
    natureza_juridica: str
    qualificacao_responsavel: str
    capital_social: Decimal | None
    porte: str
    ente_federativo: str


COLUNAS = (
    "cnpj_basico",
    "razao_social",
    "natureza_juridica",
    "qualificacao_responsavel",
    "capital_social",
    "porte",
    "ente_federativo",
)