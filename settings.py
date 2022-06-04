# ********************************************************************
#      File:    settings.py
#      Author:  Sam Strachan
#
#      Description:
#       Settings is the programmatic representation of whatever is
#       in the configuration file. It provides context to all processes
#       within the service
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
import definitions


class Settings(object):

    @staticmethod
    def requestFlags():
        """Turns config settings into request flags"""
        flagList = []

        if True:
            flagList.append(definitions.MESSAGE_REQUEST_PACKET_DATA)

        if True:
            flagList.append(definitions.MESSAGE_REQUEST_IMPACT)

        if True:
            flagList.append(definitions.MESSAGE_REQUEST_INTRUSION)

        if True:
            flagList.append(definitions.MESSAGE_REQUEST_METADATA)

        if True:
            flagList.append(definitions.MESSAGE_REQUEST_ARCHIVE_TIMESTAMPS)

        if True:
            flagList.append(definitions.MESSAGE_REQUEST_EVENT_EXTRA_DATA)

        if True:
            flagList.append(definitions.MESSAGE_REQUEST_EXTENDED)

        flags = 0

        for flag in flagList:
            flags |= flag

        return flags
