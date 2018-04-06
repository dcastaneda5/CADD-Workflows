##################################################
# Script for docking DUD-E compounds in parallel #
##################################################

# Usage: python dock.py <dude_receptor_dir> num_processes
# e.g. dock.py DUD-E/all/ampc/ 64

from multiprocessing import Pool
import glob
from os import path
from subprocess import call
import sys
import time

SMINA_PATH="./smina"


def dock(ligand):
    """Function that calls smina to dock a ligand."""
    ligname = path.splitext(ligand)[0]
    # Call vina process
    call([SMINA_PATH, "-r", receptor, "-l", ligand, "--autobox_ligand",
          crystal_ligand, "--num_modes", str(num_modes), "-o",
          ligname + "_out.pdbqt", "--cpu", "1"])


if __name__ == "__main__":
    # User inputs
    target_path = sys.argv[1].rstrip("/")
    n_cpus = int(sys.argv[2])
    # Docking parameters
    receptor = target_path + "/receptor.pdbqt"
    crystal_ligand = target_path + "/crystal_ligand.mol2"
    ligands = glob.glob(target_path + "/*/*.pdbqt")
    num_modes = 12
    start_time = time.time()
    # Start process pool
    with Pool(n_cpus) as pool:
        pool.map(dock, ligands, chunksize=10)
    stop_time = time.time()
    print("Job completed in:", stop_time - start_time, "seconds")
