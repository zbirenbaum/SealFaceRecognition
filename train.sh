#!/bin/sh

# preprocess
python zprocess.py

# training
NUM_FOLD=$1
if [[ $NUM_Fold -gt 0 ]]
then
    python train.py -c config.py -d ./data/processed/Final_Training_Dataset -n $NUM_FOLD
else
    python train.py -c config.py -d ./data/processed/Final_Training_Dataset
fi

# move the trained model to ./trainedModel
MODEL=$(ls -td -- ./log/SealNet_Full_Training/* | head -n 1) #get the newest model
rm -rf trainedModel
mkdir trainedModel
mv $MODEL ./trainedModel