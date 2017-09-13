#!/usr/bin/env python3

"""
BFV2 Theme 05 - Genomics - Sequencing Project

Simple template for parsing and filtering pileup data.
Pileup data falling within the exons in the 'bed_dict' is printed.

Deliverable 3
-------------
Make changes to the 'parse_pileup_data' function, following the instructions
preceded with double '##' signs. Note that the indentation of these instructions
can be used for placing the code.

    usage:
        python3 deliverable3.py
"""

# METADATA VARIABLES
__author__ = "Marcel Kempenaar"
__status__ = "Template"
__version__ = "2017.d3.v2"

# IMPORT
import sys

# FUNCTIONS
def parse_pileup_data(pileup_data, bed_dict):
    """ Function that parses pileup data and prints its contents """

    ## Remove thse print statements after the first time executing this program
    print('Input pilup data: ', pileup_data)
    print('\nInput BED data: ', bed_dict)

    ## Iterate over all the lines contained in the pileup_data
    ## Extract the 'chromosome' field and remove the 'chr' text (see input)
    
    ## Iterate over all exons and check if the pileup-coordinate lies within the 
    ## exon coordinates. If so; print the pileup chromosome, position and
    ## coverage data (column 4).

# MAIN
def main(args):
    """ Main function with example input data (pileup and parsed bed)"""

    ### INPUT ###
    # Pileup data with chromosome, position, base, coverage, reads, quality
    pileup_data = [
        'chr1	839427	A	24	,,,,,,,,,,,,,,,,,,,,,,,,	BFGGGGGGGGHHGHH3AFHHIGFG',
        'chr1	237732518	T	24	,,,,,,,,,,,,,,,,,,,,,,,,	>FFFGHHHCDHHHHGF>CHHHHHA',
        'chr3	1290	T	24	,$,,,,,,,,,,,,,,,,$,,,,,,,	;FFFGGCGGFHHHFHF;FFHHHFD',
        'chr4	123383120	A	22	.....................^].	>HHHHGHHBHHFGGG5GD1ACA',
        'chr12	78383124	G	22	.$....................^].	;HBH1GFAHHHHFGDGGGFFC>',
        'chr12	78383132	C	22	.....................^].	HHHHHBHHGHHHHHGGGGFC1B',
        'chr18	28651722	A	23	......................^].	GHFHHFHGAHHHHHFGGGFFABB',
        'chr18	28659880	C	23	.......................	HHHHHHHHCHH4HHGFGGFF?BA',
        'chrX	9402753	A	23	.......................	HHHGGHG/AHHHHHHG4GBBABB'
    ]

    # BED data with chromosome (key), list of tuples with (start, stop and gene name)
    bed_dict = {
        '1':  [(237729847, 237730095, 'RYR2'),
               (237732425, 237732639, 'RYR2'),
               (237753073, 237753321, 'RYR2')],
        '18': [(28651551, 28651827, 'DSC2'),
               (28654629, 28654893, 'DSC2'),
               (28659793, 28659975, 'DSC2')]}

    # Call the parse-function
    parse_pileup_data(pileup_data, bed_dict)

    # FINISH
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
