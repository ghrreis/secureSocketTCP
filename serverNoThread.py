import subprocess
import socket
from datetime import datetime
from Log import Logs
from Auth import Authentication
from Commands import CMDs

bind_ip = "0.0.0.0"  # Aceita conexão de qualquer origem
bind_port = 9999  # Porta que o servidor "escuta"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria socket utilizando protocolo IPv4 e protocolo TCP

server.bind((bind_ip, bind_port))  # Atribui ao socket endereço e porta de conexão

server.listen(5)  # Define que o servidor está pronto para receber conexões com no máximo 5

print("[*] Listening on", bind_ip, ":", bind_port)  # Imprime os endereços IP e Porta que o servidor está sendo executado


def handle_client(client_socket, addr):
    request = client_socket.recv(8192)  # Recebe dados do socket remoto em um determinado tamanho de buffer

    # Converte a mensagem de byte para string e imprime a mensagem recebida separada por espaços em branco
    print("[*] Received:", str(request, "utf-8").split(" "))

    # Pega data e hora corrente do servidor
    data = datetime.today().strftime('%d/%m/%Y')
    hora = datetime.today().strftime('%Hh%M')

    # Vetor com usuário, senha e comando que será executado pelo servidor
    cmd = str(request, "utf-8").split(" ")

    # Verifica se a quantidade de argumentos passados pelo cliente é igual a 4
    if len(cmd) >= 3:
        # Prepara a autenticação do usuário
        auth = Authentication(cmd[0], cmd[1])
        # Verifica se a autenticação foi efetuada com sucesso
        if auth.auth():
            command = CMDs(' '.join(cmd[2:]))  # Envia commando para validação
            # Verifica se o comando é válido
            if command.status() == 1:  # Se for verdadeiro executa o comando
                # Gera o log do comando recebido do cliente
                log = Logs(data + ':' + hora + ':' + addr[0] + ':' + cmd[0] + ':' + ' '.join(cmd[2:]))
                log.saveLog()

                # Executa o comando no terminal do SO e retorna o resultado
                result = subprocess.run(cmd[2:], stdout=subprocess.PIPE)
                client_socket.send(result.stdout)  # Envia conjunto de bytes (mensagens) para o socket remoto
            else: # Se for falso não executa o comando
                log = Logs(data + ':' + hora + ':' + addr[0] + ':' + cmd[0] + ':' + ' '.join(cmd[2:]) + ':' +
                           'Comando não permitido')
                log.saveLog() # Salva o log no arquivo
                client_socket.send("Comando não permitido".encode())  # Envia conjunto de bytes (mensagens) para o socket remoto
        else:
            # Gera o log de erro de autenticação
            log = Logs(data + ':' + hora + ':' + addr[0] + ':' + cmd[0] + ':' + 'Erro de autenticação')
            log.saveLog()
            # Envia conjunto de bytes (mensagens) para o socket remoto
            client_socket.send(str.encode('Erro de autenticação'))
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

    # Chama a função handle_client passando como parêmetro o socket do cliente
    handle_client(client, addr)
