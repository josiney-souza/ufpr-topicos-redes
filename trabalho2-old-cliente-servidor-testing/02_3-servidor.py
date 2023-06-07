from socket import socket, AF_INET, SOCK_STREAM
from ssl import SSLContext, PROTOCOL_TLS_SERVER

ip = '127.0.0.1'
port = 8443
context = SSLContext(PROTOCOL_TLS_SERVER)
#context.load_cert_chain('certificado.pem', 'chave-ssl.pem')
context.load_cert_chain('server-public-key.pem', 'server-private-key.pem')

with socket(AF_INET, SOCK_STREAM) as server:
    server.bind((ip, port))
    server.listen(1)
    with context.wrap_socket(server, server_side=True) as tls:
        connection, address = tls.accept()
        print(f'Connected by {address}\n')

        data = connection.recv(1024)
        print(f'Client Says: {data}')

        connection.sendall(b"You're welcome")

# Base do codigo
# https://github.com/arthurazs/python-tls/blob/master/server.py
# Acesso em: 11/05/2023