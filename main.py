import ssl
import struct
from socket import socket

MESSAGE_REQUEST_PACKET_DATA = 1
MESSAGE_REQUEST_IMPACT = 1 << 5
MESSAGE_REQUEST_INTRUSION = 1 << 6
MESSAGE_REQUEST_METADATA = 1 << 20
MESSAGE_REQUEST_ARCHIVE_TIMESTAMPS = 1 << 23
MESSAGE_REQUEST_EVENT_EXTRA_DATA = 1 << 27
MESSAGE_REQUEST_POLICY = 1 << 29
MESSAGE_REQUEST_EXTENDED = 1 << 30

flagList = [MESSAGE_REQUEST_ARCHIVE_TIMESTAMPS, MESSAGE_REQUEST_EVENT_EXTRA_DATA,
            MESSAGE_REQUEST_EXTENDED, MESSAGE_REQUEST_IMPACT,
            MESSAGE_REQUEST_INTRUSION, MESSAGE_REQUEST_METADATA,
            MESSAGE_REQUEST_PACKET_DATA]
flags = 0
for flag in flagList:
    flags |= flag
print(flags)

buf = struct.pack('>HHLLL', *[1, 2, 8, 0, flags])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket = ssl.wrap_socket(
            sock,
            keyfile=r'/home/loft/EnergoAtomEncore/10.250.102.84-8302_pkcs.key',
            certfile=r'/home/loft/EnergoAtomEncore/10.250.102.84-8302_pkcs.cert',
            do_handshake_on_connect=True,
            ssl_version=ssl.PROTOCOL_TLSv1_2)


socket.settimeout(10)
socket.connect(('10.250.102.84', 8302))
socket.send(buf)
response = socket.recv(8)
print(response)