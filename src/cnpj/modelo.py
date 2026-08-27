from dataclasses import dataclass, astuple
from decimal import Decimal

MEI = "2135"


@dataclass
class Empresa:
    cnpj_basico: str
    razao_social: str
    natureza_juridica: str
    qualificacao_responsavel: str
    capital_social: Decimal | None
    porte: str
    ente_federativo: str

    @property
    def capital_em_centavos(self) -> int | None:
        """Capital social na menor unidade monetária."""
        if self.capital_social is None:
            return None
        return int(self.capital_social * 100)

    @property
    def eh_mei(self) -> bool:
        return self.natureza_juridica == MEI

    def para_linha(self) -> tuple:
        """Campos na ordem do INSERT, com capital em centavos"""
        campos = astuple(self)
        return campos[:4] + (self.capital_em_centavos,) + campos[5:]