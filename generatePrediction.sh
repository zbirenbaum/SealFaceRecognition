#!/bin/sh

PROBE=$1
echo $PROBE
python format_data.py GALLERY ./data/processed/Final_Training_Dataset
python format_data.py PROBE ./data/probe/$PROBE
python seenbefore.py
