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

import argparse
import os
import sys
from os.path import expanduser

from common import get_target_dir, BrowserNotSupportedException, HOST_NAME


def main(argv):

    parser = init_argparse()

    try:
        args = parser.parse_args(argv)

    except Exception as e:
        print (str(e))
        return

    home_dir = expanduser("~")

    try:
        target_dir = get_target_dir(home_dir, args.browser)

    except BrowserNotSupportedException as e:
        print (str(e))
        return

    try:
        os.remove("{0}/{1}.json".format(target_dir, HOST_NAME))

    except OSError:
        # we are not interested in missing files when removing anyway
        pass

    print("Native messaging host {0} has been uninstalled from {1}".format(HOST_NAME, args.browser))


def init_argparse():

    parser = argparse.ArgumentParser(description="Build RIOT OS")

    parser.add_argument("--browser",
                        dest="browser", action="store",
                        required=True,
                        help="the browser to install the host for. (chrome or chromium)")

    return parser


if __name__ == "__main__":

    main(sys.argv[1:])