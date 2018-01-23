#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
 * Copyright (C) 2018 FU Berlin
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
"""

from __future__ import absolute_import, print_function, unicode_literals

import json
import struct
import sys


def write_message_to_stdout(message):
    """
    Write message to stdout for extension, which called the native messaging host.
    Parameter 'message' is converted to a json string.
    WARNING: without using ports, only the first message works, further messages will be ignored

    Parameters
    ----------
    message: array_like
        Message to be sent, in form of a dictionary

    """
    json_message = json.dumps(message).encode('utf-8')

    # pack message length as 4 byte integer.
    message_length = struct.pack('i', len(json_message))

    # send the data
    sys.stdout.write(message_length)
    sys.stdout.write(json_message)
    sys.stdout.flush()


# https://chromium.googlesource.com/chromium/src/+/master/chrome/common/extensions/docs/examples/api/nativeMessaging/host/native-messaging-example-host
def read_message_from_stdin():
    """
    Read message from stdin sent by chrome extension

    Returns
    -------
    string
        Input text in form of a JSON string
    """

    # read the message length (first 4 bytes)
    message_length_bytes = sys.stdin.read(4)
    if len(message_length_bytes) == 0:
        sys.exit(0)

    # unpack message length as 4 byte integer
    message_length = struct.unpack('i', message_length_bytes)[0]

    # read the data (JSON object) of the message
    text = sys.stdin.read(message_length).decode('utf-8')

    return text