import socket as sk

s = sk.gethostbyname(sk.gethostname())
sock = sk.socket()
sock.connect(("127.0.0.1", 1025))

to_send = open("moi.mp4", "rb").read()
sock.send(to_send)
recv = sock.recv(32).decode()
print(recv)
