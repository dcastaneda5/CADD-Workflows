#!/bin/bash

if [ $# -eq 0 ]; then
    echo "USAGE: bash run <target_name>"
    exit 1
fi

TARGET=$1
LINK=http://dude.docking.org/targets/"$TARGET/$TARGET".tar.gz

# Download the file
echo "Downloading "$LINK""
wget $LINK

#Decompress
echo "Decompressing "$1""
tar -xvf "$TARGET".tar.gz
rm -f "$TARGET".tar.gz

cd $TARGET

#Decompress actives and decoys
gunzip actives_final.mol2.gz
gunzip decoys_final.mol2.gz

# Convert receptor to pdbqt

# Split actives and decoys
echo "Splitting actives"
python ../split_mol2.py actives_final.mol2
echo "Done"
echo "Splitting decoys"
python ../split_mol2.py decoys_final.mol2
echo "Done"

# Moving actives and decoys to folders
echo "Moving actives and decoys to folders"
mkdir actives
mv actives_final*.mol2 actives
mkdir decoys
mv decoys_final*.mol2 decoys

# Convert mol2 files to pdbqt files
echo "Converting mol2 files to pdbqt files"
echo "Submitting job"
sleep 2
sbatch --wait ../mol2pdbqt.slurm $TARGET
echo "Done"

# Move actives and decoys to folders
echo "Moving actives and decoys to folders" 
mv actives_final*.pdbqt actives
mv decoys_final*.pdbqt decoys

# Dock
echo "Sumbitting the job for docking"
sleep 2
sbatch ../dock.slurm $TARGET

# DLScore
#echo "Submitting the job for rescoring with dlscore"
#echo "This job will run after docking is finished."
#sbatch dlscore.slurm $TARGET

# Return to working directory
cd ..
