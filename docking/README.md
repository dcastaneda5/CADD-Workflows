## Automated script for docking DUD-E compounds

Usage:

python run.py -w <DUDE_working_directory> -r <receptor_name> [options]

Options:
  --all       Runs all operations
  --split     Split mol2 ligands
  --convert   Convert mol2 ligands to pdbqt
  --dock      Dock compounds
  --rescore   Rescore with DLScore
