from decimal import Decimal

from cnpj.persistencia import gravar_empresas
from cnpj.modelo import Empresa


def empresa(cnpj="11111111", capital=Decimal("5000.00")):
    return Empresa(cnpj, "RAZAO TESTE", "2135", "50", capital, "01", "")

def test_grava_uma_empresa(conexao):
    total = gravar_empresas(conexao, [empresa()])

    assert total == 1
    assert conexao.execute("SELECT COUNT(*) FROM empresa").fetchone()[0] == 1

def test_grava_capital_em_centavos(conexao):
    gravar_empresas(conexao, [empresa(capital=Decimal("5000.00"))])

    valor = conexao.execute("SELECT capital_social FROM empresa").fetchone()[0]
    assert valor == 500_000

def test_capital_ausente_vira_null(conexao):
    gravar_empresas(conexao, [empresa(capital=None)])

    valor = conexao.execute("SELECT capital_social FROM empresa").fetchone()[0]
    assert valor is None

def test_grava_lote_incompleto(conexao):
    empresas = [empresa(cnpj=f"{i:08d}") for i in range(25)]

    total = gravar_empresas(conexao, empresas, tamanho_lote=10)

    assert total == 25
    assert conexao.execute("SELECT COUNT(*) FROM empresa").fetchone()[0] == 25