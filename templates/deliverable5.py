#!/usr/bin/env python3

import argparse

"""
BFV2 Theme 05 - Genomics - Sequencing Project

Template for parsing and filtering VCF data given a certain variant
allele frequency value.

Deliverable 8
-------------
Make changes to the `parse_vcf_data` function AND the `main` function,
following the instructions preceded with double '##' symbols.

    usage:
        python3 deliverable8.py vcf_file.vcf frequency out_file.vcf

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
__version__ = "2017.d8.v3"

# IMPORT
import sys

def parse_vcf_data(vcf_input_file, frequency, vcf_output_file):
    """ This function reads the input VCF file line by line, skipping the first
    n-header lines. The remaining lines are parsed to filter out variant allele
    frequencies > frequency.
    """

    ## Open the INTPUT VCF file, read the contents line-by-line
    ## Write the first ... comment-lines (header) directly to the output file

    ## Compare the 'FREQ' field with the `frequency` value and write the line
    ## to the output file if FREQ > frequency
    pass

# MAIN
def main(args):
    """ Main function """

    ### INPUT ###
    # Try to read input arguments from the commandline.
    # *After* testing, make sure the program gives proper errors if input is missing

    ## Change the handling of input/ output to using the `argparse` library
    if len(args) > 1:
        pass
    else:
        print('Warning, no arguments given, using default values (testing only)...')
        vcf_file = 'data/example.vcf'
        out_vcf = 'data/d8_output.vcf'
        frequency = 30

    # Process the VCF-file
    parse_vcf_data(vcf_file, frequency, out_vcf)

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
