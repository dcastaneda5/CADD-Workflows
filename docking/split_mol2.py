################################################
#  Script for splitting multiligand mol2 files #
################################################

# Usage: python split_mol2.py <mol2 ligand>
import gzip
import os

def generator(mol2_file):
    mol = ""
    f = gzip.open(mol2_file, 'rt')
    for line in f:
        if line.startswith("@<TRIPOS>MOLECULE"):
            if mol != "":
                yield mol
            mol = ""
            mol += line
        else:
            mol += line
    f.close()


def split(mol2_file):
    root_name = os.path.splitext(os.path.splitext(mol2_file)[0])[0]
    for count, contents in enumerate(generator(mol2_file)):
        outfile = open(root_name + "_" + str(count).zfill(5) + ".mol2", 'w')
        outfile.write(contents)
        outfile.close()


if __name__ == "__main__":
    import sys
    split(sys.argv[1])
