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

import errno
import os
import subprocess

from browser import Chrome, Chromium, Firefox, BrowserNotSupportedException

HOST_NAME = 'de.fu_berlin.mi.riot_app_market'
FIREFOX_EXTENSION_ID = 'rapstore.extension@fu-berlin.de'
CHROME_EXTENSION_ID = 'knldjmfmopnpolahpmmgbagdohdnhkik'


def get_browser(browser_name):
    
    if browser_name == 'chrome':
        return Chrome()

    elif browser_name == 'chromium':
        return Chromium()

    elif browser_name == 'firefox':
        return Firefox()

    raise BrowserNotSupportedException(browser_name)


def get_target_dir(home_dir, browser):
    """
    Get the target dir for installing native messaging host

    Parameters
    ----------
    home_dir: string
        Home directory of the user
    browser: Browser
        The browser to install the host

    Returns
    -------
    string
        target directory

    """
    target_dir = None
    if is_mac_os():
        if is_root_user():
            target_dir = browser.get_root_install_path(True)

        else:
            target_dir = browser.get_user_install_path(home_dir, True)

    else:
        # we are supposing it is linux
        if is_root_user():
            target_dir = browser.get_root_install_path(False)

        else:
            target_dir = browser.get_user_install_path(home_dir, False)

    if target_dir is None:
        raise BrowserNotSupportedException(browser)

    return target_dir


def get_allowed_attribute(browser):

    if browser.get_name() == 'chrome' or browser.get_name() == 'chromium':
        return '"allowed_origins": [ "chrome-extension://%s/" ]' % CHROME_EXTENSION_ID

    elif browser.get_name() == 'firefox':
        return '"allowed_extensions": [ "%s" ]' % FIREFOX_EXTENSION_ID

    else:
        raise BrowserNotSupportedException(browser.get_name())


def is_mac_os():

    output = subprocess.check_output(['uname', '-s'])
    return output.strip() == 'Darwin'


def is_root_user():

    output = subprocess.check_output(['whoami'])
    return output.strip() == 'root'


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
        Something fails creating directories, except directoy already exist

    """
    try:
        os.makedirs(path)

    except OSError as e:

        if e.errno != errno.EEXIST:
            raise
