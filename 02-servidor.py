# Josiney de Souza
# 02-servidor.py
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
#
# Fork: https://www.geeksforgeeks.org/python-os-fork-method/
# Acesso em 05/05/2023
#
# Thread opcao 1: https://realpython.com/intro-to-python-threading/
# Thread opcao 2: https://superfastpython.com/threading-in-python/
# Acesso em 05/05/2023



# Adicao do modulo socket para conseguir realizar a conexao cliente-servidor
import socket
# Adicao de um modulo de funcoes comuns ao cliente, servidor e invasor
import funcoes_comuns
# Adicao do modulo os para fazer fork()
#import os
# Adicao do modulo threading para criar Threads
import threading
# Adicao do modulo concurrent.futures para criar um pool de Threads
#import concurrent.futures

###############################################################################
# Funcao principal
###############################################################################
# Parametro: nao ha
###############################################################################
# Retorno: nao ha
###############################################################################
#
# Inicialmente, o servidor possui apenas a Thread principal e fica em loop
# infinito a espera de novas conexoes
#
# Quando uma nova conexao chega, se cria uma nova Thread para tratar
# especificamente dela, executando assim a funcao_thread()
###############################################################################
def server_program():
# Dicionario de exemplo que serve como base de dados inicial para as
    # acoes de interacao entre cliente e servidor
    db = dict(ark04=1, bcr04=2, dksy04=3, jos04=4, leg04=5, lhal04=6, rums04=7, sau04=8)

    # Variaveis para armazenar as chaves publicas dos clientes
    # Apenas as chaves publicas dos clientes sao armazenadas no servidor
    chave_pub_cliente = 401
    chave_pub_invasor = 191

    # Obtem a identificacao/endereco do servidor (este)
    host = socket.gethostname()
    # Indica a porta que o servidor ficara escutando as conexoes
    port = 5000

    # Cria uma instancia do socket
    server_socket = socket.socket()
    # Faz a correlacao entre o endereco e porta usados pelo servidor
    server_socket.bind((host, port))

    # Configura a quantidade de clientes que o servidor pode gerenciar
    # simultaneamente
    server_socket.listen(2)

    # Aceita novas conexoes de clientes
    while True:
        conn, address = server_socket.accept()

        # Tentativa de executar um fork() para as atividades de escutar
        # novas conexoes e de tratar as conexoes em dois tipos de processos
        # OBS.: nao eh viavel pois os processos filhos nao compartilham das
        #       variaveis do processo pai, tendo cada qual seu proprio
        #       contexto
        #pid = os.fork()
        #if (pid == 0):
        #    break

        # Apos uma nova conexao ser aceita, se cria uma thread para trata-la
        # OBS.: em 'target', indicar apenas o nome da funcao da thread
        #       quando se passa tambem os argumentos, a thread principal
        #       fica travada ate a thread filha terminar sua execucao
        #       Passar os argumentos via 'args'
        x = threading.Thread(target=funcao_thread, args=(conn, address, db, chave_pub_cliente, chave_pub_invasor))
        x.start()

        # Tentativa de executar um pool de threads para tratar do problema
        #with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        #    executor.map(funcao_thread(conn, address, db), i)



