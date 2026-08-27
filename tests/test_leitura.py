from decimal import Decimal

from cnpj.leitura import para_decimal


def test_converte_virgula_decimal():
    valor = "5000,00"
    assert para_decimal(valor) == Decimal("5000.00")

def test_soma_decimal_e_exata_diferenca_de_float():
    assert para_decimal("0,10") + para_decimal("0,20") == Decimal("0.30")
    assert 0.10 + 0.20 != 0.30

def test_converte_zero():
    assert para_decimal("0,00") == Decimal("0")

def test_converte_valor_com_centavos():
    assert para_decimal("1500,50") == Decimal("1500.50")

def test_converte_vazio():
    assert para_decimal("") is None
