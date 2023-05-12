# Josiney de Souza
# 02-servidor.py
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
contexto = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
contexto.load_cert_chain(certfile="certificado.crt", keyfile="chave-privada.pem")

# Associa o endereco do servidor e a porta de uso com o socket
socket_s.bind((confs_comuns.END_SERVIDOR, confs_comuns.PORTA))

# Coloca o servidor em modo de escuta por conexoes
socket_s.listen()

# Depois de estar em modo de escuta, aceita as conexoes de clientes
conexao, end_cliente = socket_s.accept()
constream = contexto.wrap_socket(conexao, server_side=True)

# Mostra que um cliente se conectou e exibe seu endereco e porta contidos
# na variavel "end_cliente"
print(confs_comuns.MSG["clientecon"], end_cliente)

# Recebe os dados enviados pelo cliente. Como ela vem codificada como
# bytes, eh necessario decodifica-la com a funcao "decode()"
dados = constream.recv(1024).decode()

# Exibe a mensagem recebida do cliente
print(confs_comuns.MSG["docliente"], dados)

# Envia mensagem de confirmação para o cliente
dados = confs_comuns.RETORNOS["ack"]
constream.send(dados.encode())

# Aguarda uma nova mensagem do cliente
dados = constream.recv(1024).decode()

# Exibe a nova mensagem
print(confs_comuns.MSG["docliente"], dados)

# Envia mais uma confirmacao de recebimento da mensagem
dados = confs_comuns.RETORNOS["ack"]
constream.send(dados.encode())

# Recebe a mensagem de fechamento da conexao do cliente e finaliza
dados = constream.recv(1024).decode()
print(confs_comuns.MSG["fim"])

# Encerra a conexao com o cliente
#dados = conexao.recv()
conexao.close()