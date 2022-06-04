# ********************************************************************
#      File:    receiver.py
#      Author:  Sam Strachan / Huxley Barbee
#
#      Description:
#       This file contains the code which connects to the eStreamer
#       server, issues requests and does the minimum parsing required
#       to send binary messages on to the callback
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

import struct
import time
import definitions
from eventstream import EventStreamRequestMessage
from streaming import StreamingRequestMessage
from null import NullMessage
from settings import Settings


class Receiver(object):
    """
    Receiver opens a host connection and sends an Event Stream Request.
    It then handles responses with the provided callback
    """
# settings
    def __init__(self, connectionParam):
        self.connection = connectionParam

    def _ack(self):
        print("NullMessage")
        self.connection.request(NullMessage())

    def _requestStreamingInformation(self, responseMessage):
        offset = 0
        serviceId = 0
        gotService = False

        while offset < len(responseMessage['data']):
            weeBuffer = responseMessage['data'][offset:offset + 8]

            (serviceId, length) = struct.unpack('>LL', weeBuffer)

            if serviceId == definitions.MESSAGE_STREAMING_INFORMATION_REQUEST_SERVICE_ID:
                gotService = True
                break

            offset = offset + 8 + length

        if not gotService:
            raise Exception('No StreamingInformation service')

        serviceMessage = StreamingRequestMessage(self.settings)
        print('serviceMessage')
        print(serviceMessage.data)
        self.connection.request(serviceMessage)

    def _parseMessageBundle(self, messageBundle):

        offset = 8

        while offset < messageBundle['length']:

            (messageType, length) = struct.unpack('>LL', messageBundle['data'][offset:offset + 8])

            if messageType != definitions.MESSAGE_TYPE_EVENT_DATA:
                raise Exception(
                    'Bundle item expected MESSAGE_TYPE_EVENT_DATA but got: {0}'.format(messageType))

            message = {
                'version': 1,
                'messageType': messageType,
                'length': length
            }

            if length > 0:
                dataStart = offset + 8
                dataEnd = offset + 8 + length
                message['data'] = messageBundle['data'][dataStart: dataEnd]

            self._send(message)

            offset = offset + 8 + length

    def init(self):
        """
        One off initialisation
        """
        timestamp = 0
        flags = Settings.requestFlags()

        eventMessage = EventStreamRequestMessage(timestamp, flags)
        print('send first EventStreamRequestMessage')
        self.connection.request(eventMessage)

    # def _send(self, message):
    #     self.sequence += 1
    #     message['sequence'] = self.sequence
    #     self.callback(message)

    def next(self):
        """
        Call this to attempt to read from the connection. Keep calling it.
        In a loop
        """
        print('read bytes from connection')
        newMessage = self.connection.response()
        if newMessage['messageType'] == definitions.MESSAGE_TYPE_STREAMING_INFORMATION:
            print('requestStreamingInformation')
            self._requestStreamingInformation(newMessage)

        elif newMessage['messageType'] == definitions.MESSAGE_TYPE_MESSAGE_BUNDLE:
            print('Message bundle')

        elif newMessage['messageType'] == definitions.MESSAGE_TYPE_NULL:
            print('Got null message.')

        elif newMessage['messageType'] == definitions.MESSAGE_TYPE_EVENT_DATA:
            print('newMessage')

        elif newMessage['messageType'] == definitions.MESSAGE_TYPE_ERROR:
            raise Exception("Error Message")
        # time.sleep(1)
        self._ack()
