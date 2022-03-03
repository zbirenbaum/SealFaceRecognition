#!/bin/sh

# preprocess
python train.py -o True -n 5 -c config.py -d ./data/processed/Final_Training_Dataset
#python train.py -o True -n 5 -c config_primnet.py -d ./data/processed/Final_Training_Dataset
