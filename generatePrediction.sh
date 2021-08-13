#!/bin/sh

# preprocess
python zprocess.py

PROBE=$1
python format_data.py GALLERY ./data/processed/train/Final_Training_Dataset
python format_data.py PROBE ./data/processed/probe/$PROBE
python seenbefore.py
