import http.server
import ssl

httpd = http.server.HTTPServer(('localhost', 5000),
	http.server.SimpleHTTPRequestHandler)

httpd.socket = ssl.wrap_socket (httpd.socket,
	keyfile='../../.ssh/chave-ssl.pem',
	certfile='../../.ssh/certificado.pem',
	server_side=True,
	ssl_version=ssl.PROTOCOL_TLS)

httpd.serve_forever()

# Geracao de certificados e base do codigo
# https://snyk.io/blog/implementing-tls-ssl-python/
# Acesso em: 10/05/2023
#
# Descobrindo o problema de chave publica
# https://stackoverflow.com/questions/30109449/what-does-sslerror-ssl-pem-lib-ssl-c2532-mean-using-the-python-ssl-libr
# Acesso em: 11/05/2023
#
# Adicionando a chave publica
# https://anvileight.com/blog/posts/simple-python-http-server/
# Acesso em: 11/05/2023