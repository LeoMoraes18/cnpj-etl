
def buscar_empresas(conexao, natureza=None, capital_min=None, limite=10):
    """Consultar empresas com filtros opcionais. Devolve lista de tuplas."""

    condicoes = []
    valores = []

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