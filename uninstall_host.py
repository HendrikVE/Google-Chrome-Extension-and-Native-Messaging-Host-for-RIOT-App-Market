#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
 * Copyright (C) 2017 Hendrik van Essen
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
"""

from __future__ import absolute_import, print_function, unicode_literals

import argparse
import os
import sys
from os.path import expanduser

from utility.common import HOST_NAME, get_target_dirs
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

    home_dir = expanduser('~')
    target_dirs = get_target_dirs(home_dir, browser)

    for dir in target_dirs:
        uninstall_manifest(dir, browser)


def uninstall_manifest(target_dir, browser):

    try:
        os.remove('{0}/{1}.json'.format(target_dir, HOST_NAME))

    except OSError:
        # we are not interested in missing files when removing anyway
        pass

    print('Native messaging host {0} at {1} has been uninstalled from {2}\n'.format(HOST_NAME, target_dir, browser.get_name()))


def init_argparse():

    parser = argparse.ArgumentParser(description='Build RIOT OS')

    parser.add_argument('browser',
                        action='store',
                        choices=['chrome', 'chromium', 'firefox'],
                        help='the browser to install the host for')

    return parser


if __name__ == '__main__':

    main(sys.argv[1:])