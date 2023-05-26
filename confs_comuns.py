# Endereco do servidor (deve ser string)
END_SERVIDOR = "127.0.0.1"

# Porta de comunicacao TCP que o servidor usa (deve ser inteiro)
PORTA = 8003

# Prompts de interacao
PROMPT = [ "#", "$", ">", "***", "###", "--->", "|----->"]

# Mensagens de retorno do servidor para o cliente
RETORNOS = dict ( ack="### MENSAGEM RECEBIDA ###",
	ok="### OPERAÇÃO REALIZADA COM SUCESSO ###",
	jaexiste="### CHAVE JÁ EXISTE ###",
	naoenc="### NÃO ENCONTRADO ###",
	inalt="### BASE INALTERADA ###" )

# Mensagens de exibicao no proprio servidor
MSG = dict ( clientecon="*** Cliente conectado:",
	docliente="*** Recebido do cliente:",
	fim="*** Encerrando o servidor" )



###############################################################################
# Funcao cripto_chave_assim()
###############################################################################
# Parametro: uma string (dados) e um inteiro (chave)
###############################################################################
# Retorno: uma string (str_cripto_chave_assim)
###############################################################################
#
# A partir de uma string 'dados', que representa os dados que serão
# transmitidos, e de um inteiro 'chave', que representa uma chave publica ou
# privada, faz um computo para criptografar a mensagem em 'dados'
#
# Para criptografar, para cada caractere contido na string 'dados' (o 'pos',
# de posicao da string), se obtem seu correspondente em inteiro de acordo
# com a tabela ASCII; depois se multiplica o valor obtido pela chave
# (privada, por exemplo) e se guarda o modulo da divisao por 1000
#
# A princípio, pensou-se na tabela ASCII tradicional, de 7 bits (caracteres
# de 0 a 127). Mesmo se for considerar caracteres acentuados graficamente
# (uma tabela ASCII estendida, de 8 bits/1 byte, caracteres de 0 a 255),
# cabem no limite do modulo de 1000
#
# O numero inteiro do caractere na tabela ASCII eh entao transformado em
# caractere/string. Também se calcula um codigo verificador de dois digitos
# para o numero calculado com a aritmetica de multiplicacao modular. O
# codigo verificador eh calculado considerando a soma dos valores do numero
#
# Como serao enviados apenas numeros para o destino, entre o numero em si
# bem como entre o digito verificador, para se separar cada caractere,
# usa-se um espaco em branco; que eh retirado na descriptografia. A proxima
# rodada de calculos tambem considera espacos em branco como separador
#
# Por fim, retira-se o espaco em branco extra da ultima iteracao e retorna a
# string criptografada
###############################################################################
def cripto_chave_assim (dados, chave):
	str_cripto_chave_assim = ""
	for pos in dados:
		codif = ord(pos)
		codif = (codif * chave) % 1000

		codif = str(codif)
		if (len(codif) == 1):
			verificador = codif
		elif (len(codif) == 2):
			verificador = int(codif[0]) + int(codif[1])
		elif (len(codif) == 3):
			verificador = int(codif[0]) + int(codif[1]) + int(codif[2])
		verificador = str(verificador)

		str_cripto_chave_assim = str_cripto_chave_assim + codif + " " + verificador + " "
	return str_cripto_chave_assim[:-1]



###############################################################################
# Funcao descripto_chave_assim()
###############################################################################
# Parametro: uma string (dados) e um inteiro (chave)
###############################################################################
# Retorno: uma string (str_descripto_chave_assim)
###############################################################################
#
# A partir de uma string 'dados', que representa os dados que serão
# transmitidos, e de um inteiro 'chave', que representa uma chave publica ou
# privada, faz a descriptografia (o computo para descriptografar a mensagem
# anteriormente criptografada com cripto_chave_assim() )
#
# Para descriptografar, como entre cada representacao inteira do caractere
# e do seu codigo verificado (que estao transformados em caractere/string)
# ha um espaco em branco inserido na criptografia, faz-se uma quebra da
# string recebida a partir de espaços em branco com a funcao split(). Isso
# resulta em uma lista que contem apenas os numeros que representam cada
# caractere da string original e seus codigos verificadores, nessa ordem
#
# Assim, eh possivel iterar sobre a lista de duas em duas posicoes. Entao
# se calcula um novo codigo verificador nesta funcao para que seja possivel
# compara-lo ao codigo verificador recebido externamente
#
# Se a string recebida nao tiver sido alterada ou corrompida, os codigos
# verificadores serao iguais. Nessa situacao, para cada numero representado
# como um caractere/string, transforma-o novamente em inteiro. Apos, se
# se multiplica o valor obtido pela chave (publica, por exemplo) e se
# guarda o modulo da divisao por 1000 (inverso multiplicativo modular). A
# partir desse numero, que agora eh um inteiro que representa o caractere
# descriptografado, transforma-o em caractere e se reconstroi a string
# original
#
# Se a verificacao do codigo verificador apontar inconsistencia, exibe uma
# mensagem informando isso e continua com o processo de descriptografia.
# Inicialmente, caso haja corrompimento da string recebida, se adiciona um
# valor a lista de dados da iteracao pois, para que este processo ocorra com
# sucesso, eh necessario haver uma quantidade par de itens (1 'caractere' e
# 1 codigo verificador)
###############################################################################
def descripto_chave_assim (dados, chave):
	dados_recebidos = dados.split()

	if (len(dados_recebidos) % 2 == 1):
		print("=== Tamanho:", len(dados_recebidos), "===")
		dados_recebidos.append("0")

	pos = 0
	str_descripto_chave_assim = ""
	while (pos < len(dados_recebidos)):
		num = dados_recebidos[pos]
		verificador = str(dados_recebidos[pos+1])

		if (len(num) == 1):
			nverificador = num
		elif (len(num) == 2):
			nverificador = int(num[0]) + int(num[1])
		elif (len(num) == 3):
			nverificador = int(num[0]) + int(num[1]) + int(num[2])
		nverificador = str(nverificador)

		codif = int(num)
		codif = (codif * chave) % 1000
		str_descripto_chave_assim = str_descripto_chave_assim + chr(codif)
		if (nverificador != verificador):
			print("=== ERRO NA VERIFICAÇÃO ===")

		pos = pos + 2

	return str_descripto_chave_assim
