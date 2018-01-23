#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
 * Copyright (C) 2017 Hendrik van Essen and FU Berlin
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
"""

from __future__ import absolute_import, print_function, unicode_literals

import base64
import json
import logging
import os
import struct
import sys
import tarfile
import time
from shutil import rmtree
from subprocess import Popen
import errno
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64decode

import config

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
LOGFILE = os.path.join(CUR_DIR, 'log', 'riot_app_market_log.txt')
PUBLIC_KEY_FILE = os.path.join(CUR_DIR, 'website.pub')


def main():

    message = read_message_from_stdin()
    message_from_extension = json.loads(message)

    # just testing connectivity
    if message_from_extension['action'] == 'test_connection_native_messaging_host':
        # print repsonse for callback within background script
        response = {'success': True}
        write_message_to_stdout(response)

        return

    # unwrap message from extension
    message_from_website = message_from_extension['message']

    verified = verify_message(PUBLIC_KEY_FILE, message_from_website['message'], b64decode(message_from_website['signature']))

    if not verified:
        # maybe unauthorized access via extension, so ignore
        logging.debug('unauthorized access denied')
        return

    # unwrap message from website
    message_from_backend = json.loads(message_from_website['message'])

    output_archive_content = base64.b64decode(message_from_backend['output_archive'])
    output_archive_extension = message_from_backend['output_archive_extension']

    board = message_from_backend['board']
    application_name = message_from_backend['application_name']

    try:
        temporary_directory = os.path.join('tmp', application_name)
        create_directories(temporary_directory)

        archive_file_path = os.path.join(temporary_directory, application_name + '.' + output_archive_extension)

        with open(archive_file_path, 'wb') as archive:
            archive.write(output_archive_content)

        dest_path = os.path.join(temporary_directory, application_name)
        create_directories(dest_path)

        tar = tarfile.open(archive_file_path, 'r:gz')
        for tarinfo in tar:
            tar.extract(tarinfo, dest_path)

        tar.close()

        path_to_makefile = os.path.join(dest_path, 'generated_by_riotam', application_name)

        #open standard terminal and execute shell script 'flash'
        file_to_look_at = os.path.join(CUR_DIR, '.terminal_finished_for_' + application_name)

        logging.debug(file_to_look_at)

        inner_command = './flash {0} {1} && touch {2}'.format(board, path_to_makefile, file_to_look_at.replace(' ', '\ '))
        Popen(['x-terminal-emulator', '-e', 'bash -c "{}"'.format(inner_command)])

        while not os.path.exists(file_to_look_at):
            time.sleep(1)

        os.remove(file_to_look_at)
        rmtree(temporary_directory)

    except Exception as e:
        logging.error(str(e), exc_info=True)


def verify_message(public_key, message, signature):

    pub_key = open(public_key, 'r').read()
    rsakey = RSA.importKey(pub_key)
    signer = PKCS1_v1_5.new(rsakey)
    digest = SHA256.new()
    digest.update(message)

    return signer.verify(digest, signature)


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


def create_directories(path):
    """
    Creates all directories on path

    Parameters
    ----------
    path: string
        Path to create

    Raises
    -------
    OSError
        Something fails creating directories, except directoy already exist

    """
    try:
        os.makedirs(path)

    except OSError as e:

        if e.errno != errno.EEXIST:
            raise


if __name__ == '__main__':

    logging.basicConfig(filename=LOGFILE, format=config.LOGGING_FORMAT, datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)

    try:
        main()

    except Exception as e:
        logging.error(str(e), exc_info=True)