###############################################################################
# Funcao funcao_thread()
###############################################################################
# Parametro: uma conexao (conn), um endereco (address), um dicionario (db)
###############################################################################
# Retorno: nao ha
###############################################################################
#
# Esta funcao possui todo o codigo que uma thread de tratamento de conexao
# faz, ou seja, eh nesta funcao que se faz o CRUD da base de dados
#
# Executa-se uma desta funcao para cada thread criada para tratar as conexoes
# que chegam dos clientes
###############################################################################
def funcao_thread (conn, address, db, chave_pub_cliente, chave_pub_invasor):
    # Exibe uma mensagem para informar que cliente (IP e porta) se conectou
    print("Cliente conectado: " + str(address))

    while True:
        # Recebe os dados da comunicacao com o cliente
        # Tem como limite 1024 B (1 kB) para o pacote de dados
        data = conn.recv(1024).decode()
        data = descriptografar(data, chave_pub_cliente)

        #######################################################################
        # Opcao 1: Inserir um item (C do CRUD)
        #######################################################################
        #
        # Nesta opcao, insere um registro de chave-valor no dicionario que
        # representa a base de dados do programa
        #
        # Se a chave nao existir na base de dados, a adiciona
        #
        # Senao, informa que ja existe esse registro e NAO faz a operacao
        #
        # Nessa ultima situacao, se desejar sobrescrever o item, usar a
        # opcao de atualizacao (opcao/menu 4)
        #######################################################################
        if (data == "1"):
            data = "Que chave inserir? "
            conn.send(data.encode())
            data = conn.recv(1024).decode()
            data = descriptografar(data, chave_pub_cliente)
            chave = data
            if (chave not in db):
                data = "Qual será o valor? "
                conn.send(data.encode())
                data = conn.recv(1024).decode()
                data = descriptografar(data, chave_pub_cliente)
                valor= data
                db[chave] = valor
                data = "### OPERAÇÃO REALIZADA COM SUCESSO ###\n"
            else:
                data = "### CHAVE JÁ EXISTE ###"



        #######################################################################
        # Opcao 2: Consultar um item (R do CRUD)
        #######################################################################
        #
        # Nesta opcao, consulta se uma determinada chave existe na base de
        # dados armazenada no dicionario
        #
        # Se a chave nao existir na base de dados, informa para o cliente e
        # NAO faz qualquer consulta adicional
        #
        # Senao, busca pelo valor associado a chave no dicionario e retorna
        # o resultado para o cliente
        #######################################################################
        elif (data == "2"):
            data = "Que valor consultar? "
            conn.send(data.encode())
            data = conn.recv(1024).decode()
            data = descriptografar(data, chave_pub_cliente)
            if (data not in db):
                data = "### NÃO ENCONTRADO ###"
            else:
                data = db[data]



        #######################################################################
        # Opcao 3: Consultar todos os itens (R do CRUD)
        #######################################################################
        #
        # Nesta opcao, faz uma varredura pela base de dados e cria uma
        #
        # string com todos os registros de chave-valor cadastrados,
        # retornando-a para o cliente
        #######################################################################
        elif (data == "3"):
            data = envia_todo_banco(db)



        #######################################################################
        # Opcao 4: Atualizar um item (U do CRUD)
        #######################################################################
        #
        # Nesta opcao, consulta se uma determinada chave existe na base de
        # dados armazenada no dicionario
        #
        # Se a chave nao existir na base de dados, informa para o cliente e
        # NAO faz qualquer atualizacao
        #
        # Senao, obtem com o cliente o novo valor que deve ser atribuido a
        # chave escolhida e o atualiza no dicionario, informando o cliente
        #######################################################################
        elif (data == "4"):
            data = "Que valor atualizar? "
            conn.send(data.encode())
            data = conn.recv(1024).decode()
            data = descriptografar(data, chave_pub_cliente)
            chave = data
            if (chave not in db):
                data = "### NÃO ENCONTRADO ###"
            else:
                data = "Qual será o novo valor? "
                conn.send(data.encode())
                data = conn.recv(1024).decode()
                data = descriptografar(data, chave_pub_cliente)
                valor= data
                db[chave] = valor
                data = "### OPERAÇÃO REALIZADA COM SUCESSO ###\n"



        #######################################################################
        # Opcao 5: Apagar um item (D do CRUD)
        #######################################################################
        #
        # Nesta opcao, consulta se uma determinada chave existe na base de
        # dados armazenada no dicionario
        #
        # Se a chave nao existir na base de dados, informa para o cliente e
        # NAO faz qualquer remocao
        #
        # Senao, apaga a chave informada e, consequentemente, seu valor,
        # informando o cliente
        #######################################################################
        elif (data == "5"):
            data = "Que valor apagar? "
            conn.send(data.encode())
            data = conn.recv(1024).decode()
            data = descriptografar(data, chave_pub_cliente)
            chave = data
            if (chave not in db):
                data = "### NÃO ENCONTRADO ###"
            else:
                del db[chave]
                data = "### OPERAÇÃO REALIZADA COM SUCESSO ###\n"



        #######################################################################
        # Opcao 6: Apagar TODOS os itens (D do CRUD)
        #######################################################################
        #
        # Nesta opcao, confirma com o cliente se REALMENTE quer apagar tudo
        #
        # Se sim, procede com a remocao de item por item
        #
        # Senao, apenas informa que NADA foi alterado
        #######################################################################
        elif (data == "6"):
            data = "Tem certeza? "
            conn.send(data.encode())
            data = conn.recv(1024).decode()
            data = descriptografar(data, chave_pub_cliente)
            data = data.lower()
            if (data == "s" or data == 'sim' or data == 'si' or data == 'y'
                            or data == 'yes'):
                for chave in list(db):
                    del db[chave]
                data = "### OPERAÇÃO REALIZADA COM SUCESSO ###\n"
            else:
                data = "### BASE INALTERADA ###"



        #######################################################################
        # Opcao 7: SIGILO
        #######################################################################
        #
        # TO-DO
        #######################################################################
        elif (data == "7"):
            data = envia_todo_banco(db)
            data = criptografar(data, chave_pub_cliente)
            print("---> Mensagem criptografada:", data)
            input()

            data = funcoes_comuns.descripto_rot13(data)
            print("|-----> (1) Mensagem descriptografada com ROT13:", data)
            input()

            cifra = funcoes_comuns.descripto_chave_assim(data, chave_pub_invasor)
            print("|-----> (2) Mensagem descriptografada com chave invasor:", cifra)
            input()

            cifra = funcoes_comuns.descripto_chave_assim(data, chave_pub_cliente)
            print("|-----> (2) Mensagem descriptografada com chave publica:", cifra)
            input()

            cifra = data
            data = "[DEBUG] Qual sua chave privada? "
            conn.send(data.encode())
            data = conn.recv(1024).decode()
            data = descriptografar(data, chave_pub_cliente)
            data = int(data)

            data = funcoes_comuns.descripto_chave_assim(cifra, data)
            print("|-----> (2) Mensagem descriptografada com chave privada:", data)
            input()

            data = funcoes_comuns.descripto_rot13(data)
            print("|-----> (3) Mensagem descriptografada com ROT13:", data)
            print("###############################################################################")
            print()
            data = "### OPERAÇÃO REALIZADA COM SUCESSO ###\n"
        


        #######################################################################
        # Opcao 8: INTEGRIDADE
        #######################################################################
        #
        # TO-DO
        #######################################################################
        elif (data == "8"):
            data = "Implementar INTEGRIDADE"



        #######################################################################
        # Opcao 9: AUTENTICIDADE
        #######################################################################
        #
        # MODO DEBUG ALINHADO COM O SERVIDOR
        #
        # Antes de enviar a mensagem, criptografa com a cifra de Cesar,
        # depois com chave privada e novamente com a cifra de Cesar
        # No servidor, descriptografa com a cifra de Cesar, depois com a
        # chave publica e de novo com a cifra de Cesar
        # Como o servidor tem a chave publica, consegue descriptografar
        # Se tentar descriptografar com a chave publica do invasor, string
        # fica ilegivel
        #######################################################################
        elif (data == "9"):
            data = "Que mensagem quer enviar? "
            conn.send(data.encode())
            data = conn.recv(1024).decode()
            print("---> Mensagem criptografada:", data)
            data = funcoes_comuns.descripto_rot13(data)
            print("|-----> (1) Mensagem descriptografada com ROT13:", data)
            cifra = funcoes_comuns.descripto_chave_assim(data, chave_pub_invasor)
            print("|-----> (2) Mensagem descriptografada com chave invasor:", cifra)
            data = funcoes_comuns.descripto_chave_assim(data, chave_pub_cliente)
            print("|-----> (2) Mensagem descriptografada com chave publica:", data)
            data = funcoes_comuns.descripto_rot13(data)
            print("|-----> (3) Mensagem descriptografada com ROT13:", data)
            print()
            data = "### OPERAÇÃO REALIZADA COM SUCESSO ###\n"
        


        #######################################################################
        # Opcao 0: Sair/Desconectar/Encerrar sessao
        #######################################################################
        #
        # Se nao vier mais dado algum do cliente, que significa seu desejo
        # de encerrar a conexao com este servidor, sai do loop infinito
        # para, na sequencia, encerrar sua parte da conexao
        #######################################################################
        elif (not data):
            break



        #######################################################################
        # Opcao ?: Ajuda
        #######################################################################
        #
        # Se o usuario digitar qualquer opcao invalida, lhe sera enviado
        # uma string com todas as opcoes que sao reconhecidas por este
        # servidor
        # Este eh o caso default/padrao do menu
        #######################################################################
        else:
            data = envia_menu()

        # Envia uma string 'data' para o cliente solicitando informacoes
        # adicionais, necessidade de confirmacao de algumas acoes, mensagens
        # de status (sucesso ou erro) e/ou o retorno das acoes requisitadas
        conn.send(data.encode())

    # Como ultima tarefa do servidor, fecha sua parte da conexao com os clientes
    conn.close()



