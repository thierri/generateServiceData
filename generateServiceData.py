import requests
import re
import json
import shutil
import os
from datetime import datetime
"""
Service Dashboard
Script utilizado para confeccionar o arquivo base com os dados dos microservicos.
"""

LISTA_REPOSITORIOS="repositoriosServico.txt"
ITENS_FICHA_TECNICA = ("funcionalidade", "macro_funcionalidade", "descritivo", "listen_topics", "produce_topics", "sit_producao", "sit_homol", "sit_dev", "obs", "contato")
BASE_REGEX = r'\|\*INDEX\*\|[\w ]+\|([\w .,-@]+)\|'
SERVICE_DATA_FILE = 'serviceData.js'
SERVICE_DATA_FOLDER = 'serviceData/'
OLD_SERVICE_DATA_FOLDER = 'serviceData/anteriores/'


def main():
    f = open(LISTA_REPOSITORIOS, "r")
    finalResult = []
    for file_line in f:
        print('-> Processando Repositório: ')
        print(file_line + "\n")
        fichaTecninca = obterFichaTecnica(file_line)
        finalResult.append(fichaTecninca)
    # print(json.dumps(finalResult))
    moveFile()
    f = open( SERVICE_DATA_FOLDER +  SERVICE_DATA_FILE, "w")
    f.write("const serviceData = " + json.dumps(finalResult) + ";\n")
    f.close()

def moveFile():
    timestamp =  str(int(datetime.timestamp(datetime.now())))
    if os.path.isfile(SERVICE_DATA_FOLDER + SERVICE_DATA_FILE):
        shutil.move(SERVICE_DATA_FOLDER + SERVICE_DATA_FILE, OLD_SERVICE_DATA_FOLDER + str(timestamp + SERVICE_DATA_FILE))

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
            print('[ERRO] -> Não foi possível adicionar o item ' + item_ficha_tecnica)
        
    return fichaTecnica




if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()