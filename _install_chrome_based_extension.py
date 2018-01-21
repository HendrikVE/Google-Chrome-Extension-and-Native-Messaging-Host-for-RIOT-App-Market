#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
 * Copyright (C) 2018 FU Berlin
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
"""
import json
import sys
import os

from utility.common import CHROME_EXTENSION_ID, EXTENSION_VERSION, create_directories


def main(argv):

    install_chrome_based(argv[0], argv[1])


def install_chrome_based(dest_path, extension_crx_path):

    dest = os.path.join(dest_path, CHROME_EXTENSION_ID + '.json')

    create_directories(dest_path)

    json_file_content = {
        'external_crx': os.path.abspath(extension_crx_path),
        'external_version': EXTENSION_VERSION,
    }

    with open(dest, 'w') as preferences_file:
        preferences_file.write(json.dumps(json_file_content))

    print('created %s' % dest)


if __name__ == '__main__':

    main(sys.argv[1:])