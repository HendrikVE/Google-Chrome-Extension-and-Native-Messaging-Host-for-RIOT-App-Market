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

from subprocess import check_output
import os

from .browser import Chrome, Chromium, Firefox, BrowserNotSupportedException

CUR_DIR = os.path.abspath(os.path.dirname(__file__))


def download_extension(browser, save_path, extension_version):

    github_version_tag = _get_github_version_tag()
    print('current release: ' + github_version_tag)

    url = _get_server_url(browser, github_version_tag, extension_version)
    print('downloading extension from ' + url)

    check_output(['curl', '-L', url, '--create-dirs', '-o', save_path])


def _get_server_url(browser, github_version_tag, extension_version):

    if isinstance(browser, Chrome) or isinstance(browser, Chromium):
        return 'https://github.com/riot-appstore/rapstore-browser-integration/releases/download/{0}/extension-{1}.crx'.format(github_version_tag, extension_version)

    elif isinstance(browser, Firefox):
        return 'https://github.com/riot-appstore/rapstore-browser-integration/releases/download/{0}/extension-{1}.xpi'.format(github_version_tag, extension_version)

    else:
        raise BrowserNotSupportedException(browser.get_name())


def _get_github_version_tag():

    output = check_output(['curl --silent "https://api.github.com/repos/riot-appstore/rapstore-browser-integration/releases/latest" | grep \'"tag_name":\' | sed -E \'s/.*"([^"]+)".*/\\1/\''], shell=True)
    return output.strip()
