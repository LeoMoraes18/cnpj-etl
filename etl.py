import argparse
import sqlite3

from cnpj.aquisicao import obter_csv
from cnpj.leitura import ler_empresas
from cnpj.persistencia import gravar_empresas
from cnpj.consultar import buscar_empresas

parser = argparse.ArgumentParser(description="Ferramenta de ETL dos dados de CNPJ")
sub = parser.add_subparsers(dest="comando", required=True)

p_carregar = sub.add_parser("carregar", help="carrega um zip da Receita no banco")
p_carregar.add_argument("--zip", required=True)

p_buscar = sub.add_parser("buscar", help="consulta empresas no banco")
p_buscar.add_argument("--natureza")
p_buscar.add_argument("--capital_min", type=int)
p_buscar.add_argument("--limite", type=int, default=10)


if __name__ == "__main__":
    args = parser.parse_args()

    if args.comando == "carregar":
        if args.zip:
            caminho, _ = obter_csv(args.zip, "data/csv")
            empresas = ler_empresas(caminho)

            conexao = sqlite3.connect("data/cnpj.db")
            
            total = gravar_empresas(conexao, empresas)
            print(f"gravado {total} empresas")

    elif args.comando == "buscar":
        conexao = sqlite3.connect("data/cnpj.db")
    
        for cnpj, razao, capital in buscar_empresas(conexao, args.natureza, args.capital_min, args.limite):
            print(f"{cnpj} {razao} R$ {capital / 100 :>15,.2f}")

