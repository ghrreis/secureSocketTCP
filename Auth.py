# Classe para autenticar o usuário

import pam


class Authentication():

    __user = ""
    __password = ""

    # Recebe, como parâmetro, usuário e senha
    def __init__(self, user, password):
        self.__user = user
        self.__password = password

    # Autentica o usuário
    def auth(self):
        # Retorna status do login
        __status = pam.authenticate(self.__user, self.__password)
        return __status
