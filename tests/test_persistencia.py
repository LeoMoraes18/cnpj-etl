from decimal import Decimal

from cnpj.persistencia import para_centavos


def test_centavos_converte():
    assert para_centavos(Decimal("5000.00")) == 500_000

def test_centavos_preserva_none():
    assert para_centavos(None) is None
