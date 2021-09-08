#!/bin/sh

# preprocess
python zprocess.py

python format_data.py GALLERY ./data/processed/train/Final_Training_Dataset
python format_data.py PROBE ./data/processed/probe/probe_folder_test
python seenbefore.py
