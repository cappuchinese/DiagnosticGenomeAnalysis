#!/usr/bin/env python3

"""
BFV2 Theme 05 - Genomics - Sequencing Project

Template for filtering Gene names from the 'RefSeq_Gene' column given
in ANNOVAR output files.

Deliverable 7
-------------
Make changes to the 'get_gene_name' function

    usage:
        python3 deliverable7.py
"""

# METADATA VARIABLES
__author__ = "Marcel Kempenaar"
__status__ = "Template"
__version__ = "2018.d7.v1"

# IMPORT
import sys
import re

def get_gene_name(gene_name):
    """
    This function returns the gene name from a complex 'RefSeq_Gene' field
    from the ANNOVAR output.
    'LOC****' (Uncharacterized Locus),
    'LINC****' (Long Intergenic Non-Coding RNA segments) and
    'NONE' elements are filtered out. The LOC and LINC elements can be searched
    on http://rnacentral.org/ for further information.

    If a record contains multiple gene-names (incase of an intergenic variant),
    combine these genes with a '/' delimeter, i.e.: 'BIN1/CYP27C1'

    If a record only contains 'NONE', 'LOC' or 'LIN' elements, the gene name
    becomes a '-'.

    Input is a single RefSeq_Gene record (String) and the output is a single
    string with the filtered gene name. Review the input/output examples in
    the main function below and execute this program before making any changes.
    """

    matches = re.match(r"RefSeq: .+", gene_name)
    for match in matches:
        match.split(",")

    ## Remove the following print() statement after the first time
    print("**INPUT GENE**:", gene_name)
    gene = ''
    # Process ...
    return gene


######
# Do not change anything below this line
######

# MAIN
def main(args):
    """ Main function """

    ### INPUT ###
    refseq_genes = [
        'TNNI3(NM_000363:exon5:c.371+2T>A)',
        'TSHZ3(dist=65732),THEG5(dist=173173)',
        'ACTR3BP2(dist=138949),NONE(dist=NONE)',
        'BIN1(dist=32600),CYP27C1(dist=43909)',
        'LOC101927282(dist=1978702),LOC101927305(dist=14658)',
        'NBPF10,NBPF20',
        'ERBB4',
        'LOC100507291',
        'NONE'
    ]

    ### OUTPUT ###
    genes = [
        'TNNI3',
        'TSHZ3/THEG5',
        'ACTR3BP2',
        'BIN1/CYP27C1',
        '-',
        'NBPF10/NBPF20',
        'ERBB4',
        '-',
        '-'
    ]
    # Process the ANNOVAR-file
    fail = 0
    for i, refseq_gene in enumerate(refseq_genes):
        filtered_gene = get_gene_name(refseq_gene)
        print("Input RefSeq_Gene: '", refseq_gene, "', Filtered gene name: '",
              filtered_gene, "'", sep='')
        if filtered_gene != genes[i]:
            print("\tUnfortunately, '", filtered_gene,
                  "' (your output) is different from the expected output ('",
                  genes[i], "').\n", sep='')
            fail = 1
        else:
            print('\tWell done! The gene name is correct.')

    if fail == 1:
        print('\nNot all genes are filtered correctly, please review',
              'the list above and try again.')
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
