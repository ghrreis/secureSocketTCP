# Classe para gerar logs do servidor

import logging


class Logs():

    __msg = ""

    def __init__(self, txt):
        self.__msg = txt

    def saveLog(self):
        # Gera arquivo tcp.log com o nível INFO
        logging.basicConfig(filename='tcp.log', level=logging.INFO)
        # Salva os dados (data:hora:IP:usuário:comando:msgs controle) no arquivo
        logging.info(self.__msg)
