#!/usr/bin/env python3
"""
Copyright (C) 2018 Enrico Bianchi (enrico.bianchi@gmail.com)
Project       mailarchive
Description   A mail archiver
License       GPL version 2 (see GPL.txt for details)
"""

__author__ = "Enrico Bianchi"
__copyright__ = "Copyright 2018, Enrico Bianchi"
__credits__ = ["Enrico Bianchi", ]
__license__ = "GPLv2"
__maintainer__ = "Enrico Bianchi"
__email__ = "enrico.bianchi@gmail.com"
__status__ = "Development"
__version__ = "0.0.0"

import argparse
import configparser
import sys


def initargs():
    """
    Argument parser initialization
    :return: An object that parse arguments passed from command line
    """

    args = argparse.ArgumentParser(description="Goffrey")

    # Global arguments
    args.add_argument("-c", "--cfg", metavar="<file>", required=True,
                      help="Use the specified configuration file")

    return args


def execute(cfg):
    """
    Execute operations
    """
    pass

def main():
    """
    Main function
    :return:
    """

    args = initargs().parse_args()
    cfg = configparser.ConfigParser()
    try:
        cfg.read(args.cfg)
    except:
        print("Cannot open the configuration file {}: not found".format(args.cfg))
        args.print_help()
        sys.exit(1)

    execute(cfg)


if __name__ == '__main__':
    main()
