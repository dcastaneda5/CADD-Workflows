#!/bin/bash
#
# SLURM script for docking with smina.
#-------------------------------------------------------
#SBATCH -J mgltools
#SBATCH -N 1 -n 128
#SBATCH -p development
#SBATCH -o %j.out
#SBATCH -e %j.err
#SBATCH -t 00:30:00
#SBATCH -A VinaXB
#SBATCH --mail-user=ravila11@miners.utep.edu
#SBATCH --mail-type=all
#------------------------------------------------------

module purge
module load TACC

python mol2pdbqt.py $1 128
