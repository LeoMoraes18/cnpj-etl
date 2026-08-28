import sqlite3

def buscar_empresas(
        conexao: sqlite3.Connection,
        natureza: str | None = None,
        capital_min: int | None = None,
        limite: int = 10) -> list[tuple[str, str, int | None]]:
    """Consultar empresas com filtros opcionais. Devolve lista de tuplas."""

    condicoes: list[str] = []
    valores: list[str | int] = []

    if natureza is not None:
        condicoes.append("natureza_juridica = ?")
        valores.append(natureza)

    if capital_min is not None:
        condicoes.append("capital_social >= ?")
        valores.append(capital_min * 100)

    sql = "SELECT cnpj_basico, razao_social, capital_social FROM empresa"

    if condicoes:
        sql += " WHERE " + " AND ".join(condicoes)

    sql += " LIMIT ?"
    valores.append(limite)

    return conexao.execute(sql, valores).fetchall()
