#!/usr/bin/env python3

"""
BFV2 Theme 05 - Genomics - Sequencing Project

Deliverable 9
-------------
Deliverable program that interacts with database to fill.

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
import re
import operator


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
        genes_list = []
        columns = []
        header_names = ["chromosome", "reference", "RefSeq_Gene", "RefSeq_Func", "dbsnp138",
                        "1000g2015aug_EUR", "LJB2_SIFT", "LJB2_PolyPhen2_HDIV",
                        "LJB2_PolyPhen2_HVAR",
                        "CLINVAR"]

        with open(anno_file) as tsv_file:  # Open TSV file
            lines = tsv_file.readlines()

        header = lines[0].strip().split("\t")  # The header line

        for col in header_names:
            columns.append(header.index(col))  # Indices of the columns needed in one list

        getter = operator.itemgetter(*columns)  # Create getter function
        header = getter(header)  # Get the headers

        for line in lines:  # Iterate through the TSV lines
            if line.startswith("chromosome"):  # Skip the header line
                continue
            line = line.strip("\n").split("\t")  # Split the line
            line = list(getter(line))  # Get the necessary columns
            line[2] = self._regex_parsing(line[2])  # Overwrite gene data with parsed gene name
            gene_data = dict(zip(header, line))  # Write data into a dictionary
            genes_list.append(gene_data)  # Put dictionary into a list

        return genes_list

    @staticmethod
    def _regex_parsing(genes):
        """
        Function from deliverable 6-7 to parse gene data
        :param genes: gene name from ANNOVAR data
        :return: parsed gene
        """
        if genes:  # Pass last NoneType
            genes = genes.strip("\"")  # Strip the quotes around the input
            if ";" in genes:  # Replace semicolon with comma
                genes = genes.replace(";", ",")

            if "NONE" or "LOC" or "LINC" in genes:  # Look for NONE LOC LINC
                pattern = r"NONE\(dist=NONE\)|LOC\d+[,]?|LINC\d+[,]?|\(dist=\d+\)|\(N.*"
                cleared = re.sub(pattern, "", genes)  # Replace with regex

                # Delete unnecessary commas
                if cleared == ",":
                    result = cleared.replace(",", "-")
                    return result

                if cleared == "":
                    result = "-"
                    return result

                if cleared.startswith(",") or cleared.endswith(","):
                    result = cleared.strip(",")
                    return result

                if "," in cleared:
                    result = cleared.replace(",", "/")
                    return result

                return cleared

            result = genes.split("(")[0]
            return result

    def data_to_db(self, config, gene_data):
        """
        Function to connect to database and put data in
        :param config: login credentials
        :param gene_data: parsed ANNOVAR data
        :return:
        """
        pass

