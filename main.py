from connection import Connection
from receiver import Receiver

connection = Connection()
receiver = Receiver(connection)
while True:
    receiver.next()
