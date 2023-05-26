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
		' 7- MOSTRAR SIGILO\n',
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
# Funcao criptografar()
###############################################################################
# Parametro: uma string (data) e um inteiro (chave)
###############################################################################
# Retorno: uma string (data)
###############################################################################
#
# Criptografa a mensagem que sera enviada ao cliente atraves da string
# 'data' usando primeiro a cifra de Cesar, depois com a chave publica do
# cliente e com # mais uma rodada da cifra de Cesar. Retorna o resultado,
# que eh uma string com o dado criptografado que se deseja enviar
#
# Esta funcao eh destinada para uso em todos os locais em que se quer enviar
# uma mensagem a um cliente
###############################################################################
def criptografar (data, chave):
	data = confs_comuns.cripto_rot13(data)
	data = confs_comuns.cripto_chave_assim(data, chave)
	data = confs_comuns.cripto_rot13(data)
	return data



###############################################################################
# PROGRAMA PRINCIPAL
###############################################################################
# Dicionario de exemplo que serve como base de dados inicial para as
# acoes de interacao entre cliente e servidor
# Fonte: https://docs.python.org/3/tutorial/datastructures.html#dictionaries
db = dict(ark04="Alexander Robert Kutzke", bcr04="Bruno César Ribas",
	dksy04="Danilo Kiyoshi Simizu Yorinori", jos04="Josiney de Souza",
	leg04="Leonardo Gomes", lhal04="Luís Henrique Alves Lourenço",
	rums04="Rubens Massayuki Suguimoto", sau04="Sérgio Akira Utime")

# Criacao de um socket
# AF_INET: para se usar IPv4
# SOCK_STREAM: para se usar TCP
socket_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
contexto = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
contexto.load_cert_chain(certfile="cert-rsa.pem", keyfile="id_rsa")

# Associa o endereco do servidor e a porta de uso com o socket
socket_s.bind((confs_comuns.END_SERVIDOR, confs_comuns.PORTA))

# Coloca o servidor em modo de escuta por conexoes
socket_s.listen()

# Depois de estar em modo de escuta, aceita as conexoes de clientes
conexao, end_cliente = socket_s.accept()
# Encapsula a conexao existente com TLS
socket_tls = contexto.wrap_socket(conexao, server_side=True)

# Mostra que um cliente se conectou e exibe seu endereco e porta contidos
# na variavel "end_cliente"
print(confs_comuns.MSG["clientecon"], end_cliente)

