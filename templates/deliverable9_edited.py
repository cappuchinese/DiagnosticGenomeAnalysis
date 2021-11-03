#!/usr/bin/env python3

"""
BFV2 Theme 05 - Genomics - Sequencing Project

Deliverable 9
-------------
Deliverable program that interacts with database to fill.

    usage:
        python3 deliverable9.py database_host database_username database_name
            database_password ANNOVAR_file
    version:
        python 3.10
"""

__author__ = "Lisa Hu"
__version__ = "2021.d9.v1"

# IMPORTS
import sys
import re
import operator
import mariadb

from Argsparsing import _args_parsing


class AnnoParser:
    """
    Parsing the ANNOVAR file
    """

    def __init__(self, anno_file):
        self.anno_file = anno_file

    def open_file(self):
        """
        Open ANNOVAR file
        :return:
        """
        with open(self.anno_file, "r", encoding="utf8") as tsv_file:  # Open TSV file
            lines = tsv_file.readlines()

        return lines

    def parse_annovar(self):
        """
        Function from deliverable 6-7 to parse data
        :return: Parsed ANNOVAR data
        """
        genes_list = []
        columns = []
        header_names = ["chromosome", "reference", "RefSeq_Gene", "RefSeq_Func", "dbsnp138",
                        "1000g2015aug_EUR", "LJB2_SIFT", "LJB2_PolyPhen2_HDIV",
                        "LJB2_PolyPhen2_HVAR",
                        "CLINVAR"]

        lines = self.open_file()

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
                # if cleared == ",":
                #     result = cleared.replace(",", "-")
                #     return result
                # if cleared == "":
                #     result = "-"
                #     return result
                match cleared:
                    case ",":
                        return re.sub(",", "-", cleared)
                    case "":
                        return "-"
                    case _:
                        if cleared.startswith(",") or cleared.endswith(","):
                            result = cleared.strip(",")
                            return result
                        if "," in cleared:
                            result = cleared.replace(",", "/")
                            return result

                        return cleared

            result = genes.split("(")[0]
            return result


class DatabaseConnector:
    """
    # TODO fill DocString
    """

    def __init__(self, argvs, anno_data):
        self.anno_data = anno_data
        self.args = argvs

    def run(self):
        """
        Main function to run program
        :return:
        """
        config = {
            "host": self.args.host,
            "user": self.args.user,
            "password": self.args.password,
            "database": self.args.database,
        }
        self.data_to_db(config, self.anno_data)

    def data_to_db(self, config, gene_data):
        """
        Function to connect to database and put data in
        :param config: login credentials
        :param gene_data: parsed ANNOVAR data
        :return:
        """
        try:
            connector = mariadb.connect(host=config["host"], user=config["user"],
                                        passwd=config["password"], db=config["database"])
            cursor = connector.cursor()

            with open("deliverable8.sql", "r") as sql_file:
                sql_string = sql_file.read()

            cursor.execute(sql_string)

        except mariadb.Error as err:
            print(f"Error with the database:\n{err}")

        for item, variant in enumerate(gene_data):
            chr_flag = cursor.execute(f"SELECT count('chromosome') FROM Chromosome "
                                      f"WHERE chromosome={variant['chromosome']}")
            gene_flag = cursor.execute(f"SELECT count({variant['RefSeq_Gene']}) FROM Genes "
                                       f"WHERE chromosome={variant['RefSeq_Gene']}")
            if chr_flag == 0:
                gene_data[item]["chr_id"] = self._insert_data(cursor, "Chromosome", variant)
            if gene_flag == 0:
                gene_data[item]["gene_id"] = self._insert_data(cursor, "Genes", variant)

            self._insert_data(cursor, "Variants", variant)

        connector.commit()
        connector.close()

    @staticmethod
    def _insert_data(cursor, table, columns):
        """
        Adds the chromosome to the chromosome table
        :param cursor: database cursor
        :param table: table name
        :param columns: data
        :return:
        """
        cursor.execute(f"INSERT INTO {table} ({', '.join(columns)}) "
                       f"VALUES ({', '.join([k for k in columns])})")

        return cursor.lastrowid


if __name__ == "__main__":
    args = _args_parsing()
    anno_data = AnnoParser.parse_annovar(args)
    ing = DatabaseConnector(args, anno_data)
    sys.exit(ing.run())
