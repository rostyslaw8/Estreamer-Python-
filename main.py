import ssl
from connection import Connection
from receiver import Receiver
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tlsVersion = ssl.PROTOCOL_TLSv1_2

sock = ssl.wrap_socket(
        sock,
        keyfile=r'/home/loft/EnergoAtomEncore/10.250.102.84-8302_pkcs.key',
        certfile=r'/home/loft/EnergoAtomEncore/10.250.102.84-8302_pkcs.cert',
        do_handshake_on_connect=True,
        ssl_version=tlsVersion.PROTOCOL_TLSv1_2)

sock.settimeout(10)
connection = Connection(sock)
connection.connect()
print('Connection succesfulle')
receiver = Receiver(connection)
receiver.init()
while True:
    receiver.next()
