# Programa cliente
import json
import socket
import sys
from Security import Security


def receive_keys(key, addr):
    with open(addr + "_server_public.pem", "wb") as f:
        for item in key:
            f.write(item.encode()+"\n".encode())


if sys.argv[1] == "generate":
    security = Security("client")
    security.generate()
elif sys.argv[1] == "transmit":
    target_host = sys.argv[2]  # IP do servidor
    target_port = 9999  # Porta de conexão com o servidor
    security = Security("client")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria socket utilizando protocolo IPv4 e protocolo TCP
    client.connect((target_host, target_port))  # Conecta a um socket remoto passando os parâmetros host, porta
    client.send("transmit:".encode() + security.read_key())  # Envia conjunto de bytes (chave pública do cliente) para o socket remoto
    response = client.recv(8192)  # Recebe dados do socket remoto em um determinado tamanho de buffer
    print(response.decode().split("\\n"))  # Converte os bytes recebidos em string codificação UTF-8
    receive_keys(str(response, "utf-8").split("\n"), sys.argv[2])
elif sys.argv[1] == "send":
    user = str.encode(sys.argv[2])
    password = str.encode(sys.argv[3])

    target_host = sys.argv[4]  # IP do servidor
    target_port = 9999  # Porta de conexão com o servidor

    cmd = str.encode(sys.argv[5])  # Lista de argumentos passadas via linha de comando para o script Python

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria socket utilizando protocolo IPv4 e protocolo TCP

    client.connect((target_host, target_port))  # Conecta a um socket remoto passando os parâmetros host, porta

    # Criptografa a msg para ser enviado ao servidor
    security = Security(target_host + "_server")
    encrypted_cmd = security.encrypt('command:' + user.decode() + ':' + password.decode() + ':' + cmd.decode())

    # Envia conjunto de bytes (mensagens) para o socket remoto
    client.send(encrypted_cmd)

    response = client.recv(8192)  # Recebe dados do socket remoto em um determinado tamanho de buffer

    # Decriptografa a msg recebida do cliente
    security = Security("client")
    result = []
    for n in range(0, len(response), 256):
        part = response[n:n+256]
        result.append(security.decrypt(part))
    decrypt_msg = json.loads(''.join(result))
    print(decrypt_msg)  # Converte os bytes recebidos em string codificação UTF-8
