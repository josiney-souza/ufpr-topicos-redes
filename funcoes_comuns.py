###############################################################################
# Funcao cripto_chave_assim()
###############################################################################
# Parametro: uma string (data) e um inteiro (chave)
###############################################################################
# Retorno: uma string (str_cripto_chave_assim)
###############################################################################
#
# A partir de uma string 'data', que representa os dados que serão
# transmitidos, e de um inteiro 'chave', que representa uma chave publica ou
# privada, faz um computo para criptografar a mensagem em 'data'
#
# Para criptografar, para cada caractere contido na string 'data' (o 'pos',
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
# caractere/string. Como serao enviados apenas numeros para o destino, para
# se separar cada caractere, usa-se um espaco em branco; que eh retirado na
# descriptografia.
#
# Por fim, retira-se o espaco em branco extra da ultima iteracao e retorna a
# string criptografada
###############################################################################
def cripto_chave_assim (data, chave):
    str_cripto_chave_assim = ""
    for pos in data:
        codif = ord(pos)
        codif = (codif * chave) % 1000
        str_cripto_chave_assim = str_cripto_chave_assim + str(codif) + " "
    return str_cripto_chave_assim[:-1]



###############################################################################
# Funcao descripto_chave_assim()
###############################################################################
# Parametro: uma string (data) e um inteiro (chave)
###############################################################################
# Retorno: uma string (str_descripto_chave_assim)
###############################################################################
#
# A partir de uma string 'data', que representa os dados que serão
# transmitidos, e de um inteiro 'chave', que representa uma chave publica ou
# privada, faz a descriptografia (o computo para descriptografar a mensagem
# anteriormente criptografada com cripto_chave_assim()
#
# Para descriptografar, como entre cada representacao inteira do caractere
# (que esta transformado em caractere/string) ha um espaco em branco
# inserido na criptografia, faz-se uma quebra da string a partir de espaços
# em branco com a funcao split(). Isso resulta em uma lista que contem
# apenas os numeros que representam as strings
#
# Assim, eh possivel iterar sobre a lista e, para cada numero representado
# como um caractere/string, transforma-o novamente em inteiro. Apos, se
# se multiplica o valor obtido pela chave (publica, por exemplo) e se
# guarda o modulo da divisao por 1000 (inverso multiplicativo modular)
#
# A partir desse numero, que agora eh um inteiro que representa o caractere
# descriptografado, transforma-o em caractere e se reconstroi a string
# original e a retorna
###############################################################################
def descripto_chave_assim (data, chave):
    str_descripto_chave_assim = ""
    for num in data.split():
        codif = int(num)
        codif = (codif * chave) % 1000
        str_descripto_chave_assim = str_descripto_chave_assim + chr(codif)
    return str_descripto_chave_assim



###############################################################################
# Funcao cripto_rot13()
###############################################################################
# Parametro: uma string (data)
###############################################################################
# Retorno: uma string (str_cripto_rot13)
###############################################################################
#
# A partir do dados que serão transmitidos, representado pela string 'data',
# criptografa a mensagem usado a cifra de Cesar (ROT13)
#
# A criptografia dos dados ocorre para cada caractere existente na string a
# ser enviada, obtendo seu numero inteiro correspondente ao caractere da
# tabela ASCII extendida (como no exemplo da imagem do link abaixo
# https://qph.cf2.quoracdn.net/main-qimg-00fcff66ae3d83dd690135cc77ec0931-lq
# Acesso em 10/05/2023), adiciona-se 13 a esse inteiro e se obtem o modulo
# da divisao por 255 (para se obter numeros de 0 a 255 - maximo da tabela)
#
# Como se deseja apenas os caracteres imprimiveis, adiciona-se 32 ao
# resultado se esse for abaixo de 32. Com o numero final obtido, constroi-se
# a string final com o caractere correspondente apos a rotacao
#
# OBS.: diferente da codificacao encode(string, 'rot13') do modulo "codecs"
# em Python (como em https://blog.finxter.com/how-to-use-rot13-in-python/,
# acesso em 05/05/2023), esta funcao faz a rotacao de qualquer caractere
# imprimivel e nao apenas dos textos alfanumericos simples da tabela ASCII
# padrao
###############################################################################
def cripto_rot13 (data):
    str_cripto_rot13 = ""
    for pos in data:
        rot13 = ord(pos)
        rot13 = (rot13 + 13) % 256
        if (rot13 < 32):
            rot13 = rot13 + 32
        str_cripto_rot13 = str_cripto_rot13 + chr(rot13)
    return str_cripto_rot13



###############################################################################
# Funcao descripto_rot13()
###############################################################################
# Parametro: uma string (data)
###############################################################################
# Retorno: uma string (str_descripto_rot13)
###############################################################################
#
# A partir do dados que serão transmitidos, representado pela string 'data',
# DEScriptografa a mensagem usado a cifra de Cesar (ROT13)
#
# A partir de cada caractere existente na string recebida, obtem um numero
# inteiro correspondente ao caractere da tabela ASCII extendida (como no
# exemplo da imagem do link abaixo
# https://qph.cf2.quoracdn.net/main-qimg-00fcff66ae3d83dd690135cc77ec0931-lq
# Acesso em 10/05/2023). Então, se esse numero for menor que 32+13, sendo 32
# o primeiro caractere imprimivel e 13 a chave da cifra, significa que o
# caractere original antes da codificacao estava no topo da tabela ASCII
# (exemplo, 250) e sofreu um "overflow" apos a operacao de modulo 256
#
# Se esse for o caso, faz o caminho inverso da criptografia: subtrai-se 32
# (valor usado para se chegar aos caracteres imprimiveis se abaixo de 32) e
# se adicionar 256 (para voltar ao valor original apos a rotacao/adicao da
# chave 13 durante a criptografia)
#
# Com o numero original apos a adicao da chave 13 na criptografia, apenas se
# retira o valor da chave 13 para retornar ao inteiro da sequencia original.
# A partir dai, constroi-se a string final e a retorna
#
# OBS.: diferente da codificacao encode(string, 'rot13') do modulo "codecs"
# em Python (como em https://blog.finxter.com/how-to-use-rot13-in-python/,
# acesso em 05/05/2023), esta funcao faz a rotacao de qualquer caractere
# imprimivel e nao apenas dos textos alfanumericos simples da tabela ASCII
# padrao
###############################################################################
def descripto_rot13 (data):
    str_descripto_rot13 = ""
    for pos in data:
        rot13 = ord(pos)
        if (rot13 < (32+13)):
            rot13 = rot13 - 32 + 256
        rot13 = rot13 - 13
        str_descripto_rot13 = str_descripto_rot13 + chr(rot13)
    return str_descripto_rot13
