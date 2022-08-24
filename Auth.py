# Classe para autenticar o usuário

import pam


class Authentication():

    __user = ""
    __password = ""

    def __init__(self, user, password):
        self.__user = user
        self.__password = password

    def auth(self):
        # Retorna status do login
        __status = pam.authenticate(self.__user, self.__password)
        return __status
