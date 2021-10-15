#!/usr/bin/env python3

"""
BFV2 Theme 05 - Genomics - Sequencing Project

Program for parsing and filtering ANNOVAR data.
"""

# META VARIABLES
__author__ = "Lisa Hu"
__status__ = "In progress"
__version__ = "2021.d6.v1"

# IMPORT
import operator
import sys
import argparse
import re


def parse_tsv(filename):
    """
    Open TSV file and parse
    :param filename:
    :return:
    """
    with open(filename) as tsv_file:  # Open TSV file
        lines = tsv_file.readlines()

    summary, data_lines = [0, 3, 16], [15, 27, *range(33, 36), -1]  # Columns
    header = lines[0].split("\t")  # The header line

    for line in lines:  # Iterate through the TSV lines
        if line.startswith("chromosome"):  # Skip the header line
            continue
        line = line.split("\t")
        columns = [*summary, *data_lines]
        getter = operator.itemgetter(*columns)
        header = getter(header)  # Error: Tuple index out of range
        print(header)
        zipped = zip(header, line)


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

    # return results


def re_test(results):
    """

    :param results:
    :return:
    """
    matches = re.findall(r"(RefSeq_Gene: \S+)", results)
    for match in matches:
        genes = match.split(" ")[1]
        if "," in genes:
            genes = genes.split(",")
            for gene in genes:
                if "NONE" or "LOC" or "LINC" in gene:
                    gene = re.sub(r"(NONE|LOC\d+|LINC\d+)", "-", gene)



def main():
    """ Main function """

    # Args parser (uncomment to use in terminal)
    # parser = argparse.ArgumentParser()
    # parser.add_argument("input", help="input tsv file")
    # parser.add_argument("output", help="output file?")
    #
    # args = parser.parse_args()

    # Process the TSV file
    results = parse_tsv("data/example_tsv.txt")
    re_test(results)


if __name__ == "__main__":
    main()

# Uncomment to use in terminal
# if __name__ == "__main__":
#     sys.exit(main(sys.argv))
