#!/bin/sh

# preprocess
python zprocess.py

# training
NUM_FOLD=$1
if [[ $NUM_FOLD -gt 0 ]]
then
    python train.py -c config.py -d ./data/processed/train/Final_Training_Dataset -n $NUM_FOLD -g True
else
    python train.py -c config.py -d ./data/processed/train/Final_Training_Dataset
    # move the trained model to ./trainedModel
    MODEL=$(ls -td -- ./log/SealNet_Full_Training/* | head -n 1) #get the newest model
    rm -rf trainedModel
    mkdir trainedModel
    mv $MODEL ./trainedModel
fi
