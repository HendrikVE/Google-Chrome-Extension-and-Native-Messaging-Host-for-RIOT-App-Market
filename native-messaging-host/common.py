#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
 * Copyright (C) 2017 Hendrik van Essen
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
"""

from __future__ import print_function

import errno
import os
import subprocess

HOST_NAME = "de.fu_berlin.mi.riot_app_market"


class BrowserNotSupportedException(Exception):
    pass


def get_target_dir(home_dir, browser):

    target_dir = None
    if is_mac_os():
        if is_root_user():
            if is_chrome(browser):
                target_dir = "/Library/Google/Chrome/NativeMessagingHosts"

            elif is_chromium(browser):
                target_dir = "/Library/Application Support/Chromium/NativeMessagingHosts"

        else:
            if is_chrome(browser):
                target_dir = "%s/Library/Application Support/Google/Chrome/NativeMessagingHosts" % home_dir

            elif is_chromium(browser):
                target_dir = "%s/Library/Application Support/Chromium/NativeMessagingHosts" % home_dir

    else:
        # we are supposing it is linux
        if is_root_user():
            if is_chrome(browser):
                target_dir = "/etc/opt/chrome/native-messaging-hosts"

            elif is_chromium(browser):
                target_dir = "/etc/chromium/native-messaging-hosts"

        else:
            if is_chrome(browser):
                target_dir = "%s/.config/google-chrome/NativeMessagingHosts" % home_dir

            elif is_chromium(browser):
                target_dir = "%s/.config/chromium/NativeMessagingHosts" % home_dir

    if target_dir is None:
        raise BrowserNotSupportedException("%s is not supported" % browser)

    return target_dir


def is_mac_os():

    output = subprocess.check_output(["uname", "-s"])
    return output.strip() == "Darwin"


def is_root_user():

    output = subprocess.check_output(["whoami"])
    return output.strip() == "root"


def is_chrome(browser):
    return browser == "chrome"


def is_chromium(browser):
    return browser == "chromium"


def create_directories(path):
    """
    Creates all directories on path

    Parameters
    ----------
    path: string
        Path to create

    Raises
    -------
    OSError
        Something fails creating directories, except errno is EEXIST

    """
    try:
        os.makedirs(path)

    except OSError as e:

        if e.errno != errno.EEXIST:
            raise
