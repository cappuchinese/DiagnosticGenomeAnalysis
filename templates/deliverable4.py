#!/usr/bin/env python3

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

Deliverable 4
-------------
This template contains a number of placeholders where you are asked to place
your own code made in previous deliverables, following the instructions
preceded with double '##' symbols.

The 'main()' functions glues all your functions into a single coherent
program that performs all required steps.

* Note: Test the program on the example data first.
* Note: by default the 'data/example.bed' and 'data/example.pileup' files are
        used as input, but you can supply your own files on the
        commandline.

    usage:
        python3 deliverable4.py [bed-file.bed] [pileup-file.pileup]
"""

# METADATA VARIABLES
__author__ = "Marcel Kempenaar"
__status__ = "Template"
__version__ = "2018.d4.v1"

# IMPORT
import sys
import csv


# FUNCTIONS
def read_data(filename):
    """ This function reads in data and returns a list containing one
        line per element. """
    opened_f = open(filename, "r")  # Open the file given the filename stored in 'filename'
    lines_list = []
    for line in opened_f:  # Iterate through lines of file
        lines_list.append(line)  # Add line to list

    opened_f.close()  # Close the file

    return lines_list  # Return a list where each line is a list element


def parse_bed_data(bed_data):
    """
    Function that parses BED data and stores its contents
        in a dictionary
    """
    # Create empty dictionary to hold the data
    bed_dict = {}

    for line in bed_data:  # Iterate through BED data
        line = line.split()

        value = (int(line[1]), int(line[2]), line[3])  # Make a tuple with data
        # Add data to dictionary as {Chromosome : [(pos1, pos2, exon), (pos1, pos2, exon)]}
        if line[0] in bed_dict:
            bed_dict[line[0]].append(value)
        else:
            bed_dict[line[0]] = []
            bed_dict[line[0]].append(value)

    return bed_dict


def parse_pileup_data(pileup_data, bed_dict):
    """
    Function that parses pileup data and collects the per-base coverage
        of all exons contained in the BED data.

    Iterate over all pileup lines and for each line:
        - check if the position falls within an exon (from `bed_dict`)
            - if so; add the coverage to the `coverage_dict` for the correct gene
    """

    # Create empty dictionary to hold the data
    coverage_dict = {}

    for line in pileup_data:
        # Loop through the pileup_data and extract the chromosome
        line = line.split("\t")
        chromosome = line[0].split("r")[1]
        if chromosome in bed_dict:
            # Save the location of the pile_coord
            pile_coord = int(line[1])
            # Loop through the bed_dict for each exon
            for exon in bed_dict[chromosome]:
                # If pile_coord is inbetween the exon location, save it to the coverage_dict
                if pile_coord in range(exon[0], exon[1]):
                    if bed_dict[chromosome][1][2] not in coverage_dict:
                        coverage_dict[bed_dict[chromosome][1][2]] = []
                        coverage_dict[bed_dict[chromosome][1][2]].append(int(line[3]))
                    else:
                        coverage_dict[bed_dict[chromosome][1][2]].append(int(line[3]))

    # Return coverage dictionary
    return coverage_dict


def calculate_mapping_coverage(coverage_dict):
    """
    Function to calculate all coverage statistics on a per-gene basis
        and store this in a list.
        Note: this function is taken from deliverable 5 and slightly modified
    """

    # Create an empty list that will hold all data to save
    statistics = []

    # Iterate over all the genes in the coverage_dict getting the gene name
    for key in coverage_dict:
        total = sum(coverage_dict[key])  # Gene length covered
        average = total/len(coverage_dict[key])  # Average coverage
        low_cov = sum(map(lambda x: x < 30, coverage_dict[key]))  # Number of low coverage
        statistics.append((key, total, average, low_cov))

    return statistics


def save_coverage_statistics(coverage_file, coverage_statistics):
    """
    Writes coverage data to a tabular file using Python's
        csv library: https://docs.python.org/3/library/csv.html#csv.writer
    """
    with open(coverage_file, "w", newline="") as write_f:
        coverage_w = csv.writer(write_f, delimiter="\t")
        for gene in coverage_statistics:
            coverage_w.writerow(gene)

    write_f.close()
    # Write the coverage_statistics to a CSV file
    return coverage_w


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
        bed_file = 'data/example.bed'
        pileup_file = 'data/example.pileup'
        output_file = 'data/d4_output.csv'

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
