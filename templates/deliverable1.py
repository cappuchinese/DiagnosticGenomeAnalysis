#!/usr/bin/env python3

"""
BFV2 Theme 05 - Genomics - Sequencing Project

Simple template for parsing BED data and printing information about
the exons contained within this data.

Deliverable 1
-------------
Make changes to the 'parse_bed_data' function,
following the instructions preceded with double '##' symbols.

(Change the metadata for each of the deliverables)

    usage:
        python3 deliverable1.py
"""

# METADATA VARIABLES [change these where necessary!]
__author__ = "Marcel Kempenaar"
__status__ = "Template"
__version__ = "2017.d1.v2"

# IMPORT
import sys

# FUNCTIONS
def parse_bed_data(bed_data):
    """ Function that parses BED data and prints its contents """
    ## Iterate over the `bed_data` contents and print details for each exon
    ## in the following format:
    ##      chromosome: 10, start: 10, stop: 1000, name: SOD2
    pass

######
# Do not change anything below this line
######

# MAIN
def main(args):
    """ Main function """
    # Create a small subset of data (9 exons for 3 genes on 3 chromosomes)
    bed_data = [
        "1	237729847	237730095	RYR2",
        "1	237732425	237732639	RYR2",
        "1	237753073	237753321	RYR2",
        "18	28651551	28651827	DSC2",
        "18	28654629	28654893	DSC2",
        "18	28659793	28659975	DSC2",
        "X	153648351	153648623	TAZ",
        "X	153648977	153649094	TAZ",
        "X	153649222	153649363	TAZ"
    ]

    parse_bed_data(bed_data)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))