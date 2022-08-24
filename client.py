import socket
import sys

user = str.encode(sys.argv[1])
password = str.encode(sys.argv[2])

target_host = sys.argv[3]  # IP do servidor
target_port = 9999  # Porta de conexão com o servidor

cmd = str.encode(sys.argv[4])  # Lista de argumentos passadas via linha de comando para o script Python

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria socket utilizando protocolo IPv4 e protocolo TCP

client.connect((target_host, target_port))  # Conecta a um socket remoto passando os parâmetros host, porta

client.send(user + str.encode(' ') + password + str.encode(' ') + cmd)  # Envia conjunto de bytes (mensagens) para o socket remoto

response = client.recv(8192)  # Recebe dados do socket remoto em um determinado tamanho de buffer

print(str(response, "utf-8"))  # Converte os bytes recebidos em string codificação UTF-8
