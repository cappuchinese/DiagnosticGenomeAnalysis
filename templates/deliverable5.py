#!/usr/bin/env python3

"""
BFV2 Theme 05 - Genomics - Sequencing Project

Simple template for processing the parsed BED and pileup data. The output of
this script is the per-gene information regarding the coverage (read depth).

Deliverable 5
-------------
Make changes to the 'calculate_mapping_coverage' function, following the instructions
preceded with double '##' symbols.

    usage:
        python3 deliverable5.py
"""

# METADATA VARIABLES
__author__ = "Marcel Kempenaar"
__status__ = "Template"
__version__ = "2017.d5.v2"

# IMPORT
import sys

# FUNCTIONS
def calculate_mapping_coverage(coverage_dict):
    """ Function to calculate all coverage statistics on a per-gene basis """

    ## Remove this print statement after the first time executing this program
    print('Input coverage dictionary:', coverage_dict)

    ## Iterate over all the genes in the coverage_dict getting the gene name
    ## and list with coverage data for that gene

    ## Print a single line with:
    ##      * Gene name,
    ##      * Total positions (gene length covered)
    ##      * Average Coverage (use round) and
    ##      * number of low-coverage positions (coverage value < 30)
    pass

# MAIN
def main(args):
    """ Main function with example input data (pileup and parsed bed)"""

    ### INPUT ###
    coverage_dict = {
        "SOB2" : [99, 100, 100, 100, 100, 100, 100, 101, 110, 110, 110, 100, 99, 98],
        "NEXN" : [256, 266, 233, 255, 345, 355, 344, 222, 399, 200, 199, 263, 234, 133, 165, 176],
        "TCAP" : [50, 51, 55, 23, 43, 23, 33, 24, 53, 24, 30, 33, 37, 37]
    }

    # Call the calculate-function
    calculate_mapping_coverage(coverage_dict)

    # FINISH
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
