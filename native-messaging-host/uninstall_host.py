#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import argparse
from os.path import expanduser

import sys

import os

from common import get_target_dir, BrowserNotSupportedException


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

    host_name = "de.fu_berlin.mi.riot_app_market"

    try:
        os.remove("{0}/{1}.json".format(target_dir, host_name))

    except OSError:
        pass

    print("Native messaging host {0} has been uninstalled from {1}".format(host_name, args.browser))


def init_argparse():

    parser = argparse.ArgumentParser(description="Build RIOT OS")

    parser.add_argument("--browser",
                        dest="browser", action="store",
                        required=True,
                        help="the browser to install the host for. (chrome or chromium)")

    return parser


if __name__ == "__main__":

    main(sys.argv[1:])