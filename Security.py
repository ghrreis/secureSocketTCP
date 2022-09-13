# Classe para gerar chaves RSA, criptografar e decriptografar mensagens

import rsa


class Security():

    __message = ""
    __file = ""
    __public_key = ""
    __private_key = ""

    def __init__(self, file_name):
        self.__file = file_name

    def generate(self):
        self.__public_key, self.__private_key = rsa.newkeys(2048)
        with open(self.__file+"_public.pem", "wb") as f:
            f.write(self.__public_key.save_pkcs1("PEM"))

        with open(self.__file+"_private.pem", "wb") as f:
            f.write(self.__private_key.save_pkcs1("PEM"))

    def encrypt(self, msg):
        self.__message = msg
        with open(self.__file+"_public.pem", "rb") as f:
            self.__public_key = rsa.PublicKey.load_pkcs1(f.read())

        return rsa.encrypt(self.__message.encode(), self.__public_key)

    def decrypt(self, msg):
        self.__message = msg
        with open(self.__file+"_private.pem", "rb") as f:
            self.__private_key = rsa.PrivateKey.load_pkcs1(f.read())

        return rsa.decrypt(self.__message, self.__private_key).decode()

    def read_key(self):
        with open(self.__file+"_public.pem", "rb") as f:
            public_key = f.read()
        return public_key