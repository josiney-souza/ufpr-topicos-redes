import socket


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Cliente conectado: " + str(address))

    db = dict(ark04=1, bcr04=2, dksy04=3, jos04=4, leg04=5, lhal04=6, rums04=7, sau04=8)
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()

        if (str(data) == "1"):
            data = "Criar base dados"
        elif (str(data) == "2"):
            data = "Que valor consultar? "
            conn.send(data.encode())
            data = conn.recv(1024).decode()
            if (str(data) not in db):
                data = "### NÃO ENCONTRADO ###"
            else:
                data = str(db[str(data)])
        elif (str(data) == "3"):
            data = envia_todo_banco(db)
        elif (str(data) == "4"):
            data = "Atualizar um valor"
        elif (str(data) == "5"):
            data = "Apagar um valor"
        elif (str(data) == "6"):
            data = "Apagar base de dados"
        elif (str(data) == "7"):
            data = "Implementar SIGILO"
        elif (str(data) == "8"):
            data = "Implementar INTEGRIDADE"
        elif (str(data) == "9"):
            data = "Implementar AUTENTICIDADE"
        elif (not data):
            break
        else:
            data = envia_menu()

        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection

def envia_menu():
    opcoes = [ '\nOpções disponíveis:\n',
        ' 1- Criar base de dados\n',
        ' 2- Consultar um valor\n',
        ' 3- Consultar todos os valores\n',
        ' 4- Atualizar um valor\n',
        ' 5- Apagar um valor\n',
        ' 6- Apagar base de dados\n',
        ' 7- Mostrar que tem SIGILO\n',
        ' 8- Mostrar que tem INTEGRIDADE\n',
        ' 9- Mostrar que tem AUTENTICIDADE\n',
        ' ?- Ajuda\n',
        ' 0- Desconectar'
    ]
    str_envio = ""
    for opcao in opcoes:
        str_envio = str_envio + opcao
    return str_envio

def envia_todo_banco (db):
    str_unica = "\nCHAVE : VALOR\n"
    for chave in db:
        valor=db[chave];
        str_unica = str_unica + str(chave) + ":" + str(valor) + '\n'
    return str_unica

if __name__ == '__main__':
    server_program()