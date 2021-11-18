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

# IMPORTS
# Uncomment to use in terminal
# import sys
# import argparse
import operator
import re
import csv


def parse_tsv(filename):
    """
    Function that parses the ANNOVAR data
    :param filename: name of the file
    :return: list of dictionaries from ANNOVAR data
    """
    genes_list = []
    columns = []
    header_names = ["chromosome", "reference", "observed", "RefSeq_Gene", "RefSeq_Func", "dbsnp138",
                    "1000g2015aug_EUR", "LJB2_SIFT", "LJB2_PolyPhen2_HDIV", "CLINVAR"]
    num_headers = ["1000g2015aug_EUR", "LJB2_SIFT", "LJB2_PolyPhen2_HDIV"]
    num_columns = []

    with open(filename, "r", encoding="utf8") as tsv_file:  # Open TSV file
        lines = tsv_file.readlines()

    header = lines[0].strip().split("\t")  # The header line

    for col in header_names:
        columns.append(header.index(col))  # Indices of the columns needed in one list

    getter = operator.itemgetter(*columns)  # Create getter function
    header = getter(header)  # Get the headers

    gene_index = header.index("RefSeq_Gene")
    for x in num_headers:
        num_columns.append(header.index(x))

    for line in lines:  # Iterate through the TSV lines
        if line.startswith("chromosome"):  # Skip the header line
            continue
        line = line.strip("\n").split("\t")  # Split the line
        line = list(getter(line))  # Get the necessary columns
        # Split the letter value from 1000g, SIFT and PolyPhen2
        for y in num_columns:
            try:
                line[y] = float(line[y].split(",")[0])
            except ValueError:
                line[y] = None
        # Overwrite gene data with parsed gene name
        line[gene_index] = regex_parsing(line[gene_index])
        gene_data = dict(zip(header, line))  # Write data into a dictionary
        genes_list.append(gene_data)  # Put dictionary into a list

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


def regex_parsing(genes):
    """
`   Gene name parsing using regex
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


def write_to_csv(genes_list, output_file):
    """
    Write out all the dictionaries of data into a file
    :param genes_list: list of dictionaries of gene data
    :param output_file: name of output file
    :return:
    """
    with open(output_file, "w", encoding="utf8") as out_file:
        writer = csv.DictWriter(out_file, fieldnames=genes_list[0].keys())
        writer.writeheader()
        writer.writerows(genes_list)


def main():
    """ Main function """

    # Process the TSV file
    genes = parse_tsv("data/Galaxy30-[_ANNOVAR_Annotated_variants_on_data_26].tsv")
    write_to_csv(genes, "data/d6_7_output.csv")


if __name__ == "__main__":
    main()

    # Uncomment to use in terminal
    # Args parser (uncomment to use in terminal)
    # parser = argparse.ArgumentParser()
    # parser.add_argument("input", help="input tsv file")
    # parser.add_argument("output", help="output file (add file extension)")
    #
    # args = parser.parse_args()

    # genes = parse_tsv(args.input)
    # write_to_file(genes, args.output)


# if __name__ == "__main__":
#     sys.exit(main(sys.argv))
