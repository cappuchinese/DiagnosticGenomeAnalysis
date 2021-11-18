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

from argsparsing import _args_parsing


class AnnoParser:
    """
    Parsing the ANNOVAR file
    """

    def __init__(self, anno_file):
        self.anno_file = anno_file

    def file_opener(self):
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
        header_names = ["chromosome", "reference", "observed", "RefSeq_Gene", "RefSeq_Func",
                        "dbsnp138", "1000g2015aug_EUR", "LJB2_SIFT", "LJB2_PolyPhen2_HDIV",
                        "CLINVAR"]
        num_headers = ["1000g2015aug_EUR", "LJB2_SIFT", "LJB2_PolyPhen2_HDIV"]
        num_columns = []

        lines = self.file_opener()

        header = lines[0].strip().split("\t")  # The header line

        for col in header_names:
            columns.append(header.index(col))  # Indices of the columns needed in one list

        getter = operator.itemgetter(*columns)  # Create getter function
        header = getter(header)  # Get the headers

        for x in num_headers:
            num_columns.append(header.index(x))

        gene_index = header.index("RefSeq_Gene")
        for line in lines:  # Iterate through the TSV lines
            if line.startswith("chromosome"):  # Skip the header line
                continue
            line = line.strip("\n").split("\t")  # Split the line
            line = list(getter(line))  # Get the necessary columns
            # Split the letter value from 1000g, SIFT and PolyPhen2
            for y in num_columns:
                try:
                    line[y] = line[y].split(",")[0]
                except ValueError:
                    line[y] = ""
            # Overwrite gene data with parsed gene name
            line[gene_index] = self._regex_parsing(line[gene_index])
            gene_data = dict(zip(header, line))  # Write data into a dictionary
            genes_list.append(gene_data)  # Put dictionary into a list
        #print(genes_list)
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
                    result = cleared.replace(",", ",")
                    return result

                return cleared

            result = genes.split("(")[0]
            return result


class DatabaseConnector:
    """
    Module to connect with database via terminal commands.
    """

    def __init__(self, argvs, annovar_data, passwd):
        """
        Initialize
        :param argvs: terminal commands
        :param annovar_data: parse ANNOVAR data
        :param passwd: password to database
        """
        self.anno_data = annovar_data
        self.args = argvs
        self.password = passwd

    def run(self):
        """
        Main function to run program
        :return:
        """
        config = {
            "host": self.args.host,
            "user": self.args.user,
            "password": self.password,
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
            # Make connection to database
            connector = mariadb.connect(host=config["host"], user=config["user"],
                                        passwd=config["password"], db=config["database"])
            cursor = connector.cursor()

            # Open SQL script
            with open("deliverable8.sql", "r", encoding="utf8") as sql_file:
                sql_string = sql_file.read()

            # Split the file into the different commands
            commands = sql_string.replace("\n", "").replace("\t", " ").split(";")

            # Execute each command
            for command in commands:
                try:
                    cursor.execute(command+";")
                except mariadb.OperationalError:
                    print("Operational Error")
            connector.commit()

        # Catch possible errors (connection or execution of script)
        except mariadb.Error as err:
            print(f"Error with the database:\n{err}")

        for item, variant in enumerate(gene_data):
            # Check if the chromosome or gene already exist in the tables
            try:
                cursor.execute(f"SELECT * FROM Chromosomes "
                               f"WHERE chromosome='{variant['chromosome']}';")
                chr_flag = cursor.fetchone()
            except mariadb.OperationalError:
                chr_flag = None

            try:
                cursor.execute(f"SELECT * FROM Genes "
                               f"WHERE RefSeq_Gene='{variant['RefSeq_Gene']}';")
                gene_flag = cursor.fetchone()
            except mariadb.OperationalError:
                gene_flag = None

            # Insert the data if chromosome does not exist in table
            if chr_flag is None:
                gene_data[item]['chr_id'] = self._insert_data(cursor, 'Chromosomes', variant)
            # Else the chromosome id is fetched from earlier SELECT query
            else:
                gene_data[item]['chr_id'] = chr_flag[0]

            # Same as above but for Genes table
            if gene_flag is None:
                gene_data[item]['gene_id'] = self._insert_data(cursor, 'Genes', variant)
            else:
                gene_data[item]['gene_id'] = gene_flag[0]

            self._insert_data(cursor, 'Variants', variant)

            cursor.execute("UPDATE Variants SET 1000g2015aug_EUR=NULL WHERE 1000g2015aug_EUR='';")
            cursor.execute("UPDATE Variants SET LJB2_SIFT=NULL WHERE LJB2_SIFT='';")
            cursor.execute("UPDATE Variants SET LJB2_PolyPhen2_HDIV=NULL WHERE LJB2_PolyPhen2_HDIV='';")
            cursor.execute("ALTER TABLE Variants MODIFY COLUMN 1000g2015aug_EUR FLOAT;")
            cursor.execute("ALTER TABLE Variants MODIFY COLUMN LJB2_SIFT FLOAT;")
            cursor.execute("ALTER TABLE Variants MODIFY COLUMN LJB2_PolyPhen2_HDIV FLOAT;")

            connector.commit()
        connector.close()

    @staticmethod
    def _insert_data(cursor, table, data):
        """
        Adds the chromosome to the chromosome table
        :param cursor: database cursor
        :param table: table name
        :param data: variant data
        :return:
        """
        cursor.execute(f'DESCRIBE {table}')
        tdescription = cursor.fetchall()  # Get information of table

        # Get the column names from the table
        table_columns = [column[0] for column in tdescription]
        # Match with the columns in the input-data
        data_columns = [column for column in table_columns if column in data.keys()]
        # Join the values from the data
        value_query = ', '.join(f"'{data[variant_info]}'" for variant_info in data_columns)


        # Execute insert query
        cursor.execute(f"INSERT INTO {table} ({', '.join(data_columns)}) "
                       f"VALUES ({value_query});")

        return cursor.lastrowid


if __name__ == "__main__":
    args, password = _args_parsing()
    print("Parsing ANNOVAR file...")
    annoparser = AnnoParser(args.anno_file)
    anno_data = annoparser.parse_annovar()
    print("Filling database...")
    ing = DatabaseConnector(args, anno_data, password)
    sys.exit(ing.run())
