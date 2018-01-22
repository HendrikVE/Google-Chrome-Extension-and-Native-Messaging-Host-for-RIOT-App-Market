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
import sys
import os

import install_extension as install_extension
import install_host as install_host
from utility.browser import BrowserNotSupportedException, get_browser

CUR_DIR = os.path.abspath(os.path.dirname(__file__))


def main(argv):

    parser = init_argparse()

    try:
        args = parser.parse_args(argv)

    except Exception as e:
        print (str(e))
        return

    try:
        browser = get_browser(args.browser)

    except BrowserNotSupportedException as e:
        print(str(e))
        return

    print('installing extension')
    install_extension.main(argv)

    print('installing native messaging host')
    install_host.main(argv)

    print('done')


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