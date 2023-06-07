import requests

response=requests.get('https://localhost:5000', verify=False)

print(response)

# Base do codigo
# https://snyk.io/blog/implementing-tls-ssl-python/
# Acesso em: 10/05/2023
#
# Descobrindo como nao verificar o certificado por estar auto-assinado
# https://stackoverflow.com/questions/64911257/ssl-certificate-verify-failed-certificate-verify-failed-in-python
# Acesso em: 11/05/2023