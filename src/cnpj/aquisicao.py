import os
import zipfile

def obter_csv(caminho_zip: str, pasta_destino: str) -> tuple[str, bool]:
    with zipfile.ZipFile(caminho_zip) as zf:
        nome = zf.namelist()[0]
        caminho = os.path.join(pasta_destino, nome)
        if os.path.exists(caminho):
            return caminho, False
        zf.extract(nome, path=pasta_destino)
    return caminho, True