################################################
#  Script for splitting multiligand mol2 files #
################################################

# Usage: python split_mol2.py <mol2 ligand>

def split_file(mol2_file):
    mol = ""
    f = open(mol2_file, 'rt')
    for line in f:
        if line.startswith("@<TRIPOS>MOLECULE"):
            if mol != "":
                yield mol
            mol = ""
            mol += line
        else:
            mol += line
    f.close()

if __name__ == "__main__":
    import sys
    file_name = sys.argv[1]
    root_name = file_name.split(".")[-2]
    for count, contents in enumerate(split_file(file_name)):
        outfile = open(root_name + "_" + str(count).zfill(5) + ".mol2", 'w')
        outfile.write(contents)
        outfile.close()
