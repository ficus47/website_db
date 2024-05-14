import socket as sk

s = sk.gethostbyname(sk.gethostname())
sock = sk.socket()
sock.bind((s, 1024))

sock.close()
