import sqlite3
from collections.abc import Iterable

from cnpj.modelo import Empresa


def gravar_empresas(conexao: sqlite3.Connection, empresas: Iterable[Empresa], tamanho_lote: int = 10_000) -> int:
    """Grava empresas em lote e devolve o total gravado."""

    cursor = conexao.cursor()

    lote = []
    total = 0

    for empresa in empresas:
        lote.append(empresa.para_linha())
        total += 1

        if len(lote) >= tamanho_lote:
            cursor.executemany("INSERT INTO empresa VALUES (?, ?, ?, ?, ?, ?, ?)", lote)
            conexao.commit()
            lote.clear()


    if lote:
        cursor.executemany("INSERT INTO empresa VALUES (?, ?, ?, ?, ?, ?, ?)", lote)
        conexao.commit()

    return total
