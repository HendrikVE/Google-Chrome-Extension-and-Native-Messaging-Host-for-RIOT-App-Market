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
import os
import sys
from subprocess import Popen

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
EXTENSION_XPI_PATH = os.path.join('src', 'extension', 'rapstore-1.0.6-an+fx-mac.xpi')

import utility.common as common
from utility.browser import Firefox, Chrome, Chromium, BrowserNotSupportedException


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
        print('chrome not supported yet!')

    elif isinstance(browser, Chromium):
        print('chromium not supported yet!')


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