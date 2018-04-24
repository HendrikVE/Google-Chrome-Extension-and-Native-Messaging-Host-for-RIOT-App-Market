#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
 * Copyright (C) 2017 Hendrik van Essen
 *
 * This file is subject to the terms and conditions of the MIT License
 * See the file LICENSE in the top level directory for more details.
"""

from __future__ import absolute_import, print_function, unicode_literals

import sys

BLACK = '\033[0;30m'
GREY_DARK = '\033[1;30m'
GREY_LIGHT = '\033[0;37m'
RED = '\033[0;31m'
RED_LIGHT = '\033[1;31m'
GREEN = '\033[0;32m'
GREEN_LIGHT = '\033[1;32m'
BROWN = '\033[0;33m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
BLUE_LIGHT = '\033[1;34m'
PURPLE = '\033[0;35m'
PURPLE_LIGHT = '\033[1;35m'
CYAN = '\033[0;36m'
CYAN_LIGHT = '\033[1;36m'
WHITE = '\033[1;37m'
COLORLESS = '\033[0m'

BOLD = '\033[;1m'
REVERSE = '\033[;7m'

RESET = '\033[0;0m'


def style_text(text, style):
    return style + text + RESET


def print_red(output_string):
    _colored_print(output_string, RED)


def print_blue(output_string):
    _colored_print(output_string, BLUE)


def print_cyan(output_string):
    _colored_print(output_string, CYAN)


def print_green(output_string):
    _colored_print(output_string, GREEN)


def print_bold(output_string):
    _colored_print(output_string, BOLD)


def print_reverse(output_string):
    _colored_print(output_string, REVERSE)


def _colored_print(output_string, style):
    sys.stdout.write(style)
    sys.stdout.write(output_string)
    print(RESET)
