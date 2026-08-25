import csv

def carregar_naturezas(caminho: str) -> tuple[dict[str, str], int]:
    """Devolve (mapa de codigo -> descricao, quantidade de linhas ignoradas)."""
    naturezas = {}
    ignoradas = 0

    with open(caminho, encoding="latin-1") as f:
        for campos in csv.reader(f, delimiter=";"):
            if len(campos) != 2:
                ignoradas += 1
                continue
            codigo, descricao = campos
            naturezas[codigo] = descricao

    return naturezas, ignoradas