###############################################################################
# Funcao envia_menu()
###############################################################################
# Parametro: nao ha
###############################################################################
# Retorno: uma string (str_envio)
###############################################################################
#
# Cria uma string 'str_envio' com todas as opcoes disponiveis reconhecidas
# pelo servidor para que seja enviada ao cliente e este possa escolhar uma
# opcao de interacao
#
# Cada opcao possivel de atividades reconhecidas pelo servidor esta
# armazenada em uma lista
#
# Esta funcao eh usada pelo menu de interacao ? entre cliente e servidor
###############################################################################
def envia_menu():
    opcoes = [ '\nOpções disponíveis:\n',
        ' 1- [CRUD - C] Adicionar um registro\n',
        ' 2- [CRUD - R] Consultar um valor\n',
        ' 3- [CRUD - R] Consultar todos os valores\n',
        ' 4- [CRUD - U] Atualizar um valor\n',
        ' 5- [CRUD - D] Apagar um valor\n',
        ' 6- [CRUD - D] Apagar base de dados\n',
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



###############################################################################
# Funcao envia_todo_banco()
###############################################################################
# Parametro: um dicionario (db)
###############################################################################
# Retorno: uma string (str_unica)
###############################################################################
#
# Faz a varredura em um dicionario 'db' e monta uma string 'str_unica' com
# todos os pares de chave-valor contidos no dicionario (base de dados)
#
# Esta funcao eh usada pelo menu de interacao 3 entre cliente e servidor
###############################################################################
def envia_todo_banco (db):
    str_unica = "\nCHAVE : VALOR\n"
    for chave in db:
        valor=db[chave];
        str_unica = str_unica + str(chave) + ":" + str(valor) + '\n'
    return str_unica



###############################################################################
# Funcao descriptografar()
###############################################################################
# Parametro: uma string (data) e um inteiro (chave)
###############################################################################
# Retorno: uma string (data)
###############################################################################
#
# Descriptografa a mensagem recebida atraves da string 'data' usando
# primeiro a cifra de Cesar, depois com a chave publica do cliente e com
# mais uma rodada da cifra de Cesar. Retorna o resultado, que eh uma string
# com o dado originalmente enviado para este servidor
#
# Esta funcao eh usada em todos os locais em que se recebe uma mensagem de
# um cliente
###############################################################################
def descriptografar (data, chave):
    data = funcoes_comuns.descripto_rot13(data)
    data = funcoes_comuns.descripto_chave_assim(data, chave)
    data = funcoes_comuns.descripto_rot13(data)
    return data



def criptografar (data, chave):
    data = funcoes_comuns.cripto_rot13(data)
    data = funcoes_comuns.cripto_chave_assim(data, chave)
    data = funcoes_comuns.cripto_rot13(data)
    return data



###############################################################################
# Chamada da funcao que executada como principal
###############################################################################
if __name__ == '__main__':
    server_program()