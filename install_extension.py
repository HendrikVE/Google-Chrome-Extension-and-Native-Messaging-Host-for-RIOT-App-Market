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

import argparse
import json
import os
import sys
from subprocess import Popen

import utility.common as common
from utility.browser import Firefox, Chrome, Chromium, BrowserNotSupportedException

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
EXTENSION_XPI_PATH = os.path.join('dist', 'extension', 'firefox', 'rapstore-%s.xpi' % common.EXTENSION_VERSION)
EXTENSION_CRX_PATH = os.path.join('dist', 'extension', 'chrome', 'rapstore-%s.crx' % common.EXTENSION_VERSION)


def main(argv):

    parser = init_argparse()

    try:
        args = parser.parse_args(argv)

    except Exception as e:
        print (str(e))
        return

    try:
        browser = common.get_browser(args.browser)

    except BrowserNotSupportedException as e:
        print(str(e))
        return

    install_extension(browser)


def install_extension(browser):

    if isinstance(browser, Firefox):
        Popen(['firefox', EXTENSION_XPI_PATH])

    elif isinstance(browser, Chrome):
        install_chrome_based('/usr/share/google-chrome/extensions/')

    elif isinstance(browser, Chromium):
        install_chrome_based('/usr/share/chromium-browser/extensions/')

    else:
        raise BrowserNotSupportedException(browser.get_name())


def install_chrome_based(dest_path):
    dest = os.path.join(dest_path, common.CHROME_EXTENSION_ID + '.json')

    common.create_directories(dest_path)

    json_file_content = {
        'external_crx': os.path.abspath(EXTENSION_CRX_PATH),
        'external_version': common.EXTENSION_VERSION,
    }

    with open(dest, 'w') as preferences_file:
        preferences_file.write(json.dumps(json_file_content))


def init_argparse():

    parser = argparse.ArgumentParser(description='Build RIOT OS')

    parser.add_argument('browser',
                        action='store',
                        choices=['chrome', 'chromium', 'firefox'],
                        help='the browser to install the host for')

    return parser


if __name__ == '__main__':

    if ' ' in CUR_DIR:
        print('this repository needs to be cloned to a path without spaces before installing the native messaging host!')

    else:
        main(sys.argv[1:])