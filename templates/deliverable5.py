#!/usr/bin/env python3

"""
BFV2 Theme 05 - Genomics - Sequencing Project

Template for parsing and filtering VCF data given a certain variant
allele frequency value.

Deliverable 5
-------------
Make changes to the `parse_vcf_data` function AND the `main` function,
following the instructions preceded with double '##' symbols.

    usage:
        python3 deliverable5.py vcf_file.vcf frequency out_file.vcf

    arguments:
        vcf_file.vcf: the input VCF file, output from the varscan tool
        frequency: a number (integer) to use as filtering value
        out_file.vcf: name of the output VCF file 

    output:
        a VCF file containing the complete header (comment lines) and
        only the remaining variant positions after filtering.
"""

# METADATA VARIABLES
__author__ = "Marcel Kempenaar"
__status__ = "Template"
__version__ = "2019.d5.v1"

# IMPORT
import sys
import argparse


def parse_vcf_data(vcf_input_file, frequency, vcf_output_file):
    """ This function reads the input VCF file line by line, skipping the first
    n-header lines. The remaining lines are parsed to filter out variant allele
    frequencies > frequency.
    """

    with open(vcf_input_file, "r") as input_vcf:  # Open the INPUT VCF file
        lines = input_vcf.readlines()  # Read the contents line-by-line

    with open(vcf_output_file, "w") as output_vcf:
        for line in lines:
            # Write the first comment-lines (header) directly to the output file
            if line.startswith("##"):
                output_vcf.writelines(line)
            elif line.startswith("#C"):
                pass  # Pass the format-header line
            else:
                line = line.split()
                freq = float(line[9].split(":")[6].split("%")[0])  # Parse to get the frequency
                if freq > frequency:  #Compare the 'FREQ' field with the `frequency` value
                    output_vcf.writelines("\t".join(line) + "\n")  # Write the line to output

    return output_vcf

# MAIN
def main(args):
    """ Main function """

    ### INPUT ###
    # Try to read input arguments from the commandline.
    # *After* testing, make sure the program gives proper errors if input is missing

    if len(args) > 1:
        parser = argparse.ArgumentParser()
        parser.add_argument("input", metavar="I", type=open, nargs=1,
                            help="input vcf file")
        parser.add_argument("frequency", metavar="F", type=float, nargs=1,
                            help="frequency threshold")
        parser.add_argument("output", metavar="O", type=argparse.FileType("w"),
                            help="output vcf file")

        vcf_file = args[1]
        frequency = int(args[2])
        out_vcf = args[3]

    else:
        print('Warning, no arguments given, using default values (testing only)...')
        vcf_file = 'data/example.vcf'
        out_vcf = 'data/d5_output.vcf'
        frequency = 30

    # Process the VCF-file
    parse_vcf_data(vcf_file, frequency, out_vcf)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
