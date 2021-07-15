
import sys
import os
import warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # or any {'0', '1', '2'}
#sys.stderr = open(os.devnull, "w")  # silence stderr
warnings.filterwarnings('ignore')

import pandas as pd
import time
import tensorflow as tf
import tensorflow.contrib.slim as slim
import numpy as np
from argparse import ArgumentParser
import utils
import tflib
from network import Network
# from tensorflow.contrib.tensorboard.plugins import projector
import evaluate
import shutil
import traintestsplit as ttsplit
from preprocess import preprocess
import math





def test_model(config, config_file, counter, trainset, model, probeset, testset=None):

    gal = trainset.set_list# delete later, gallary set equal to training prior to preprocess
    network = Network()
    network.initialize(config, trainset.total_num_classes)

    if config.restore_model:
        network.restore_model(model, config.restore_scopes)
    
    #print(len(probeset.keys()))
    probes = utils.init_from_dict(probeset)[3]
    #print(len(probes))
    probe_set = evaluate.ImageSet(probes, config)


    gal_set = evaluate.ImageSet(gal, config)

    config.batch_size = math.ceil(len(gal)/3)
    config.epoch_size = 3
    config.num_epochs = 40
    
    # Initalization log and summary for running
    log_dir = utils.create_log_dir(config, config_file, 'SealNet_Fold{}'.format(counter))
    
    print('Testing...')
    probe_set.extract_features(network, len(probes))
    gal_set.extract_features(network, len(gal))

    rank1, rank5, df = evaluate.identify(log_dir, probe_set, gal_set)
    print(df)
    print('rank-1: {:.3f}, rank-5: {:.3f}'.format(rank1[0], rank5[0]))
    
    # Output test result
    return








def main():
    parser = ArgumentParser(description='Train SealNet', add_help=False)
    parser.add_argument('-c','--config_file', dest='config_file', action='store', 
        type=str, required=True, help='Path to training configuration file', )
    parser.add_argument('-d', '--directory', dest='directory', action='store',
        type=str, required=True, help='Directory containing subdirectories that contain photos')
    parser.add_argument('-s', '--splits', dest='splits', action='store', type=bool,
        required=False, help='Flag to use existing splits for training and testing data')
    parser.add_argument('-n', '--number', dest='number', action='store', type=int,
        required=False, help='Number of times to run the training(default is 3)')
    

    settings = parser.parse_args()
    config_file = 'config.py' if not settings.config_file else settings.config_file
    config = utils.import_file(config_file, 'config')
    num_trainings = 5 if not settings.number else settings.number
    print('Running testing {} times'.format(num_trainings))
    modelslist = []
    for model in os.listdir(config.restore_model):
        modelslist.append(os.path.join(config.restore_model, model))

    builder = ttsplit.DatasetBuilder(settings.directory, usedict=1, settype=config.testing_type, kfold=int(num_trainings))
    for i in range(num_trainings):
        print('Starting training #{}\n'.format(i+1))
        trainset = builder.dsetbyfold[i]
        testset = builder.testsetbyfold[i]
        probeset = builder.probesetbyfold[i]
        #print(len(probeset.keys()))
#        print('There are {} seal photos, {} unique seals in training, {} probe photos, {} gallery photos, {} unique seals for testing\n'.format(splitData[i][0], splitData[i][1], splitData[i][2], splitData[i][3], splitData[i][4]))
        test_model(config, settings.config_file, i+1, trainset, modelslist[i], probeset)

if __name__ == '__main__':
    main()
