import sqlite3
import pytest

from cnpj.schema import criar_tabelas

@pytest.fixture
def conexao():
    conexao = sqlite3.connect(":memory:")
    criar_tabelas(conexao)
    yield conexao
    conexao.close()