#!/usr/bin/env python3

"""
BFV2 Theme 05 - Genomics - Sequencing Project

Deliverable 6 and 7
-------------------
Program for parsing and filtering ANNOVAR data. Filtering gene names from 'RefSeq_Gene' with Regex.

    Usage:
        python3 deliverable6.py
"""

# META VARIABLES
__author__ = "Lisa Hu"
__status__ = "In progress"
__version__ = "2021.d6-7.v1"

# IMPORT
# Uncomment to use in terminal
# import sys
# import argparse
import operator
import re
import csv


def parse_tsv(filename):
    """
    Open TSV file and parse
    :param filename:
    :return:
    """
    with open(filename) as tsv_file:  # Open TSV file
        lines = tsv_file.readlines()

    header = lines[0].strip().split("\t")  # The header line

    genes_list = []
    columns = []
    header_names = ["chromosome", "reference", "RefSeq_Gene", "RefSeq_Func", "dbsnp138",
                    "1000g2015aug_EUR", "LJB2_SIFT", "LJB2_PolyPhen2_HDIV", "LJB2_PolyPhen2_HVAR",
                    "CLINVAR"]

    for col in header_names:
        columns.append(header.index(col))

    getter = operator.itemgetter(*columns)
    header = getter(header)

    for line in lines:  # Iterate through the TSV lines
        if line.startswith("chromosome"):  # Skip the header line
            continue
        line = line.strip("\n").split("\t")
        line = list(getter(line))
        line[2] = re_test(line[2])
        test = dict(zip(header, line))
        genes_list.append(test)

    return genes_list

    # Uncomment for printed summary
    # result_list = []
    #     line = line.split("\t")  # Split per tabular
    #     for col in summary:  # The output header line
    #         result_list.append(f"{header[col]}: {line[col]}\t")
    #         if col == 16:  # Newline after the last header
    #             result_list.append("\n")
    #     for column in data_lines:  # The rest of the data
    #         result_list.append(f"\t{header[column]}: {line[column]}\n")
    # results = "".join(result_list)
    # print(results)


def re_test(genes):
    """
`   Gene name parsing using regex
    :param genes:
    :return:
    """
    if genes:  # Pass last NoneType
        genes = genes.strip("\"")  # Strip the quotes around the input
        if ";" in genes:  # Replace semicolon with comma
            genes = genes.replace(";", ",")

        if "NONE" or "LOC" or "LINC" in genes:  # Look for NONE LOC LINC
            pattern = r"NONE\(dist=NONE\)|LOC\d+[,]?|LINC\d+[,]?|\(dist=\d+\)|\(N.*"
            cleared = re.sub(pattern, "", genes)  # Replace with regex

            # Delete unnecessary commas and
            if cleared == ",":
                result = cleared.replace(",", "-")
                return result

            elif cleared == "":
                result = "-"
                return result

            elif cleared.startswith(",") or cleared.endswith(","):
                result = cleared.strip(",")
                return result

            elif "," in cleared:
                result = cleared.replace(",", "/")
                return result

            else:
                return cleared

        else:
            result = genes.split("(")[0]
            return result


def write_to_csv(genes_list):
    """
    Write out all the dictionaries of data into text-file
    :param genes_list:
    :return:
    """
    with open("data/d6_7_output.csv", "w") as out_file:
        fc = csv.DictWriter(out_file, fieldnames=genes_list[0].keys())
        fc.writeheader()
        fc.writerows(genes_list)


def main():
    """ Main function """

    # Process the TSV file
    genes = parse_tsv("data/Galaxy30-[_ANNOVAR_Annotated_variants_on_data_26].tsv")
    write_to_csv(genes)


if __name__ == "__main__":
    main()

    # Uncomment to use in terminal
    # Args parser (uncomment to use in terminal)
    # parser = argparse.ArgumentParser()
    # parser.add_argument("input", help="input tsv file")
    #
    # args = parser.parse_args()

    # parse_tsv(args.input)


# if __name__ == "__main__":
#     sys.exit(main(sys.argv))
