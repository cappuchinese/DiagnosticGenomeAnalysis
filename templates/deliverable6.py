#!/usr/bin/env python3

"""
BFV2 Theme 05 - Genomics - Sequencing Project

Program for parsing and filtering ANNOVAR data.
"""

# META VARIABLES
__author__ = "Lisa Hu"
__status__ = "Uncomplete"
__version__ = "2021.d6.v1"

# IMPORT
import sys
import argparse


def open_tsv_file(filename):
    """
    Open TSV file
    :param filename:
    :return:
    """
    with open(filename) as tsv_file:
        lines = tsv_file.readlines()
    return lines


def parse_tsv(tsv_lines):
    """
    Parse opened TSV file
    :param tsv_lines:
    :return:
    """
    summary = [0, 3, 16, 15, 16, 27, 33, 34, 35, 36, -1]
    header = tsv_lines[0].strip().split("\t")
    result_list = []
    for line in tsv_lines:
        line = line.strip("\n").split("\t")
        for col in summary:
            result_list.append(f"{header[col]}: {line[col]}")
    result_list = "\t".join(result_list)
    print(result_list)


def main():
    """ Main function """

    # Args parser
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input tsv file")
    parser.add_argument("output", help="output file?")

    args = parser.parse_args()

    # Process the TSV file
    lines = open_tsv_file(args.input)
    parse_tsv(lines)


if __name__ == "__main__":
    main()
