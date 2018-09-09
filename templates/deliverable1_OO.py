#!/usr/bin/env python3

"""
BFV2 Theme 05 - Genomics - Sequencing Project

Template for parsing BED data and storing this data in a dictionary with the
chromosomes as keys.

    This program uses two classes (BED and Exon) as an exercise and
refresher for programming with objects. Some of the more advanced methods
are already given, later deliverables require to write these yourselves.

    Take good care to study this program before you start editing. Note that
this program can already be executed and it will properly report the difference
between the given output and the expected output.

Deliverable 1 - Object Oriented Version
---------------------------------------
Make changes to the 'BED' and 'Exon' classes and the `bed_to_datastructure` function,
following the instructions preceded with double '##' symbols.

    usage:
        python3 deliverable1.py
"""

# METADATA VARIABLES
__author__ = "Marcel Kempenaar"
__status__ = "Template"
__version__ = "2017.d1oo.v3"

# IMPORTS
import sys


class BED(object):
    """ BED object for parsing and storing exon data from a BED file

        Assignment: complete all methods that only have a 'pass' statement """

    def __init__(self):
        # Storage for all exons from the file or data object
        self.exons = []
        # Positional index used with the __iter__() function
        self.exon_index = 0

    def read_bed_file(self, filename):
        """ Opens a BED file given the filename and calls the
            _parse_bed_line() function for each line """
        pass

    def parse_bed_data(self, bed_data):
        """ Calls the _parse_bed_line() function for each item
            in the provided bed_data list """
        pass

    def _parse_bed_line(self, bed_line):
        """ Parses (splits) a single line for a BED file and adds
            a single exon to self.exons by calling _add_exon(). """
        pass

    def _add_exon(self, exon_data):
        """ Creates an Exon object given the fields from a line of
            exon data read from a BED file. Calls the Exon.define_from_bed_line()
            method to fill its data member """
        pass

    def __iter__(self):
        return self

    def __next__(self):
        """ Enables iterating over all found Exons. """
        try:
            exon = self.exons[self.exon_index]
        except IndexError:
            raise StopIteration
        self.exon_index += 1
        return exon

    def __getitem__(self, exon_index):
        """ Access the self.exons list by a given index """
        return self.exons[exon_index]

    def __str__(self):
        """ Returns a string representation of the BED object by formatting the
            Exon data. """
        exons_representation = []
        for exon in self.exons:
            exons_representation.append('chromosome: {}, start: {}, stop: {}, name: {}'
                                        .format(*exon.get_content_tuple()))
        return '\n'.join(exons_representation)


class Exon(object):
    """ Simple data structure-class to hold information about an exon

        Assignment: complete all methods that only have a 'pass' statement

        Bonus: use the 'pythonic' way of setting the class properties. Use
        the '@property' and '@<property>.setter' decorators. """

    def define_from_bed_line(self, exon_contents):
        """ Set the parameters from a list of exon elements
            Note: these elements are still strings """
        pass

    def get_content_tuple(self):
        """ Return the object contents in a tuple """
        pass

    def __str__(self):
        """ Return a custom string representation of the object """
        return 'chromosome: {}, start: {}, stop: {}, name: {}'.format(*self.get_content_tuple())

# FUNCTIONS
def bed_to_datastructure(bed_data):
    """ Function that parses BED data and stores its contents
        in a dictionary
    """

    ## Create empty dictionary to hold the data
    bed_dict = {}

    ## Create a BED object and call the parse_bed_data() method

    ## For each exon (remember that our BED object is an iterable),

        ## check if the 'chromosome' is already in the dictionary

            ## If True, append the start, stop and name as a tuple

            ## If False, add a new key using the chromosome and a list
            ## containing a tuple with the start, stop and name as value

    return bed_dict


######
# Do not change anything below this line
######

# MAIN
def main(args):
    """ Main function that tests for correct parsing of BED data """
    ### INPUT ###
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

    ### OUTPUT ###
    expected_bed_dict = {
        '1':  [(237729847, 237730095, 'RYR2'),
               (237732425, 237732639, 'RYR2'),
               (237753073, 237753321, 'RYR2')],
        '18': [(28651551, 28651827, 'DSC2'),
               (28654629, 28654893, 'DSC2'),
               (28659793, 28659975, 'DSC2')],
        'X':  [(153648351, 153648623, 'TAZ'),
               (153648977, 153649094, 'TAZ'),
               (153649222, 153649363, 'TAZ')]}

    bed_dict = bed_to_datastructure(bed_data)
    _assert_output_vs_expected(bed_dict, expected_bed_dict)

    # FINISH
    return 0

def _assert_output_vs_expected(output, expected):
    """ Compares given output with expected output.
    Do not modify. """
    import unittest
    if isinstance(output, dict):
        testcase = unittest.TestCase('__init__')
        try:
            testcase.assertDictEqual(expected, output,
                                     msg="\n\nUnfortunately, the output is *not* correct..")
        except AssertionError as error:
            print(error)
            return 0
        print("\nWell done! Output is correct!")
        return 1
    print("\n\nUnfortunately, the output is *not* a dictionary!")
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
