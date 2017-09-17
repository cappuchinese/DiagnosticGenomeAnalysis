"""
BFV2 Theme 05 - Genomics - Sequencing Project

Template for a program performing the following steps:
----------------------------------------------------------
* Load the BED file containing the information (names, chromosome and
  coordinates of the exons) of all cardiopanel genes
* Load the pileup file containing the mapping data
* For each exon found in the BED file:
    * read the start- and end-coordinate
    * find all entries in the pileup file for this chromosome and within
      these coordinates
    * for each pileup-entry:
        * store the coverage (data from column 4)
* Given the found coverage for each position in all exons:
    * Calculate the average coverage per gene
    * Count the number of positions with a coverage < 30
* Write a report on all findings (output to Excel-like file)

Deliverable 7
-------------
This template contains a number of placeholders where you are asked to place
your own code made in previous deliverables, following the instructions
preceded with double '##' symbols.

The 'main()' functions glues all your functions into a single coherent
program that performs all required steps.

* Note: by default the 'data/example.bed' and 'data/example.pileup' files are
        used as input, but you can supply your own files on the
        commandline.

    usage:
        python3 deliverable7.py [bed-file.bed] [pileup-file.pileup]
"""

# METADATA VARIABLES
__author__ = "Marcel Kempenaar"
__status__ = "Template"
__version__ = "2017.d7.v3"

# IMPORT
import sys
import csv

# FUNCTIONS
def read_data(filename):
    """ PLACE YOUR deliverable6 'read_data' FUNCTION HERE """
    pass

def parse_bed_data(bed_data):
    """ PLACE YOUR deliverable2 'parse_bed_data' FUNCTION HERE """
    pass

def parse_pileup_data(pileup_data, bed_dict):
    """ PLACE YOUR deliverable4 'parse_pileup_data' FUNCTION HERE """
    pass

def calculate_mapping_coverage(coverage_dict):
    """ PLACE YOUR deliverable6 'calculate_mapping_coverage' FUNCTION HERE """
    pass

def save_coverage_statistics(coverage_file, coverage_statistics):
    """ PLACE YOUR deliverable6 'save_coverage_statistics' FUNCTION HERE """
    pass


######
# Do not change anything below this line
######

# MAIN
def main(args):
    """ Main function connecting all functions
        Note: the 'is None' checks that are done are only
        necessary for this program to run without error if
        not all functions are completed.
    """

    ### INPUT ###
    # Try to read input en output filenames from the commandline. Use defaults if
    # they are missing and warn if the extensions are 'wrong'.
    if len(args) > 1:
        bed_file = args[1]
        if not bed_file.lower().endswith('.bed'):
            print('Warning: given BED file does not have a ".bed" extension.')
        pileup_file = args[2]
        if not pileup_file.lower().endswith('.pileup'):
            print('Warning: given pileup file does not have a ".pileup" extension.')
        output_file = args[3]
    else:
        bed_file = 'example.bed'
        pileup_file = 'example.pileup'
        output_file = 'd7_output.csv'

    # STEP 1: Read BED data
    print('Reading BED data from', bed_file)
    bed_data = read_data(bed_file)
    if bed_data is None:
        print('No BED-data read...')
    else:
        print('\t> A total of', len(bed_data), 'lines have been read.\n')

    # STEP 2: Read Pileup data
    print('Reading pileup data from', pileup_file)
    pileup_data = read_data(pileup_file)
    if pileup_data is None:
        print('No Pileup-data read...')
    else:
        print('\t> A total of', len(pileup_data), 'lines have been read.\n')

    # STEP 3: Parsing BED data
    print('Parsing BED data...')
    bed_dict = parse_bed_data(bed_data)
    if bed_dict is None:
        print('BED-data not parsed!')
    else:
        print('\t> A total of', len(bed_dict.keys()), 'chromosomes have been stored.\n')

    # STEP 4: Parsing and filtering pileup data
    print('Parsing and filtering pileup-data...')
    coverage_dict = parse_pileup_data(pileup_data, bed_dict)
    if coverage_dict is None:
        print('Pileup data not parsed!')
    else:
        print('\t> Coverage of', len(coverage_dict.keys()), 'genes have been stored.\n')

    # STEP 5: Store calculated data
    print('Calculating coverage statistics...')
    coverage_statistics = calculate_mapping_coverage(coverage_dict)
    if coverage_statistics is None:
        print('No coverage statistics calculated!')
    else:
        print('\t> Statistics for', len(coverage_statistics), 'genes have been calculated.\n')

    # STEP 6: Write output data
    print('Writing the coverage statistics to', output_file)
    if coverage_statistics is None:
        print('Nothing to write, quitting...')
    else:
        save_coverage_statistics(output_file, coverage_statistics)
        from pathlib import Path
        csv_file_check = Path(output_file)
        if csv_file_check.is_file():
            print('\t> CSV file created, program finished.')
        else:
            print('\tCSV file', output_file, 'does not exist!')

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
