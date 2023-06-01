# Josiney de Souza
# 02-invasor.py
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
# contexto = ssl.create_default_context()
# Para nao verificar o hostname nem o certificado, o
# "ssl._create_unverified_context()" eh equivalente a
# "contexto.check_hostname = False" e "contexto.verify_mode = ssl.CERT_NONE"
# contexto.check_hostname = False
# contexto.verify_mode = ssl.CERT_NONE
# contexto = ssl._create_unverified_context()
# socket_tls = contexto.wrap_socket(socket_s, server_hostname="josiney")
#
# Versao 2
# Fonte: https://gist.github.com/Oborichkin/d8d0c7823fd6db3abeb25f69352a5299
# Acesso em: 16/05/2023
# socket_tls = ssl.wrap_socket(socket_s,
# 		certfile="certificado.crt",
# 		keyfile="chave-privada.pem")
#
# Versao 3
# Fonte: https://vegibit.com/python-ssl-tutorial/
# Acesso em: 16/05/2023
contexto = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
# Para testar sem carregar certificados, deixar a linha abaixo comentada
# contexto.load_verify_locations(cafile="cert-rsa.pem")
# Carregando certificados errados - descomente a linha abaixo
# contexto.load_verify_locations(cafile="certificado.crt")
contexto.check_hostname = True
contexto.verify_mode = ssl.CERT_REQUIRED
socket_tls = contexto.wrap_socket(socket_s, server_hostname="localhost")

# Usa o socket para se conectar ao servidor
socket_tls.connect((confs_comuns.END_SERVIDOR, confs_comuns.PORTA))

# Mostra um simbolo de prompt no cliente e faz a captura de mensagem ou
# comando para se enviar ao servidor
dados = input(confs_comuns.PROMPT["cmd1"])

###########################################################################
# Laco principal de interacao com o servidor
###########################################################################
#
# A partir da captura acima, envia a mensagem ou comando para o servidor
#
# Apos o envio, aguarda algum tipo de resposta do servidor para continuar
#
# Ao receber a resposta, a exibe na tela
#
# Entao obtem novos comandos ou mensagens para continuar a comunicacao
# com o servidor
#
# Quando o cliente (este) enviar o comando '0', acabara o laco e a
# conexao com o servidor sera fechada
###########################################################################
while dados.lower().strip() != '0':
    # Envia mensagem/comando para o servidor
    socket_tls.send(dados.encode())
    # Aguarda uma resposta para poder prosseguir
    dados = socket_tls.recv(1024).decode()

    print('*** Resposta do servidor: ' + dados)

    # Mostra um simbolo de prompt no cliente e faz a captura de mensagem ou
    # comando para se enviar ao servidor
    # De novo. Eh o incremento/passo indutivo para sair do laco
    dados = input(confs_comuns.PROMPT["cmd1"])

# Envia para o servidor a confirmação do encerramento
socket_tls.send(dados.encode())
# Aguarda o OK do servidor para encerrar em definitivo
dados = socket_tls.recv(1024).decode()

# Encerra a conexao com o servidor e finaliza
socket_tls.close()