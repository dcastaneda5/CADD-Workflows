##################################################
# Script for docking DUD-E compounds in parallel #
##################################################

# Usage: python dock.py <dude_receptor_dir> num_processes
# e.g. dock.py DUD-E/all/ampc/ 64

import glob
from Queue import Queue
from os import path
from subprocess import Popen
import sys
import time

SMINA_PATH="./smina"

# User inputs
target_path = sys.argv[1].rstrip("/")
n_cpus = int(sys.argv[2])
    
# Docking parameters
receptor = target_path + "/receptor.pdbqt"
crystal_ligand = target_path + "/crystal_ligand.mol2"
actives = glob.glob(target_path + "/actives/*.pdbqt")
decoys = glob.glob(target_path + "/decoys/*.pdbqt")
ligands = actives + decoys
num_modes = 12
start_time = time.time()

# Initialize queue
q = Queue(maxsize=n_cpus)

start_time = time.time()
while len(ligands) != 0:
    while not q.full():
        ligand = ligands.pop()
        ligname = path.splitext(ligand)[0]
        # Start subprocess
        p = Popen([SMINA_PATH, "-r", receptor, "-l", ligand, "--autobox_ligand",
                   crystal_ligand, "--num_modes", str(num_modes), "-o",
                   ligname + "_out.pdbqt", "--cpu", "1"])
        # Add to queue
        q.put(p)
    # Get first item and check if it finished
    top = q.get()
    poll = top.poll()
    if poll == None:
        # Process is alive
        q.put(top)
    q.task_done()
q.join()

stop_time = time.time()
print("Job completed in:", stop_time - start_time, "seconds")
