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
import stat
import sys
from os.path import expanduser
from shutil import copyfile

from utility.common import HOST_NAME, get_target_dirs, create_directories, get_allowed_attribute
from utility.browser import BrowserNotSupportedException, get_browser

CUR_DIR = os.path.abspath(os.path.dirname(__file__))

HOST_PATH = os.path.join(CUR_DIR, 'src', 'native-messaging-host', 'riot_app_market.py')
HOST_MANIFEST_PATH = os.path.join(CUR_DIR, 'src', 'native-messaging-host', 'de.fu_berlin.mi.riot_app_market.json')


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
        install_manifest_file(dir, browser)


def install_manifest_file(target_dir, browser):

    # create directory to store native messaging host
    create_directories(target_dir)

    # copy native messaging host manifest
    json_manifest_name = '%s.json' % HOST_NAME
    source_manifest = HOST_MANIFEST_PATH
    target_manifest = os.path.join(target_dir, json_manifest_name)
    copyfile(source_manifest, target_manifest)

    target_file = os.path.join(target_dir, json_manifest_name)

    # replace HOST_PATH placeholder in the manifest
    replace_host_path(target_file, HOST_PATH)

    # replace ALLOWED_ATTRIBUTE placeholder in the manifest
    firefox_chrome_compatibility_switch(target_file, browser)

    # set permissions for the manifest so that all users can read it
    json_manifest = '{0}/{1}'.format(target_dir, json_manifest_name)
    st = os.stat(json_manifest)
    os.chmod(json_manifest, st.st_mode | stat.S_IROTH)

    print('Native messaging host {0} has been installed for {1} in {2}'.format(HOST_NAME, browser.get_name(), target_dir))


def init_argparse():

    parser = argparse.ArgumentParser(description='Build RIOT OS')

    parser.add_argument('browser',
                        action='store',
                        choices=['chrome', 'chromium', 'firefox'],
                        help='the browser to install the host for')

    return parser


def replace_host_path(path, host_path):

    copyfile(path, path + '.old')

    with open(path + '.old', 'r') as old_file:
        with open(path, 'w') as file:

            for line in old_file.readlines():
                if 'HOST_PATH' in line:
                    line = line.replace('HOST_PATH', host_path)

                file.write(line)

    os.remove(path + '.old')


def firefox_chrome_compatibility_switch(path, browser):

    copyfile(path, path + '.old')

    with open(path + '.old', 'r') as old_file:
        with open(path, 'w') as file:

            for line in old_file.readlines():
                if 'ALLOWED_ATTRIBUTE' in line:
                    allowed_attribute = get_allowed_attribute(browser)
                    line = line.replace('ALLOWED_ATTRIBUTE', allowed_attribute)

                file.write(line)

    os.remove(path + '.old')


if __name__ == '__main__':

    if ' ' in CUR_DIR:
        print('this repository needs to be cloned to a path without spaces before installing the native messaging host!')

    else:
        main(sys.argv[1:])