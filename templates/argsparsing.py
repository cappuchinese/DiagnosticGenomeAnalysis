#!/usr/bin/env python3

"""
Module to parse terminal arguments
"""

import argparse
from getpass import getpass


def _args_parsing():
    """
    Function to parse terminal commands
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("host", metavar="H", help="Host of database")
    parser.add_argument("user", metavar="U", help="Name of the user")
    parser.add_argument("database", metavar="D", help="Name of database")
    parser.add_argument("anno_file", metavar="F", help="ANNOVAR file")
    parser.add_argument("-p", "--password", action="store_true", dest="password",
                        help="Password of the user")
    args = parser.parse_args()

    if args.password:
        password = getpass("Enter password: ")

    return args, password
