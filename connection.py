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
import struct
import time
import definitions


class Connection(object):
    """
    Connection manages the connection to the remote host as well as
    sending and receiving messages
    """

    def __init__(self, socketParam):
        self.firstReceiveTime = None
        self.lastReceiveTime = None
        self.socket = socketParam

    def connect(self):
        """
        Opens a secure connection to the remote host
        """

        host = '10.250.102.84'
        port = 8302
        self.socket.connect((host, port))

        self.socket.settimeout(10)

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

    def sendBuf(self, buf):
        self.socket.send(buf)

    def __read(self, want):
        """Read and return 'want' bytes from the network"""
        dataBuffer = b''  # py3edit
        start = time.time()
        lastGot = 0
        got = 0

        while want > 0:
            try:
                print("try to recv new bytes")
                peekBytes = self.socket.recv(want)
                got = len(peekBytes)
                if got == 0:
                    # Connection closed.
                    raise Exception('Connection closed')

                dataBuffer += peekBytes
                want = want - got

            except:
                print('socket error in __read')
                duration = time.time() - start

                if got > lastGot:
                    # If we received data, then reset our time counter
                    lastGot = got
                    start = time.time()

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
