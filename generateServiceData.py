import requests
import re

"""
Service Dashboard
Script utilizado para confeccionar o arquivo base com os dados dos microservicos.
"""

LISTA_REPOSITORIOS="repositoriosServico.txt"
ITENS_FICHA_TECNICA = ("funcionalidade", "macro_funcionalidade", "descritivo")
BASE_REGEX = r'\|\*INDEX\*\|[a-zA-Z ]+\|([\w .]+)\|'

def main():
    f = open(LISTA_REPOSITORIOS, "r")
    for file_line in f:
        print('-> Processando Repositório: ')
        print(file_line)
        obterFichaTecnica(file_line)

def obterFichaTecnica(url):
    r = requests.get(url)
    readmeContent = r.text
    fichaTecnica = {
        "repo_url": url
    }
    for item_ficha_tecnica in ITENS_FICHA_TECNICA:
        # Obtém indice do item da ficha tecninca que queremos buscar
        index = ITENS_FICHA_TECNICA.index(item_ficha_tecnica) + 1

        # Cria o regex adequado a partir do regex base.
        regex = BASE_REGEX.replace("INDEX", str(index))

        match = re.search(regex, readmeContent)
        
        try:
            print(item_ficha_tecnica+ ': ' + match.group(1))
            fichaTecnica[item_ficha_tecnica] = match.group(1)
        except:
            print('-> Não foi possível adicionar o item ' + item_ficha_tecnica)
        
    return fichaTecnica




if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()