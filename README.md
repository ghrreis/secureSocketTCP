# Secure Socket TCP
Aplicação cliente/servidor onde o cliente envia comandos de terminal ao servidor para ser executado no SO e devolver a resposta ao cliente.

Toda a comunicação é feita de forma criptografada
## Instalação das bibliotecas necessárias
pip install pam rsa six logging

## Execução do programa servidor
### Gera as chaves pública/privada do servidor 
python serverThread.py generate
### Executa o servidor
python serverThread.py run

## Execução do programa cliente
### Gera as chaves pública/privada do cliente
python client.py generate
### Transmite a chave pública do cliente para o servidor e recebe a chave pública do servidor
python client.py transmit
### Envia usuário, senha e comando para ser executado no servidor
python client.py send usuario senha 127.0.0.1 "ls -l"

## Resultado de retorno do servidor
total 52

-rw-rw-r-- 1 gustavo gustavo   782 abr 13  2021 client.py

-rw-rw-r-- 1 gustavo gustavo 35149 abr 13  2021 LICENSE

-rw-rw-r-- 1 gustavo gustavo   155 nov  3 23:55 README.md

-rw-rw-r-- 1 gustavo gustavo  1713 nov  3 23:58 serverThread.py
