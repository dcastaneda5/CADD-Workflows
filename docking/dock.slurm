#!/bin/bash
#
# SLURM script for docking with smina.
#-------------------------------------------------------
#SBATCH -J dock
#SBATCH -N 5 -n 640
#SBATCH -p normal
#SBATCH -o %j.out
#SBATCH -e %j.err
#SBATCH -t 02:00:00
#SBATCH -A VinaXB
#SBATCH --mail-user=ravila11@miners.utep.edu
#SBATCH --mail-type=all
#------------------------------------------------------

module purge
module load TACC

python dock.py $1 320

