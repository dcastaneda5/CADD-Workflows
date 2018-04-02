import argparse
import glob
import os
import subprocess
import sys


parser = argparse.ArgumentParser(
        description="A pipeline for docking/rescoring using DUD-E.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

# Define commandline arguments
parser.add_argument("-w", "--work_dir", help="DUD-E working directory.")
parser.add_argument("-r", "--receptor", help="Name of receptor.")
parser.add_argument("--split", type=bool, default=False,
                    help="Split mol2 files.")
parser.add_argument("--convert", type=bool, default=False,
                    help="Convert to pdbqt.")
parser.add_argument("--dock", type=bool, default=False,
                    help="Dock ligands.")
parser.add_argument("--rescore", type=bool, default=False,
                    help="Rescore ligands.")
parser.add_argument("--cpus", type=int, default=1280,
                    help="Number of SLURM processors for docking and " +
                    "rescoring. (Number of nodes is cpus / 64)")

args = parser.parse_args()


def download(target_dir):
    """Download DUD-E files."""
    print("Downloading DUD-E files for", args.receptor)
    url = "dude.docking.org/targets/" + args.receptor + "/"
    files = ["receptor.pdb", "decoys_final.mol2.gz",
             "actives_final.mol2.gz", "crystal_ligand.mol2"]
    for f in files:
        subprocess.Popen(['wget', url + f], cwd=target_dir).wait()


def split(target_dir):
    """Split mol2 files."""
    import split_mol2
    from organize_folders import move_decoys_actives
    print("Splitting actives")
    split_mol2.split(target_dir + "/actives_final.mol2.gz")
    print("Splitting decoys")
    split_mol2.split(target_dir + "/decoys_final.mol2.gz")
    # Make direcories to store mol2 files
    os.makedirs(target_dir + "/actives")
    os.makedirs(target_dir + "/decoys")
    # Move actives and decoys
    move_decoys_actives(target_dir)


if __name__ == "__main__":
    # Check if working directory exists
    if args.work_dir is None or args.receptor is None:
        print("You must supply a working directory and receptor.")
        sys.exit()
    if not os.path.exists(args.work_dir):
        print("Working directory does not exist.")
        sys.exit()
    target_dir = args.work_dir + args.receptor
    # Download the receptor if not in working directory
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        download(target_dir)
    # Split the mol2 files
    if args.split:
        split(target_dir)
    # Convert to pdbqt
    ig args.convert:
        convert_receptor(target_dir)
        convert_ligands(target_dir)

