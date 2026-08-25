
def gravar_empresas(conexao, empresas, tamanho_lote: int = 10_000) -> int:
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
            str(empresa.capital_social),
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
