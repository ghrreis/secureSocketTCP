# Programa servidor
import json
import subprocess
import socket
import threading
import sys
import os
from datetime import datetime
from Log import Logs
from Auth import Authentication
from Commands import CMDs
from Security import Security

# Se argumento for igual a generate, gera as chaves públicas e privadas do servidor
if sys.argv[1] == "generate":
    security = Security("server")
    security.generate()
    #print(security.encrypt("Olá mundo"))
# Se argumento for igual a run, executa o servidor para receber msgs do cliente
elif sys.argv[1] == "run":
    bind_ip = "0.0.0.0"  # Aceita conexão de qualquer origem
    bind_port = 9999  # Porta que o servidor "escuta"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria socket utilizando protocolo IPv4 e protocolo TCP

    server.bind((bind_ip, bind_port))  # Atribui ao socket endereço e porta de conexão

    server.listen(10)  # Define que o servidor está pronto para receber conexões com no máximo 5

    print("[*] Listening on", bind_ip, ":", bind_port)  # Imprime os endereços IP e Porta que o servidor está sendo executado


    def receive_keys(key, addr):
        with open(addr[0] + "_public.pem", "wb") as f:
            for item in key:
                f.write(item.encode()+"\n".encode())
        # Pega data e hora corrente do servidor
        data = datetime.today().strftime('%d/%m/%Y')
        hora = datetime.today().strftime('%Hh%M')

        # Gera o log do comando recebido do cliente
        log = Logs(data + ':' + hora + ':' + addr[0] + ':' + 'Chave recebida')
        log.saveLog()

    def encrypt_msg(msg, addr):
        security = Security(addr)
        msg = json.dumps(msg)
        result = []
        for n in range(0, len(msg), 245):
            part = msg[n:n+245]
            result.append(security.encrypt(part))
        return b''.join(result)

    def handle_client(client_socket, addr):
        request = client_socket.recv(8192)  # Recebe dados do socket remoto em um determinado tamanho de buffer
        if not os.path.exists(addr[0]+"_public.pem"):
            cmd = str(request, "utf-8").split(":")
            # Se msg igual a transmit, faz a troca de chaves públicas
            if cmd[0] == "transmit":
                receive_keys(cmd[1:], addr)
                security = Security("server")
                client_socket.send(security.read_key())
        else:
            # Decriptografa a msg recebida do cliente
            security = Security("server")
            decrypt_cmd = security.decrypt(request)

            # Converte a mensagem de byte para string e imprime a mensagem recebida separada por espaços em branco
            print("[*] Received:", decrypt_cmd.split(":"))

            # Pega data e hora corrente do servidor
            data = datetime.today().strftime('%d/%m/%Y')
            hora = datetime.today().strftime('%Hh%M')

            # Vetor com usuário, senha e comando que será executado pelo servidor
            cmd = decrypt_cmd.split(":")

            # Se msg igual a command, autentica o usuário e executa o comando recebido do cliente
            if cmd[0] == "command":
                # Prepara a autenticação do usuário
                auth = Authentication(cmd[1], cmd[2])
                # Verifica se a autenticação foi efetuada com sucesso
                if auth.auth():
                    command = CMDs(' '.join(cmd[3:])) # Envia commando para validação
                    # Verifica se o comando é válido
                    if command.status() == 1: # Se for verdadeiro executa o comando
                        # Gera o log do comando recebido do cliente
                        log = Logs(data + ':' + hora + ':' + addr[0] + ':' + cmd[1] + ':' + ' '.join(cmd[3:]))
                        log.saveLog()

                        # Executa o comando no terminal do SO e retorna o resultado
                        cmd = cmd[3].split(" ") # Necessário para permitir execução de comandos com parâmetros
                        result = subprocess.run(cmd[0:], stdout=subprocess.PIPE)
                        # Envia conjunto de bytes (mensagens) para o socket remoto
                        #client_socket.send(result.stdout)
                        client_socket.send(encrypt_msg(result.stdout.decode(), addr[0]))
                    else:  # Se for falso não executa o comando
                        log = Logs(data + ':' + hora + ':' + addr[0] + ':' + cmd[1] + ':' + ' '.join(cmd[3:]) + ':' +
                                   'Comando não permitido')
                        log.saveLog() # Salva o log no arquivo
                        # Envia conjunto de bytes (mensagens) para o socket remoto
                        client_socket.send(encrypt_msg("Comando não permitido", addr[0]))
                else:
                    # Gera o log de erro de autenticação
                    log = Logs(data + ':' + hora + ':' + addr[0] + ':' + cmd[1] + ':' + 'Erro de autenticação')
                    log.saveLog()
                    # Envia conjunto de bytes (mensagens) para o socket remoto
                    client_socket.send(encrypt_msg("Erro de autenticação!!!", addr[0]))
            else:
                # Gera o log de erro de parâmetros insuficientes
                log = Logs(data + ':' + hora + ':' + addr[0] + ':' + 'Erro nos parâmetros')
                log.saveLog()
                # Envia conjunto de bytes (mensagens) para o socket remoto
                client_socket.send(str.encode('Quantidade de parâmetros incorretos'))

            client_socket.close()  # Fecha conexão com o socket remoto

    while True:
        # Bloqueia o serviço até receber um pedido de conexão com os valores de conexão (socket cliente) e endereço
        client, addr = server.accept()

        print("[*] Accepted connection from:", addr[0], ":", addr[1])  # Imprime os endereços IP e Porta respectivamente

        # Cria uma thread passando como parâmetros a função handle_client e o socket do cliente
        client_handler = threading.Thread(target=handle_client, args=(client, addr))
        client_handler.start()  # Inicia a thread
