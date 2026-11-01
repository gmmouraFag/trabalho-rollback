"""Impede empacotamento quando as capas declaradas nao existem."""
import json
import sys
from pathlib import Path


def validar(raiz):
    raiz=Path(raiz).resolve()

    def caminho(relativo):
        destino=(raiz/relativo).resolve()
        if not destino.is_relative_to(raiz):
            raise ValueError(f'Caminho fora da raiz da release: {relativo}')
        return destino

    config=json.loads(caminho('config/app-config.json').read_text(encoding='utf-8'))
    catalogo=json.loads(caminho(config['catalogoUrl']).read_text(encoding='utf-8'))
    jogos=catalogo['jogos']
    if not isinstance(jogos,list) or not jogos:
        raise ValueError('Catalogo vazio ou invalido')
    ausentes=[]
    for jogo in jogos:
        relativo=str(Path(config['pastaCapas'])/jogo['capa'])
        if not caminho(relativo).is_file(): ausentes.append(relativo)
    for relativo in ausentes:
        print(f'::error::Capa ausente na release: {relativo}')
    if ausentes:
        print(f'RELEASE BLOQUEADA: {len(ausentes)}/{len(jogos)} capas ausentes.')
        return 1
    print(f"RELEASE APROVADA: versao {config['versao']}, {len(jogos)}/{len(jogos)} capas existentes.")
    return 0


if __name__=='__main__':
    try:
        codigo=validar(sys.argv[1] if len(sys.argv)>1 else '.')
    except (OSError,ValueError,KeyError,TypeError) as erro:
        print(f'::error::Release invalida: {erro}')
        codigo=1
    sys.exit(codigo)
