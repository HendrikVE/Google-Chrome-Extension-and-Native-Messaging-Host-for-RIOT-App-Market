#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
 * Copyright (C) 2018 Hendrik van Essen and FU Berlin
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
"""

from __future__ import absolute_import, print_function, unicode_literals

import base64
import errno
import json
import logging
import os
import tarfile
import time
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from base64 import b64decode
from shutil import rmtree
from subprocess import Popen
import sys

from util import io
import config

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
LOGFILE = os.path.join(CUR_DIR, 'log', 'rapstore_nmh_log.txt')
PUBLIC_KEY_FILE = os.path.join(CUR_DIR, 'website.pub')

FIREFOX_EXTENSION_ID = 'rapstore.browser-integration@riot-apps.net'

CHROME_EXTENSION_ID = 'dlbaedkcgjohebkgillljbggndicfoej'
CHROME_EXTENSION_ID_DEVELOPMENT = 'omfbdeblphficlecofpbkdcchnghnkhc'


def test_connection_native_messaging_host(message, development):

    # print repsonse for callback within background script
    response = {'success': True}
    io.write_message_to_stdout(response)


def start_flash_process(message, development):

    # unwrap message from extension
    message_from_website = message['message']

    verified = verify_message(PUBLIC_KEY_FILE, message_from_website['message'],
                              b64decode(message_from_website['signature']))

    if not verified:
        # maybe unauthorized access via extension, so ignore
        logging.warning('unauthorized access denied')
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

        path_to_makefile = os.path.join(dest_path, 'generated_by_rapstore', application_name)

        # open standard terminal and execute shell script 'flash'
        file_to_look_at = os.path.join(CUR_DIR, '.terminal_finished_for_' + application_name)

        inner_command = './flash {0} {1} {2} && touch {3}'.format(board, path_to_makefile, int(development),
                                                              file_to_look_at.replace(' ', '\ '))

        Popen(['x-terminal-emulator', '-e', 'bash -c "{}"'.format(inner_command)])

        while not os.path.exists(file_to_look_at):
            time.sleep(1)

        os.remove(file_to_look_at)
        rmtree(temporary_directory)

    except Exception as e:
        logging.error(str(e), exc_info=True)


def main(calling_extension):

    development = False

    if CHROME_EXTENSION_ID_DEVELOPMENT in calling_extension:
        development = True

    action_dict = {
        'rapstore_test_connection_native_messaging_host': test_connection_native_messaging_host,
        'rapstore_install_image': start_flash_process,
    }

    message = io.read_message_from_stdin()
    message_from_extension = json.loads(message)

    action_key = message_from_extension['action']
    function_for_action = action_dict.get(action_key)

    if function_for_action is None:
        logging.error('missing field "action"')

    else:
        function_for_action(message_from_extension, development)


def verify_message(public_key, message, signature):

    pub_key = open(public_key, 'r').read()
    rsakey = RSA.importKey(pub_key)
    signer = PKCS1_v1_5.new(rsakey)
    digest = SHA256.new()
    digest.update(message)

    return signer.verify(digest, signature)


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
        # firefox calls nmh with 3 arguments, chrome only with 2. identify the last argument as calling extension id
        calling_extension_id = sys.argv[-1]

        main(calling_extension_id)

    except Exception as e:
        logging.error(str(e), exc_info=True)
