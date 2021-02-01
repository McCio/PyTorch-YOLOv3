import glob
import os
import numpy as np
import sys
from utils.parse_config import *
from utils.utils import load_classes
from utils.convert_labels import convert


def create_lists(artifacts, file_train, file_val):
    convert(artifacts)
    file_train = open(file_train, "w")
    file_val = open(file_val, "w")
    counter = 1
    split_pct = 10
    index_test = round(100 / split_pct)
    val_dir_exists = False
    val_dir = os.path.join(artifacts, "val")
    if os.path.exists(val_dir) and os.path.isdir(val_dir):
        convert(val_dir)
        # we have already-splitted train/val
        val_dir_exists = True
    if val_dir_exists:
        any_file_found = False
        for pathAndFilename in glob.iglob(os.path.join(val_dir, "images", "*.png")):
            any_file_found = True
            title, ext = os.path.splitext(os.path.basename(pathAndFilename))
            rel_path = str(os.path.join(val_dir, "images", f"{title}{ext}"))
            file_val.write(f"{rel_path}\n")
        val_dir_exists = any_file_found
        val_dir_exists = True  # this forces empty val list
    for pathAndFilename in glob.iglob(os.path.join(artifacts, "images", "*.png")):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        rel_path = str(os.path.join(artifacts, "images", f"{title}{ext}"))
        if counter == index_test and not val_dir_exists:
            counter = 1
            file_val.write(f"{rel_path}\n")
        else:
            file_train.write(f"{rel_path}\n")
            counter = counter + 1
    file_train.close()
    file_val.close()


if __name__ == "__main__":
    data_config = parse_data_config("config/dota.data")
    train_path = data_config["train"]
    valid_path = data_config["valid"]
    class_names = load_classes(data_config["names"])
    create_lists(artifacts="data/dota", file_train=train_path, file_val=valid_path)
