def cripto_subs (data, chave):
    str_cripto_subs = ""
    for pos in data:
        codif = ord(pos)
        codif = (codif * chave) % 1000
        str_cripto_subs = str_cripto_subs + str(codif) + " "
    return str_cripto_subs[:-1]

def descripto_subs (data, chave):
    str_descripto_subs = ""
    for num in data.split():
        codif = int(num)
        codif = (codif * chave) % 1000
        str_descripto_subs = str_descripto_subs + chr(codif)
    return str_descripto_subs
