import sqlite3
from decimal import Decimal
from collections.abc import Iterable

from cnpj.modelo import Empresa


def para_centavos(valor: Decimal | None) -> int | None:
    """Converte Decimal em reais para inteiro em centavos"""
    return int(valor*100) if valor is not None else None

def gravar_empresas(conexao: sqlite3.Connection, empresas: Iterable[Empresa], tamanho_lote: int = 10_000) -> int:
    """Grava empresas em lote e devolve o total gravado."""

    cursor = conexao.cursor()

    lote = []
    total = 0

    for empresa in empresas:
        lote.append((
            empresa.cnpj_basico,
            empresa.razao_social,
            empresa.natureza_juridica,
            empresa.qualificacao_responsavel,
            para_centavos(empresa.capital_social),
            empresa.porte,
            empresa.ente_federativo,
        ))
        total += 1

        if len(lote) >= tamanho_lote:
            cursor.executemany("INSERT INTO empresa VALUES (?, ?, ?, ?, ?, ?, ?)", lote)
            conexao.commit()
            lote.clear()


    if lote:
        cursor.executemany("INSERT INTO empresa VALUES (?, ?, ?, ?, ?, ?, ?)", lote)
        conexao.commit()

    return total
