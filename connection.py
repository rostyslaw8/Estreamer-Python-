# ********************************************************************
#      File:    connection.py
#      Author:  Sam Strachan / Huxley Barbee
#
#      Description:
#       Manages the connection to the eStreamer Server
#
#      Copyright (c) 2017 by Cisco Systems, Inc.
#
#       ALL RIGHTS RESERVED. THESE SOURCE FILES ARE THE SOLE PROPERTY
#       OF CISCO SYSTEMS, Inc. AND CONTAIN CONFIDENTIAL  AND PROPRIETARY
#       INFORMATION.  REPRODUCTION OR DUPLICATION BY ANY MEANS OF ANY
#       PORTION OF THIS SOFTWARE WITHOUT PRIOR WRITTEN CONSENT OF
#       CISCO SYSTEMS, Inc. IS STRICTLY PROHIBITED.
#
# *********************************************************************/

from __future__ import absolute_import
import datetime
import socket
import ssl
import struct
import time
import definitions


class Connection(object):
    """
    Connection manages the connection to the remote host as well as
    sending and receiving messages
    """

    def __init__(self):
        # self.settings = settings
        self.firstReceiveTime = None
        self.lastReceiveTime = None
        self.socket = None

    def connect(self):
        """
        Opens a secure connection to the remote host
        """
        host = '10.250.102.84'
        port = 8302

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Default TLS
        tlsVersion = ssl.PROTOCOL_TLSv1_2

        self.socket = ssl.wrap_socket(
            sock,
            keyfile=r'/home/loft/EnergoAtomEncore/10.250.102.84-8302_pkcs.key',
            certfile=r'/home/loft/EnergoAtomEncore/10.250.102.84-8302_pkcs.cert',
            do_handshake_on_connect=True,
            ssl_version=tlsVersion)

        self.socket.settimeout(self.settings.connectTimeout)
        self.socket.connect((host, port))
        self.socket.settimeout(1)

    def close(self):
        """closes the connection"""

        self.socket.close()

    def getFirstReceiveTime(self):
        """Returns the time when the first message was received this session"""
        return self.firstReceiveTime

    def getLastReceiveTime(self):
        """Returns the time when the last message was received this session"""
        return self.lastReceiveTime

    def request(self, message):
        """Issue a request"""
        buf = message.getWireData()

        self.socket.send(buf)

    def __read(self, want):
        """Read and return 'want' bytes from the network"""
        dataBuffer = b''  # py3edit
        start = time.time()
        lastGot = 0
        got = 0

        while want > 0:
            try:

                peekBytes = self.socket.recv(want)
                got = len(peekBytes)
                if got == 0:
                    # Connection closed.
                    raise Exception('Connection closed')

                dataBuffer += peekBytes
                want = want - got

            except socket.error:
                duration = time.time() - start

                if got > lastGot:
                    # If we received data, then reset our time counter
                    lastGot = got
                    start = time.time()

                if duration >= self.settings.responseTimeout:
                    raise Exception('Connection read timeout')

        return dataBuffer

    def response(self):
        """Returns the next response from the wire"""

        dataBuffer = self.__read(8)

        (version, messageType, length) = struct.unpack('>HHL', dataBuffer)

        message = {
            'version': version,
            'messageType': messageType,
            'length': length
        }

        if version != 1:
            raise Exception(definitions.STRING_CONNECTION_INVALID_HEADER.format(version, message))

        if version == 1 and messageType != 0:
            self.lastReceiveTime = datetime.datetime.now().now()

            if not self.firstReceiveTime:
                self.firstReceiveTime = self.lastReceiveTime

            message['data'] = self.__read(length)

            actualLength = len(message['data'])
            if length != actualLength:
                raise Exception('Expected length {0} but got {1}'.format(length, actualLength))

        return message
