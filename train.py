#! /usr/local/bin/python3
"""Main training file for face recognition
"""
# MIT License
# 
# Copyright (c) 2018 Debayan Deb
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import pandas as pd
import os
import time
import tensorflow as tf
import numpy as np
from argparse import ArgumentParser
import utils
from network import Network
import evaluate
import shutil
import traintestsplit as ttsplit
import math
from preprocess import preprocess


def trainKFold(config, config_file, counter, trainset, testset=None):
    # In training, we consider training set to be gallery and testing set to be probes (Closed Set Identification)
    trainset = utils.Dataset(ddict=trainset)
    trainset.images = preprocess(trainset.images, config, True)
    gal = trainset.set_list
    gal_set = evaluate.ImageSet(gal, config)   
    
    probeset = utils.Dataset(ddict=testset)
    probeset.images = preprocess(probeset.images, config)
    probes = probeset.set_list
    probe_set = evaluate.ImageSet(probes, config)

    # Initialize the network
    network = Network()
    network.initialize(config, trainset.total_num_classes)

    # Initalization log and summary for running
    log_dir = utils.create_log_dir(config, config_file, 'SealNet_Fold{}'.format(counter))
    summary_writer = tf.summary.FileWriter(log_dir, network.graph)
    if config.restore_model:
        network.restore_model(config.restore_model, config.restore_scopes)

    config.epoch_size = int(math.ceil(len(gal)/config.batch_size))
    trainset.start_batch_queue(config, True) 

    ##############################################################################################################
    ############################################## MAIN LOOP #####################################################
    ##############################################################################################################
    print('\nStart Training\n# epochs: {}\nepoch_size: {}\nbatch_size: {}\n'\
            .format(config.num_epochs, config.epoch_size, config.batch_size)) #config.epoch_size, config.batch_size))

    global_step = 0
    start_time = time.time()
    # Learning_rate=.001
    df = pd.DataFrame()
    for epoch in range(config.num_epochs):
        # Training
        for step in range(config.epoch_size):    #config.epoch_size):
            # Prepare input
            learning_rate = utils.get_updated_learning_rate(global_step, config)
            image_batch, label_batch = trainset.pop_batch_queue()

            wl, sm, global_step = network.train(image_batch, label_batch, learning_rate, config.keep_prob)

            # Display
            if step % config.summary_interval == 0:
                duration = time.time() - start_time
                start_time = time.time()
                utils.display_info(epoch, step, duration, wl)
                summary_writer.add_summary(sm, global_step=global_step)

        # Testing
        print('Testing...')
        probe_set.extract_features(network, len(probes))
        gal_set.extract_features(network, len(gal))

        rank1, rank5, df = evaluate.identify(log_dir, probe_set, gal_set)
        print('rank-1: {:.3f}, rank-5: {:.3f}'.format(rank1[0], rank5[0]))
        
        # Output test result
        summary = tf.Summary()
        summary.value.add(tag='identification/rank1', simple_value=rank1[0])
        summary.value.add(tag='identification/rank5', simple_value=rank5[0])
        summary_writer.add_summary(summary, global_step)

        # Save the model
        network.save_model(log_dir, global_step)

    resultsdf_file = 'log/result_fold_{}.csv'.format(counter)
    df.to_csv(resultsdf_file, index=False)
    
    results_copy = os.path.join('log/result_{}_{}.txt'.format(config.model_version, counter))
    shutil.copyfile(os.path.join(log_dir,'result.txt'), results_copy)

def trainAllData(trainingDir, config, config_file):
    trainset = utils.Dataset(path=trainingDir)
    
    # Initialize the network
    network = Network()
    network.initialize(config, trainset.total_num_classes)

    # Initalization log and summary for running
    log_dir = utils.create_log_dir(config, config_file, 'SealNet_Full_Training')
    summary_writer = tf.summary.FileWriter(log_dir, network.graph)
    if config.restore_model:
        network.restore_model(config.restore_model, config.restore_scopes)

    config.epoch_size = int(math.ceil(len(trainset.set_list)/config.batch_size))
    trainset.start_batch_queue(config, True) 
    
    ##############################################################################################################
    ############################################## MAIN LOOP #####################################################
    ##############################################################################################################
    print('\nStart Training\n# epochs: {}\nepoch_size: {}\nbatch_size: {}\n'\
            .format(config.num_epochs, config.epoch_size, config.batch_size)) #config.epoch_size, config.batch_size))

    global_step = 0
    start_time = time.time()
    df = pd.DataFrame()
    for epoch in range(config.num_epochs):
        # Training
        for step in range(config.epoch_size):   
            # Prepare input
            learning_rate = utils.get_updated_learning_rate(global_step, config)
            image_batch, label_batch = trainset.pop_batch_queue()

            wl, sm, global_step = network.train(image_batch, label_batch, learning_rate, config.keep_prob)

            # Display
            if step % config.summary_interval == 0:
                duration = time.time() - start_time
                start_time = time.time()
                utils.display_info(epoch, step, duration, wl)
                summary_writer.add_summary(sm, global_step=global_step)

        # Save the model
        network.save_model(log_dir, global_step)

    resultsdf_file = 'log/full_train.csv'
    df.to_csv(resultsdf_file, index=False)    

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
    dir = settings.directory
    config_file = settings.config_file
    config = utils.import_file(config_file, 'config')
    if (settings.number):
        num_trainings = settings.number
        print('Running training {} times'.format(num_trainings))

        if not settings.splits:
            if os.path.exists(os.path.expanduser('./splits')):
                shutil.rmtree(os.path.expanduser('./splits')) 
        else:
            print('Using existing splits in the splits folder. Haven\'t implemented this yet so don\'t use it.')

        builder = ttsplit.DatasetBuilder(dir, usedict=1, settype=config.testing_type, kfold=int(num_trainings))

        for i in range(num_trainings):
            print('Starting training #{}\n'.format(i+1))
            trainset = builder.dsetbyfold[i]
            testset = builder.testsetbyfold[i]
            trainKFold(config, config_file, i+1, trainset, testset)

    else:
        trainAllData(dir, config, config_file)

if __name__ == '__main__':
    main()
