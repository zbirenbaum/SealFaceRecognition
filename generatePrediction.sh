#!/bin/sh

python format_data.py GALLERY ./data/processed/Final_Training_Data
python format_data.py PROBE ./data/probe
python seenbefore.py