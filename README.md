# TCP socket
Aplicação cliente/servidor onde o cliente envia comandos de terminal ao servidor para ser executado no SO e devolver a resposta ao cliente.

## Instalação das bibliotecas necessárias
pip install pam

pip install six

## Execução do programa servidor
python serverThread.py

## Execução do programa cliente
python client.py usuario senha 127.0.0.1 "ls -l"

## Resultado de retorno do servidor
total 52

-rw-rw-r-- 1 gustavo gustavo   782 abr 13  2021 client.py

-rw-rw-r-- 1 gustavo gustavo 35149 abr 13  2021 LICENSE

-rw-rw-r-- 1 gustavo gustavo   155 nov  3 23:55 README.md

-rw-rw-r-- 1 gustavo gustavo  1584 abr 13  2021 serverNoThread.py

-rw-rw-r-- 1 gustavo gustavo  1713 nov  3 23:58 serverThread.py
