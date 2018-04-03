#############################################
# Generating pdbqts from mol2 using MGLTools#
#############################################

# Usage: python mol2pdbqt.py <dude_receptor_dir> num_processes

import glob
from multiprocessing import Pool
import os
from subprocess import call
import sys
import time

# MGLTools environment
PIPELINE_DIR = os.path.dirname(os.path.realpath(__file__))
os.environ['MGL_ROOT'] = PIPELINE_DIR + "/MGLTools"

 
def convert2pdbqt(ligand):
    """Uses MGLTools to convert a ligand to pdbqt."""
    root_name = os.path.splitext(ligand)[0]
    print(root_name)
    # Split ligand
    call(["MGLTools/bin/pythonsh",
          "MGLTools/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_ligand4.py",
          "-l", ligand, "-o", root_name + ".pdbqt"])


if __name__ == "__main__":
    # User inputs
    target_path = sys.argv[1]
    n_cpus = int(sys.argv[2])
    # Generate list of ligands
    actives = glob.glob(target_path + "actives/*.mol2")
    decoys = glob.glob(target_path + "decoys/*.mol2")
    ligands = actives + decoys
    # Start process pool
    pool = Pool(processes=n_cpus)
    start_time = time.time()
    # Run for each ligand
    pool.map(convert2pdbqt, ligands)
    stop_time = time.time()
    print("Job completed in:", stop_time - start_time, "seconds")
