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

import common
from common import Browser, BrowserNotSupportedException

CUR_DIR = os.path.abspath(os.path.dirname(__file__))


def main(argv):

    parser = init_argparse()

    try:
        args = parser.parse_args(argv)

    except Exception as e:
        print (str(e))
        return

    home_dir = expanduser('~')

    try:
        if args.browser == 'chrome':
            browser = Browser.CHROME

        elif args.browser == 'chromium':
            browser = Browser.CHROMIUM

        elif args.browser == 'firefox':
            browser = Browser.FIREFOX

        else:
            raise BrowserNotSupportedException(args.browser)

        target_dir = common.get_target_dir(home_dir, browser)

    except common.BrowserNotSupportedException as e:
        print(str(e))
        return

    # create directory to store native messaging host
    common.create_directories(target_dir)

    # copy native messaging host manifest
    json_manifest_name = '%s.json' % common.HOST_NAME
    copyfile(os.path.join(CUR_DIR, json_manifest_name), os.path.join(target_dir, json_manifest_name))

    target_file = os.path.join(target_dir, json_manifest_name)

    # replace HOST_PATH placeholder in the manifest
    host_path = '%s/riot_app_market.py' % CUR_DIR
    replace_host_path(target_file, host_path)

    # replace ALLOWED_ATTRIBUTE placeholder in the manifest
    firefox_chrome_compatibility_switch(target_file, browser)

    # set permissions for the manifest so that all users can read it
    json_manifest = '{0}/{1}'.format(target_dir, json_manifest_name)
    st = os.stat(json_manifest)
    os.chmod(json_manifest, st.st_mode | stat.S_IROTH)

    print ('Native messaging host {0} has been installed for {1}'.format(common.HOST_NAME, browser))


def init_argparse():

    parser = argparse.ArgumentParser(description='Build RIOT OS')

    parser.add_argument('--browser',
                        dest='browser', action='store',
                        required=True,
                        help='the browser to install the host for. (chrome or chromium)')

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
                    allowed_attribute = common.get_allowed_attribute(browser)
                    line = line.replace('ALLOWED_ATTRIBUTE', allowed_attribute)

                file.write(line)

    os.remove(path + '.old')


if __name__ == '__main__':

    main(sys.argv[1:])