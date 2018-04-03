#! /usr/bin/env python3

import argparse
import glob
import os
import shutil
import split_mol2
import subprocess
import sys

PIPELINE_DIR = os.path.dirname(os.path.realpath(__file__))
os.environ['MGL_ROOT'] = PIPELINE_DIR + "/MGLTools"

parser = argparse.ArgumentParser(
        description="A pipeline for docking/rescoring using DUD-E.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

# Define commandline arguments
parser.add_argument("-w", "--work_dir", help="DUD-E working directory.")
parser.add_argument("-r", "--receptor", help="Name of receptor.")
parser.add_argument("--split", dest='split', action='store_true',
                    help="Split mol2 files.")
parser.add_argument("--convert", dest='convert', action='store_true',
                    help="Convert to pdbqt.")
parser.add_argument("--dock", dest='dock', action='store_true',
                    help="Dock ligands.")
parser.add_argument("--rescore", dest='rescore', action='store_true',
                    help="Rescore ligands.")
parser.add_argument("--cpus", type=int, default=1280,
                    help="Number of SLURM processors for docking and " +
                    "rescoring. (Number of nodes is cpus / 64)")
parser.set_defaults(split=False)
parser.set_defaults(convert=False)
parser.set_defaults(dock=False)
parser.set_defaults(rescore=False)

args = parser.parse_args()


def download(target_dir):
    """Download DUD-E target files."""
    print("Downloading DUD-E files for", args.receptor)
    url = "dude.docking.org/targets/" + args.receptor + "/"
    files = ["receptor.pdb", "decoys_final.mol2.gz",
             "actives_final.mol2.gz", "crystal_ligand.mol2"]
    for f in files:
        subprocess.Popen(['wget', url + f], cwd=target_dir).wait()


def move_decoys_actives(target, extension):
        """Create subfolders for decoys and actives."""
        actives_dir = target + "/actives"
        decoys_dir = target + "/decoys"
        if not os.path.exists(actives_dir):
            os.makedirs(actives_dir)
        for file in glob.iglob(target + "/actives*." + extension):
            shutil.move(file, actives_dir)
        if not os.path.exists(decoys_dir):
            os.makedirs(decoys_dir)
        for file in glob.iglob(target + "/decoys*." + extension):
            shutil.move(file, decoys_dir)


def split(target_dir):
    """Split mol2 files."""
    print("Splitting actives")
    split_mol2.split(target_dir + "/actives_final.mol2.gz")
    print("Splitting decoys")
    split_mol2.split(target_dir + "/decoys_final.mol2.gz")
    # Move actives and decoys
    move_decoys_actives(target_dir, "mol2")


def convert_receptor(target_dir):
    """Convert a receptor to pdbqt."""
    pdb = target_dir + "/receptor.pdb"
    print("Converting receptor to pdbqt")
    # Delete HN atoms
    subprocess.Popen(["sed", "-i", "/HN/d", pdb], cwd=target_dir).wait()
    # Convert using MGLTools
    subprocess.Popen([PIPELINE_DIR + "/MGLTools/bin/pythonsh", PIPELINE_DIR +
                      "/MGLTools/MGLToolsPckgs/AutoDockTools/Utilities24" +
                      "/prepare_receptor4.py", "-r", pdb],
                      cwd=target_dir).wait()
    print("Done.")


def convert_ligands(target_dir):
    """Convert ligands to pdbqt."""
    subprocess.Popen(["sbatch", "--wait",
                      PIPELINE_DIR + "/mol2pdbqt.slurm", target_dir],
                      cwd=target_dir).wait()
    # Move converted ligands
    move_decoys_actives(target_dir, "pdbqt")


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
        flag = input("Target is not in working directory. Download? (Y/n)")
        if flag.lower() == 'n':
            sys.exit()
        else:
            os.makedirs(target_dir)
            download(target_dir)
    # Split the mol2 files
    if args.split:
        split(target_dir)
    # Convert to pdbqt
    if args.convert:
        convert_receptor(target_dir)
        #convert_ligands(target_dir)
