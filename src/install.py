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

from setup.util.browser import get_browser, BrowserNotSupportedException
from setup.extension import install_extension, uninstall_extension, get_extension_version
from setup.host import install_host, uninstall_host

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

    if args.remove:
        if args.component == 'extension':
            uninstall_extension(browser)

        elif args.component == 'host':
            uninstall_host(browser)

        else:
            uninstall_extension(browser)
            uninstall_host(browser)

    else:
        version = get_extension_version()

        if args.component == 'extension':
            install_extension(browser, version)

        elif args.component == 'host':
            install_host(browser)

        else:
            install_extension(browser, version)
            install_host(browser)

    print('done')


def init_argparse():

    parser = argparse.ArgumentParser(description='Build RIOT OS')

    parser.add_argument('browser',
                        action='store',
                        choices=['chrome', 'chromium', 'firefox'],
                        help='the browser to install the integration for')

    parser.add_argument('--remove',
                        action='store_true',
                        help='remove installed components')

    parser.add_argument('--component',
                        action='store',
                        choices=['host', 'extension', 'all'],
                        default='all',
                        help='which part of the integration should be installed (all on default)')

    return parser


if __name__ == '__main__':

    if ' ' in CUR_DIR:
        print('this repository needs to be cloned to a path without spaces before installing the native messaging host!')

    else:
        main(sys.argv[1:])