while True:
	# Recebe os dados da comunicacao com o cliente
	# Tem como limite 1024 B (1 kB) para o pacote de dados
	dados = socket_tls.recv(1024).decode()

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
	if (dados == "1"):
		dados = "Que chave inserir? "
		socket_tls.send(dados.encode())
		dados = socket_tls.recv(1024).decode()
		chave = dados
		if (chave not in db):
			dados = "Qual será o valor? "
			socket_tls.send(dados.encode())
			dados = socket_tls.recv(1024).decode()
			valor= dados
			db[chave] = valor
			dados = "### OPERAÇÃO REALIZADA COM SUCESSO ###\n"
		else:
			dados = "### CHAVE JÁ EXISTE ###"



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
	elif (dados == "2"):
		dados = "Que valor consultar? "
		socket_tls.send(dados.encode())
		dados = socket_tls.recv(1024).decode()
		if (dados not in db):
			dados = "### NÃO ENCONTRADO ###"
		else:
			dados = db[dados]



	#######################################################################
	# Opcao 3: Consultar todos os itens (R do CRUD)
	#######################################################################
	#
	# Nesta opcao, faz uma varredura pela base de dados e cria uma
	#
	# string com todos os registros de chave-valor cadastrados,
	# retornando-a para o cliente
	#######################################################################
	elif (dados == "3"):
		dados = envia_todo_banco(db)



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
	elif (dados == "4"):
		dados = "Que valor atualizar? "
		socket_tls.send(dados.encode())
		dados = socket_tls.recv(1024).decode()
		chave = dados
		if (chave not in db):
			dados = "### NÃO ENCONTRADO ###"
		else:
			dados = "Qual será o novo valor? "
			socket_tls.send(dados.encode())
			dados = socket_tls.recv(1024).decode()
			valor= dados
			db[chave] = valor
			dados = "### OPERAÇÃO REALIZADA COM SUCESSO ###\n"



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
	elif (dados == "5"):
		dados = "Que valor apagar? "
		socket_tls.send(dados.encode())
		dados = socket_tls.recv(1024).decode()
		chave = dados
		if (chave not in db):
			dados = "### NÃO ENCONTRADO ###"
		else:
			del db[chave]
			dados = "### OPERAÇÃO REALIZADA COM SUCESSO ###\n"



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
	elif (dados == "6"):
		dados = "Tem certeza? "
		socket_tls.send(dados.encode())
		dados = socket_tls.recv(1024).decode()
		dados = dados.lower()
		if (dados == "s" or dados == 'sim' or dados == 'si' or dados == 'y'
						or dados == 'yes'):
			for chave in list(db):
				del db[chave]
			dados = "### OPERAÇÃO REALIZADA COM SUCESSO ###\n"
		else:
			dados = "### BASE INALTERADA ###"



	#######################################################################
	# Opcao 7: MOSTRAR SIGILO
	#######################################################################
	#
	# 
	#
	#######################################################################
	elif (dados == "7"):
		chave_pub_cliente = 401
		chave_priv_cliente = 601

		chave_pub_invasor = 191
		chave_priv_invasor = 911

		dados = envia_todo_banco(db)
		dados_crip = criptografar(dados, chave_pub_cliente)
		print("---> Simulando a criptografia antes do envio da mensagem para o cliente ...")
		print("|-----> Criptografa usando a chave publica do cliente ...")
		print("|-----> (0) Mensagem criptografada:\n", dados_crip)
		input()

		print("---> Simulando o cliente descriptgrafando a mensagem - rodada 1 ...")
		sem_rot13 = confs_comuns.descripto_rot13(dados_crip)
		print("|-----> (1) Mensagem descriptografada com ROT13:\n", sem_rot13)
		input()

		print("---> Simulando o cliente descriptografando a mensagem - rodada 2 ...")
		cifra = confs_comuns.descripto_chave_assim(sem_rot13, chave_pub_invasor)
		print("|-----> (2) Mensagem descriptografada com chave pub invasor (", chave_pub_invasor, "):\n", cifra)
		input()

		cifra = confs_comuns.descripto_chave_assim(sem_rot13, chave_pub_cliente)
		print("|-----> (2) Mensagem descriptografada com chave publica cliente (", chave_pub_cliente, "):\n", cifra)
		input()

		cifra = confs_comuns.descripto_chave_assim(sem_rot13, chave_priv_invasor)
		print("|-----> (2) Mensagem descriptografada com chave priv invasor (", chave_priv_invasor, "):\n", cifra)
		input()

		cifra = confs_comuns.descripto_chave_assim(sem_rot13, chave_priv_cliente)
		print("|-----> (2) Mensagem descriptografada com chave privada cliente (", chave_priv_cliente, "):\n", cifra)
		input()

		print("---> Simulando o cliente descriptografando a mensagem - rodada 3 ...")
		cifra = confs_comuns.descripto_rot13(cifra)
		print("|-----> (3) Mensagem descriptografada com ROT13:\n", cifra)
		print("###############################################################################")
		print("---> Simulando a alteração da mensagem ...")
		input()

		print("---> Simulando o cliente descriptgrafando a mensagem - rodada 1 ...")
		sem_rot13 = confs_comuns.descripto_rot13(dados_crip)
		print("|-----> (1) Mensagem descriptografada com ROT13:\n", sem_rot13)
		input()

		print("|-----> (2) Mensagem sendo alterada...")
		sem_rot13 = confs_comuns.alterar(sem_rot13)
		# print("|-----> (2) Mensagem alterada nos indices ímpares:", sem_rot13)
		print("|-----> (3) Mensagem alterada nos indices 1,3,5,7,9:\n", sem_rot13, "\nExecução finalizaria aqui...")
		input()

		print("|-----> (4) mas, se continuasse, assim seria...")
		sem_rot13 = confs_comuns.descripto_rot13(dados_crip)
		sem_rot13 = confs_comuns.alterar(sem_rot13)
		cifra = confs_comuns.descripto_chave_assim(sem_rot13, chave_priv_cliente)
		print("|-----> (5) Mensagem descriptografada com chave privada cliente (", chave_priv_cliente, "):\n", cifra)
		input()

		print("---> Simulando o cliente descriptografando a mensagem - rodada 3 ...")
		cifra = confs_comuns.descripto_rot13(cifra)
		print("|-----> (6) Mensagem descriptografada com ROT13:\n", cifra)
		print("###############################################################################\n")



	#######################################################################
	# Opcao 0: Sair/Desconectar/Encerrar sessao
	#######################################################################
	#
	# Se nao vier mais dado algum do cliente, que significa seu desejo
	# de encerrar a conexao com este servidor, sai do loop infinito
	# para, na sequencia, encerrar sua parte da conexao
	#######################################################################
	elif (not dados):
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
		dados = envia_menu()



	# Envia uma string 'dados' para o cliente solicitando informacoes
	# adicionais, necessidade de confirmacao de algumas acoes, mensagens
	# de status (sucesso ou erro) e/ou o retorno das acoes requisitadas
	socket_tls.send(dados.encode())

# Encerra a conexao com o cliente
conexao.close()