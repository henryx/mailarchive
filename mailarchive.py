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
import imaplib
import sys
from contextlib import closing

import database
import emails


def initargs():
    """
    Argument parser initialization
    :return: An object that parse arguments passed from command line
    """

    args = argparse.ArgumentParser(description="Mailarchive")

    # Global arguments
    args.add_argument("-c", "--cfg", metavar="<file>", required=True,
                      help="Use the specified configuration file")

    return args


def fetch(imap, folder):
    """
    fetch emails in folder
    :param imap: imap connection
    :param folder: Folder to archive
    :return: A generator that yield fetched emails in folder
    """
    status, count = imap.list(folder[2])
    if status == "OK":
        for msgid in count[0]:
            status, mail = imap.fetch(msgid, folder[2])
            if status == "OK":
                yield mail


def store(location, folder, mail):
    """
    store emails in folder to database
    :param location: location of the database
    :param folder: folder that contain email
    :param mail: the email
    :return:
    """
    with database.Database(location) as db:
        pass


def execute(cfg):
    """
    Execute operations
    :param cfg: A configuration object
    """

    for section in cfg.sections():
        if section not in ["general", "logging"]:
            if cfg[section]["protocol"] in ["imap", "imaps"]:
                with closing(emails.IMAP()) as imap:
                    imap.user = cfg[section]["user"]
                    imap.password = cfg[section]["password"]
                    imap.host = cfg[section]["host"]
                    imap.port = cfg[section]["port"]
                    imap.scheme = cfg[section]["protocol"]
                    try:
                        imap.open()
                    except imaplib.IMAP4.error as e:
                        print(
                            "Could not connect to {0}://{1}:{2} - {3!s}".format(imap.scheme,
                                                                                imap.host,
                                                                                imap.port,
                                                                                str(e.args[0].decode()))
                        )
                        break

                    status, folders = imap.folders()
                    if status == "OK":
                        for folder in folders:
                            for mail in fetch(imap, folder):
                                store(cfg["general"]["database"], folder, mail)


def main():
    """
    Main function
    :return:
    """

    parser = initargs()
    args = parser.parse_args()
    cfg = configparser.ConfigParser()
    try:
        with open(args.cfg) as f:
            cfg.read_file(f)
    except:
        print("Cannot open the configuration file {}: not found".format(args.cfg))
        parser.print_help()
        sys.exit(1)

    execute(cfg)


if __name__ == '__main__':
    main()
