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

import json
import os
import subprocess

from .util.browser import Firefox, Chrome, Chromium, BrowserNotSupportedException
from .util.common import EXTENSION_VERSION, CHROME_EXTENSION_ID, is_root_user

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT_DIR = os.path.normpath(os.path.join(CUR_DIR, os.pardir, os.pardir))

EXTENSION_XPI_PATH = os.path.join(PROJECT_ROOT_DIR, 'dist', 'extension', 'firefox', 'rapstore-%s.xpi' % EXTENSION_VERSION)
EXTENSION_CRX_PATH = os.path.join(PROJECT_ROOT_DIR, 'dist', 'extension', 'chrome', 'rapstore-%s.crx' % EXTENSION_VERSION)

INSTALL_PATH_CHROME = '/usr/share/google-chrome/extensions/'
INSTALL_PATH_CHROMIUM = '/usr/share/chromium-browser/extensions/'

CHROME_INSTALL_FILE_NAME = CHROME_EXTENSION_ID + '.json'


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

        _install_chrome_based(INSTALL_PATH_CHROME, EXTENSION_CRX_PATH)
        print('installed for chrome')
        print('NOTICE: You need to restart your browser!')

    elif isinstance(browser, Chromium):

        _install_chrome_based(INSTALL_PATH_CHROMIUM, EXTENSION_CRX_PATH)
        print('installed for chromium')
        print('NOTICE: You need to restart your browser!')


    else:
        raise BrowserNotSupportedException(browser.get_name())

    print()


def uninstall_extension(browser):

    if isinstance(browser, Firefox):

        print('please remove the extension manually')

    elif isinstance(browser, Chrome):

        file_to_delete = os.path.join(INSTALL_PATH_CHROME, CHROME_INSTALL_FILE_NAME)

        if not os.path.isfile(file_to_delete):
            print('File not found, it seems like the extension is currently not installed')
            return

        output = subprocess.check_output(['sudo', 'rm', file_to_delete],
                                         stderr=subprocess.STDOUT, cwd=CUR_DIR)
        print(output)
        print('removed from chrome')
        print('NOTICE: You need to restart your browser!')

    elif isinstance(browser, Chromium):

        file_to_delete = os.path.join(INSTALL_PATH_CHROMIUM, CHROME_INSTALL_FILE_NAME)

        if not os.path.isfile(file_to_delete):
            print('File not found, it seems like the extension is currently not installed')
            print()
            return

        output = subprocess.check_output(['sudo', 'rm', file_to_delete],
                                         stderr=subprocess.STDOUT, cwd=CUR_DIR)
        print(output)
        print('removed from chromium')
        print('NOTICE: You need to restart your browser!')

    else:
        raise BrowserNotSupportedException(browser.get_name())

    print()


def _install_chrome_based(dest_path, extension_crx_path):

    json_file_content = {
        'external_crx': os.path.abspath(extension_crx_path),
        'external_version': EXTENSION_VERSION,
    }

    tmp_file_path = os.path.join(CUR_DIR, CHROME_INSTALL_FILE_NAME)

    # beginning with sudo operations
    output = subprocess.check_output(['sudo', 'mkdir', '-p', dest_path], stderr=subprocess.STDOUT, cwd=CUR_DIR)
    if len(output.strip()) > 0:
        print(output)

    with open(tmp_file_path, 'w') as tmp_file:
        tmp_file.write(json.dumps(json_file_content))

    output = subprocess.check_output(['sudo', 'mv', tmp_file_path, dest_path], stderr=subprocess.STDOUT, cwd=CUR_DIR)
    if len(output.strip()) > 0:
        print(output)

    print('created {0} in {1}'.format(CHROME_INSTALL_FILE_NAME, dest_path))