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
import subprocess
import sys

from utility.common import EXTENSION_VERSION, is_root_user
from utility.browser import Firefox, Chrome, Chromium, BrowserNotSupportedException, get_browser

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
EXTENSION_XPI_PATH = os.path.join(CUR_DIR, 'dist', 'extension', 'firefox', 'rapstore-%s.xpi' % EXTENSION_VERSION)
EXTENSION_CRX_PATH = os.path.join(CUR_DIR, 'dist', 'extension', 'chrome', 'rapstore-%s.crx' % EXTENSION_VERSION)


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

    install_extension(browser)


def install_extension(browser):

    if isinstance(browser, Firefox):

        if is_root_user():
            origin_user = subprocess.check_output(['logname']).strip()
            # can't run firefox as root to install, because of problems
            output = subprocess.check_output(['sudo', '-u', origin_user, 'firefox', EXTENSION_XPI_PATH],
                                             stderr=subprocess.STDOUT)
        else:
            output = subprocess.check_output(['firefox', EXTENSION_XPI_PATH], stderr=subprocess.STDOUT)

        print(output)

    elif isinstance(browser, Chrome):
        output = subprocess.check_output(['sudo', 'python', '_install_chrome_based_extension.py',
                                          '/usr/share/google-chrome/extensions/', EXTENSION_CRX_PATH],
                                         stderr=subprocess.STDOUT)
        print(output)

    elif isinstance(browser, Chromium):
        output = subprocess.check_output(['sudo', 'python', '_install_chrome_based_extension.py',
                                          '/usr/share/chromium-browser/extensions/', EXTENSION_CRX_PATH],
                                         stderr=subprocess.STDOUT)
        print(output)

    else:
        raise BrowserNotSupportedException(browser.get_name())


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