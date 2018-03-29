#!/bin/bash
#
# SLURM script for docking with smina.
#-------------------------------------------------------
#SBATCH -J mgltools
#SBATCH -N 5 -n 640
#SBATCH -p normal
#SBATCH -o %j.out
#SBATCH -e %j.err
#SBATCH -t 00:15:00
#SBATCH -A VinaXB
#SBATCH --mail-user=ravila11@miners.utep.edu
#SBATCH --mail-type=all
#------------------------------------------------------

# Suggested nodes:

module purge
module load TACC

python mol2pdbqt.py $1 640

