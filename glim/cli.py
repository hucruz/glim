#!/usr/bin/env python
#          _
#       | (_)
#   __ _| |_ _ __ ___
#  / _` | | | '_ ` _ \
# | (_| | | | | | | | |
#  \__, |_|_|_| |_| |_|
#   __/ |
#  |___/
#
#
# A modern python framework for the web

__author__ = "Aras Can Akin"

from . import paths
paths.configure()

from termcolor import colored

from glim.app import Glim
from glim.utils import import_module
from glim.command import CommandAdapter

import glim.commands

import traceback
import argparse
import os
import sys

description = "glim ~ a modern python framework for the web"


def main():
    """
    The single entry point to glim command line interface.Main method is called
    from pypi console_scripts key or by glim.py on root.This function
    initializes a new app given the glim commands and app commands if app
    exists.

    Usage
    -----
      $ python glim/cli.py start
      $ python glim.py start (on root folder)
    """
    # register the global parser
    preparser = argparse.ArgumentParser(description=description,
                                        add_help=False)

    # parse existing options
    namespace, extra = preparser.parse_known_args()

    # register the subparsers
    parser = argparse.ArgumentParser(parents=[preparser],
                                     description=description,
                                     add_help=True)

    subparsers = parser.add_subparsers(title='commands', help='commands')

    # initialize a command adapter with subparsers
    commandadapter = CommandAdapter(subparsers)

    # register glim commands
    commandadapter.register(glim.commands)

    # register app commands
    appcommands = import_module('app.commands', pass_errors=True)
    commandadapter.register(appcommands)

    app = None

    if paths.app_exists() is False:
        # check if a new app is being created
        new = True if 'new' in extra else False

        if ('help' in extra) or ('--help' in extra) or ('-h' in extra):
            help = True
        else:
            help = False

        if help:
            parser.print_help()
            exit()
    else:
        app = make_app(commandadapter)

    args = parser.parse_args()

    command = commandadapter.match(args)
    commandadapter.dispatch(command, app)

def make_app(commandadapter=None):
    """
    Function creates an app
    """
    mconfig = import_module('app.config', pass_errors=True)
    mstart = import_module('app.start')
    mroutes = import_module('app.routes')
    mcontrollers = import_module('app.controllers')
    before = mstart.before

    return Glim(commandadapter, mconfig, mroutes, mcontrollers, before)

if __name__ == '__main__':
    main()
