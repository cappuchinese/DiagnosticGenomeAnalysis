#!/usr/bin/env python3

"""
BFV2 Theme 05 - Genomics - Sequencing Project

Deliverable 9
-------------
Template deliverable that interacts with database to fill.

    usage:
        python3 deliverable9.py database_host database_username database_password ANNOVAR_file
"""

__author__ = "Lisa Hu"
__version__ = "2021.d9.v1"

# IMPORTS
import sys
import argparse
import mysql.connector as msql
import getpass


class DatabaseConnector:

    def __init__(self):
        pass

    def run(self):
        """
        Main function to run program
        :return:
        """
        args = self._args_parsing()
        config = {
            "user": args.user,
            "password": args.password,
            "host": args.host,
            "database": args.database,
            "raise_on_warnings": True
        }
        # genes_list = self.parse_annovar(args.ANNO_file)
        # self.data_to_db(config, genes)

    @staticmethod
    def _args_parsing():
        parser = argparse.ArgumentParser()
        parser.add_argument("host", metavar="H", help="Host of database")
        parser.add_argument("user", metavar="U", help="Name of the user")
        parser.add_argument("database", metavar="D", help="Name of database")
        parser.add_argument("password", metavar="P", type=getpass.getpass(),
                            help="Password of the user")
        parser.add_argument("ANNO_file", metavar="F", help="ANNOVAR file")
        args = parser.parse_args()

        return args

    def parse_annovar(self, anno_file):
        """
        Function from deliverable 6-7 to parse data
        :param anno_file: ANNOVAR file
        :return: Parsed ANNOVAR data
        """
        pass

    @staticmethod
    def _regex_parsing(genes):
        """
        Function from deliverable 6-7 to parse gene data
        :param genes: gene name from ANNOVAR data
        :return: parsed gene
        """
        pass

    def data_to_db(self, config, gene_data):
        """
        Function to connect to database and put data in
        :param config: login credentials
        :param gene_data: Parsed ANNOVAR data
        :return:
        """
        pass

