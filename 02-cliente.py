# Josiney de Souza
# 02-cliente.py
#
# Trabalho 2 do componente curricular Topicos em Redes de Computadores
# (INFO-7065) do Programa de Pos-Graduacao em Informatica (40001016034P5)
# da Universidade Federal do Parana (UFPR)
#
# Professor: Elias Procopio Duarte Junior
# Maio de 2023
#
# Base do codigo: https://www.digitalocean.com/community/tutorials/python-socket-programming-server-client
# Acesso em 04/05/2023



# Adicao do modulo socket para conseguir realizar a conexao cliente-servidor
import socket

###############################################################################
# Funcao principal
###############################################################################
def client_program():
    # https://pt.khanacademy.org/computing/computer-science/cryptography/modarithmetic/a/modular-inverses
    chave_publica = 401
    chave_privada = 601

    # Obtem a identificacao/endereco do servidor (este)
    host = socket.gethostname()
    # Indica a porta que o servidor ficara escutando as conexoes
    port = 5000

    # Cria uma instancia do socket
    client_socket = socket.socket()
    # Tenta se conectar ao servidor usando o endereco e porta definidos
    client_socket.connect((host, port))

    # Mostra um simbolo de prompt no cliente e faz a captura de mensagem ou
    # comando para se enviar ao servidor
    message = input(" -> ")

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
    while message.lower().strip() != '0':
        # Envia mensagem/comando para o servidor
        client_socket.send(message.encode())
        # Aguarda uma resposta para poder prosseguir
        data = client_socket.recv(1024).decode()

        print('*** Resposta do servidor: ' + data)

        # Mostra um simbolo de prompt no cliente e faz a captura de mensagem ou
        # comando para se enviar ao servidor
        # De novo. Eh o incremento/passo indutivo para sair do laco
        message = input(" -> ")

    # Caso nao tenha mais o que trocar de mensagem, fecha sua parte da
    # conexao com o servidor
    client_socket.close()



###############################################################################
# Chamada da funcao que executada como principal
###############################################################################
if __name__ == '__main__':
    client_program()