#####################################################
# Script for rescoring DUD-E compounds with DLScore #
#####################################################

# Usage: python rescore.py <dude_receptor_dir> num_processes

from dlscore import *
from multiprocessing import Pool
import glob
from subprocess import call
import sys
import time
import pickle

VINA_PATH="./vina"
dlscore = "./dlscore.py" 


def rescore(ligand):
    """Function that calls DLScore."""
    # Call vina process
    ds = dlscore(ligand=ligand, receptor=receptor, vina_executable=VINA_PATH,
                 nb_nets=100)
    print(ds)
    print(ds.get_output())
    results.append(ds.get_output())


if __name__ == "__main__":
    # User inputs
    target_path = sys.argv[1].rstrip("/")
    n_cpus = int(sys.argv[2])
    # Parameters
    receptor = target_path + "/receptor.pdbqt"
    ligands = glob.iglob(target_path + "/actives/*_out.pdbqt")
    start_time = time.time()
    results = []
    # Start process pool
    with Pool(n_cpus) as pool:
        pool.imap(rescore, ligands, chunksize=10)
    stop_time = time.time()
    print("Job completed in:", stop_time - start_time, "seconds")
    with open(target_path + "/data.pickle", 'wb') as f:
        pickle.dump(results, f) 
