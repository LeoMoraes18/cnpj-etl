import sqlite3
import time


if __name__ == "__main__":
    conexao = sqlite3.connect("data/cnpj.db")
    cursor = conexao.cursor()

    SQL = "SELECT COUNT(*) FROM empresa WHERE natureza_juridica = ?"


    def medir(rotulo, natureza):
        cursor.execute("EXPLAIN QUERY PLAN " + SQL, (natureza,))
        plano = cursor.fetchall()[0][3]

        inicio = time.perf_counter()
        cursor.execute(SQL, (natureza,))
        total = cursor.fetchone()[0]
        duracao = time.perf_counter() - inicio

        print(f"{rotulo}: {total:_} linhas em {duracao:.3f}s | {plano}")

    cursor.execute("DROP INDEX IF EXISTS idx_empresa_natureza")
    conexao.commit()

    medir("sem indice / comum (2135)", "2135")
    medir("sem indice / raro  (3999)", "3999")

    inicio = time.perf_counter()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_empresa_natureza ON empresa(natureza_juridica)")
    conexao.commit()
    print(f"\nindice criado em {time.perf_counter() - inicio:.2f}s\n")

    medir("com indice / comum (2135)", "2135")
    medir("com indice / raro  (3999)", "3999")

    conexao.close()
