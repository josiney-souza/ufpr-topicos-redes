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
