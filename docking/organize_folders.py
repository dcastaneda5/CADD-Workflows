import glob
import os
import shutil


def move_decoys_actives(folder):
    """Create subfolders for decoys and actives."""
    actives_dir = folder + "/actives"
    decoys_dir = folder + "/decoys"
    if not os.path.exists(actives_dir):
        os.makedirs(actives_dir)
    for file in glob.iglob(folder + "/actives*.mol2"):
        shutil.move(file, actives_dir)
    if not os.path.exists(decoys_dir):
        os.makedirs(decoys_dir)
    for file in glob.iglob(folder + "/decoys*.mol2"):
        shutil.move(file, decoys_dir)


if __name__ == "__main__":
    import sys
    move_decoys_actives(sys.argv[1])
