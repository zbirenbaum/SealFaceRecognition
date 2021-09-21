#generate splits files
python train.py -d data/processed -c config.py -n 3 -g True
#load splits files
python train.py -d data/processed -c config.py -n 3 -s splitsave
