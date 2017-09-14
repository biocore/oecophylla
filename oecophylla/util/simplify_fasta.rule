#!/usr/bin/env python
"""
Program to simplify fasta headers.

Optionally returns a conversion table to old headers.
"""
import argparse

parser = argparse.ArgumentParser(description=__doc__,
                            formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('fasta_fp', help="input fasta file")

parser.add_argument('-o', '--output_fp', 
    type=str,
    help='output simplified fasta file [Default: STDOUT]')

parser.add_argument('-t', '--header_fp', 
    type=str,
    help='output file for header lookup [Default: Not written]')

parser.add_argument('-p', '--prepend', 
    type=str, default='sequence_',
    help='text to prepend to index')

def simplify_headers(fasta_fp, prepend='sequence_',
                     output_fp=None, header_fp=None):
    """
    Function to simplify fasta headers.
    """
    if output_fp:
        o_f = open(output_fp, 'w')
    if header_fp:
        h_f = open(header_fp, 'w')

    with open(fasta_fp) as fa:
        i = 0
        for line in fa:
            if line.startswith('>'):
                old_header = line.strip()[1:]
                new_header = prepend + str(i)

                outline = ">{0}".format(new_header)

                i += 1
            else:
                outline = line.strip()

            if header_fp:
                h_f.write("{0}\t{1}\n".format(new_header, old_header))
            if output_fp:
                o_f.write(outline + '\n')
            else:
                print(outline)

    if output_fp:
        o_f.close()
    if header_fp:
        h_f.close()

    return


def main():

    args = parser.parse_args()

    fasta_fp = args.fasta_fp
    output_fp = args.output_fp
    header_fp = args.header_fp
    prepend = args.prepend

    simplify_headers(fasta_fp, prepend=prepend,
                     output_fp=output_fp, header_fp=header_fp)


if __name__ == "__main__":
    main()
