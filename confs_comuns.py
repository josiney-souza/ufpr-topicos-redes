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