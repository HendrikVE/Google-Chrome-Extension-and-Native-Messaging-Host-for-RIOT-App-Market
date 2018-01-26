#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
 * Copyright (C) 2018 Hendrik van Essen and FU Berlin
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
"""

from __future__ import absolute_import, print_function, unicode_literals

import os
from os.path import expanduser
import stat
from shutil import copyfile

from .util.common import HOST_NAME, get_target_dirs, create_directories, get_allowed_attribute

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT_DIR = os.path.normpath(os.path.join(CUR_DIR, os.pardir, os.pardir))

HOST_PATH = os.path.join(PROJECT_ROOT_DIR, 'src', 'native-messaging-host', 'riot_app_market.py')
HOST_MANIFEST_PATH = os.path.join(PROJECT_ROOT_DIR, 'src', 'native-messaging-host', 'de.fu_berlin.mi.riot_app_market.json')


def install_host(browser):

    home_dir = expanduser('~')
    target_dirs = get_target_dirs(home_dir, browser)

    for dir in target_dirs:
        _install_manifest_file(dir, browser)

    print()


def uninstall_host(browser):

    home_dir = expanduser('~')
    target_dirs = get_target_dirs(home_dir, browser)

    for dir in target_dirs:
        _uninstall_manifest(dir, browser)

    print()


def _install_manifest_file(target_dir, browser):

    # create directory to store native messaging host
    create_directories(target_dir)

    # copy native messaging host manifest
    json_manifest_name = '%s.json' % HOST_NAME
    source_manifest = HOST_MANIFEST_PATH
    target_manifest = os.path.join(target_dir, json_manifest_name)
    copyfile(source_manifest, target_manifest)

    target_file = os.path.join(target_dir, json_manifest_name)

    # replace HOST_PATH placeholder in the manifest
    _replace_host_path(target_file, HOST_PATH)

    # replace ALLOWED_ATTRIBUTE placeholder in the manifest
    _firefox_chrome_compatibility_switch(target_file, browser)

    # set permissions for the manifest so that all users can read it
    json_manifest = '{0}/{1}'.format(target_dir, json_manifest_name)
    st = os.stat(json_manifest)
    os.chmod(json_manifest, st.st_mode | stat.S_IROTH)

    print('installed host {0} for {1} at {2}'.format(HOST_NAME, browser.get_name(), target_dir))


def _replace_host_path(path, host_path):

    copyfile(path, path + '.old')

    with open(path + '.old', 'r') as old_file:
        with open(path, 'w') as file:

            for line in old_file.readlines():
                if 'HOST_PATH' in line:
                    line = line.replace('HOST_PATH', host_path)

                file.write(line)

    os.remove(path + '.old')


def _firefox_chrome_compatibility_switch(path, browser):

    copyfile(path, path + '.old')

    with open(path + '.old', 'r') as old_file:
        with open(path, 'w') as file:

            for line in old_file.readlines():
                if 'ALLOWED_ATTRIBUTE' in line:
                    allowed_attribute = get_allowed_attribute(browser)
                    line = line.replace('ALLOWED_ATTRIBUTE', allowed_attribute)

                file.write(line)

    os.remove(path + '.old')


def _uninstall_manifest(target_dir, browser):

    file_to_delete = '{0}/{1}.json'.format(target_dir, HOST_NAME)

    try:
        os.remove(file_to_delete)

    except OSError:
        print('host is currently not installed for {0} at {1}'.format(browser.get_name(), target_dir))
        return

    print('removed host {0} at {1} from {2}'.format(HOST_NAME, target_dir, browser.get_name()))
