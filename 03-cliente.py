# Josiney de Souza
# 02-cliente.py
#
# Trabalho 2 do componente curricular Topicos em Redes de Computadores
# (INFO-7065) do Programa de Pos-Graduacao em Informatica (40001016034P5)
# da Universidade Federal do Parana (UFPR)
#
# Professor: Elias Procopio Duarte Junior
# Maio de 2023



# Adicao do modulo socket para conseguir realizar a conexao cliente-servidor
import socket
# Adicao do modulo ssl para usar o TLS e tornar a comunicacao segura
import ssl
# Adicao de modulo de funcoes e configuracoes comuns ao cliente e servidor
import confs_comuns



###############################################################################
# PROGRAMA PRINCIPAL
###############################################################################
# Criacao de um socket
# AF_INET: para se usar IPv4
# SOCK_STREAM: para se usar TCP
socket_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Formas de uso do TLS/SSL:
#
# Versao 1
# Fonte: https://docs.python.org/3/library/ssl.html
# Acesso em 12/05/2023
contexto = ssl.create_default_context()
# Para nao verificar o hostname nem o certificado, o
# "ssl._create_unverified_context()" eh equivalente a
# "contexto.check_hostname = False" e "contexto.verify_mode = ssl.CERT_NONE"
contexto.check_hostname = False
contexto.verify_mode = ssl.CERT_NONE
#contexto = ssl._create_unverified_context()
socket_tls = contexto.wrap_socket(socket_s, server_hostname="josiney")

# Usa o socket para se conectar ao servidor
socket_tls.connect((confs_comuns.END_SERVIDOR, confs_comuns.PORTA))

# Quando conectado, envia uma string ao servidor. Para enviar, eh necessario
# codifica-la como bytes, por isso se usa a funcao "encode()"
print("Enviando mensagem pré-definida ao servidor")
socket_tls.send("Olá, servidor!".encode())

# Aguarda pela mensagem de confirmação do servidor e a imprime. Como ela vem
# codificada como bytes, eh necessario decodifica-la com a funcao "decode()"
dados = socket_tls.recv(1024).decode()
print("Recebido do servidor:", dados)

# Obtem uma mensagem digitada pelo usuario e a envia ao servidor
dados = "O que quer enviar?\n" + confs_comuns.PROMPT[1] + " "
dados = input(dados)
socket_tls.send(dados.encode())

# Aguarda pela mensagem de confirmação do servidor e a imprime
dados = socket_tls.recv(1024).decode()
print("Recebido do servidor:", dados)

# Encerra a conexao com o servidor e finaliza
socket_tls.close()