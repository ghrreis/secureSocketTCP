# Classe para validação de comandos permitidos
class CMDs():

    __command = ""
    __status = 0

    def __init__(self, cmd):
        self.__command = cmd
        print(self.__command)
        f = open("commands.txt", "r")  # Abre arquivo com os comandos válidos
        for line in f:  # Lê linha a linha dos comandos válidos
            # Verifica se o comando enviado pelo cliente é válido
            if self.__command == line.strip("\n"):  # Em caso positivo altera variável status para 1 finaliza loop
                self.__status = 1
                break
            else:  # Caso contrário altera variável status para 0
                print(0)
                self.__status = 0

    def status(self):
        return self.__status