# Secure Socket TCP
Aplicação cliente/servidor onde o cliente envia comandos de terminal ao servidor para ser executado no SO e devolver a resposta ao cliente.

Toda a comunicação é feita de forma criptografada
## Instalação das bibliotecas necessárias
pip install 

pip install pam 

pip install rsa 

pip install six 

pip install logging

## Execução do programa servidor
### Gera as chaves pública/privada do servidor 
python serverThread.py **_generate_**
### Executa o servidor
python serverThread.py **_run_**

## Execução do programa cliente
### Gera as chaves pública/privada do cliente
python client.py **_generate_**
### Transmite a chave pública do cliente para o servidor e recebe a chave pública do servidor
python client.py **_transmit_**
### Envia usuário, senha e comando para ser executado no servidor
python client.py **_send_** usuario senha 127.0.0.1 "ls -l"

## Resultado de retorno do servidor
total 52

-rw-rw-r-- 1 gustavo gustavo   782 abr 13  2021 client.py

-rw-rw-r-- 1 gustavo gustavo 35149 abr 13  2021 LICENSE

-rw-rw-r-- 1 gustavo gustavo   155 nov  3 23:55 README.md

-rw-rw-r-- 1 gustavo gustavo  1713 nov  3 23:58 serverThread.py
