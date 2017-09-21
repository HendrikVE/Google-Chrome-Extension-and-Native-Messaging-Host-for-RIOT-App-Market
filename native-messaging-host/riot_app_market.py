#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import base64
import errno
import json
import logging
import os
import struct
from subprocess import Popen, call
import sys
import tarfile
from shutil import rmtree


def main():
    
    json_message = json.loads(get_message())
    
    output_file_content = base64.b64decode(json_message["output_file"])
    output_file_extension = json_message["output_file_extension"]
    
    output_archive_content = base64.b64decode(json_message["output_archive"])
    output_archive_extension = json_message["output_archive_extension"]

    board = json_message["board"]
    application_name = json_message["application_name"]
    
    try:
        temporary_directory = "tmp/" + application_name + "/"
        create_directories(temporary_directory)
        
        archive_file_path = temporary_directory + application_name + "." + output_archive_extension
        
        with open(archive_file_path, "wb") as archive:
            archive.write(output_archive_content)
            
        dest_path = temporary_directory + application_name + "/"
        create_directories(dest_path)
        
        tar = tarfile.open(archive_file_path, "r:gz")
        for tarinfo in tar:
            tar.extract(tarinfo, dest_path)
            
        tar.close()
        
        path_to_makefile = os.path.join(dest_path, "generated_by_riotam", application_name)
        process = Popen(["x-terminal-emulator -e './flash " + board + " " + path_to_makefile + "'"], shell=True)
        #process.communicate()

        #rmtree(temporary_directory)
        
    except Exception as e:
        logging.error(str(e), exc_info=True)


def create_directories(path):
    
    try:
        os.makedirs(path)

    except OSError as e:

        if e.errno != errno.EEXIST:
            raise


# https://chromium.googlesource.com/chromium/src/+/master/chrome/common/extensions/docs/examples/api/nativeMessaging/host/native-messaging-example-host
def get_message():
    
    # Read the message length (first 4 bytes).
    text_length_bytes = sys.stdin.read(4)
    if len(text_length_bytes) == 0:
        sys.exit(0)

    # Unpack message length as 4 byte integer.
    text_length = struct.unpack('i', text_length_bytes)[0]

    # Read the text (JSON object) of the message.
    text = sys.stdin.read(text_length).decode('utf-8')
    
    return text


if __name__ == "__main__":

    logging.basicConfig(filename="log/riot_app_market_log.txt", format="%(asctime)s [%(levelname)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)

    try:
        main()

    except Exception as e:
        logging.error(str(e), exc_info=True)
