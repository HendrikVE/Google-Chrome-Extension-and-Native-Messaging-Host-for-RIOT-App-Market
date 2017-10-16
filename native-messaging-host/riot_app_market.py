#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import base64
import json
import logging
import os
import struct
import sys
import tarfile
from subprocess import Popen

import common


def main():

    json_message = json.loads(get_message_from_stdin())

    try:
        # just testing connectivity
        if json_message["native_messaging_host_accessible"]:
            return
    except Exception as e:
        pass

    output_file_content = base64.b64decode(json_message["output_file"])
    output_file_extension = json_message["output_file_extension"]

    output_archive_content = base64.b64decode(json_message["output_archive"])
    output_archive_extension = json_message["output_archive_extension"]

    board = json_message["board"]
    application_name = json_message["application_name"]

    try:
        temporary_directory = os.path.join("tmp", application_name)
        common.create_directories(temporary_directory)

        archive_file_path = os.path.join(temporary_directory, application_name + "." + output_archive_extension)

        with open(archive_file_path, "wb") as archive:
            archive.write(output_archive_content)

        dest_path = os.path.join(temporary_directory, application_name)
        common.create_directories(dest_path)

        tar = tarfile.open(archive_file_path, "r:gz")
        for tarinfo in tar:
            tar.extract(tarinfo, dest_path)

        tar.close()

        path_to_makefile = os.path.join(dest_path, "generated_by_riotam", application_name)
        Popen(["x-terminal-emulator", "-e", "./flash {0} {1}".format(board, path_to_makefile)])

        #rmtree(temporary_directory)

    except Exception as e:
        logging.error(str(e), exc_info=True)


# https://chromium.googlesource.com/chromium/src/+/master/chrome/common/extensions/docs/examples/api/nativeMessaging/host/native-messaging-example-host
def get_message_from_stdin():
    """
    Read message from stdin sent by chrome extension

    Returns
    -------
    string
        Input text in form of a JSON string
    """

    # Read the message length (first 4 bytes).
    text_length_bytes = sys.stdin.read(4)
    if len(text_length_bytes) == 0:
        sys.exit(0)

    # Unpack message length as 4 byte integer.
    text_length = struct.unpack('i', text_length_bytes)[0]

    # Read the text (JSON object) of the message.
    text = sys.stdin.read(text_length).decode("utf-8")

    return text


if __name__ == "__main__":

    logging.basicConfig(filename="log/riot_app_market_log.txt", format="%(asctime)s [%(levelname)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)

    try:
        main()

    except Exception as e:
        logging.error(str(e), exc_info=True)
