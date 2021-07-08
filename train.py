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

import os
import sys
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

def train(config_file, counter):
    # I/O for config
    config = utils.import_file(config_file, 'config')
    splits_path = config.splits_path + '/' + config.testing_type + '/fold{}'.format(counter)
    print(splits_path)
    # Get training set
    trainset = utils.Dataset(splits_path + '/train.txt')
    trainset.images = utils.preprocess(trainset.images, config, True)

    # Creating the network (check network.py)
    network = Network()
    network.initialize(config, trainset.total_num_classes)

    # Initalization log and summary for running
    log_dir = utils.create_log_dir(config, config_file, 'SealNet_Fold{}'.format(counter))
    summary_writer = tf.summary.FileWriter(log_dir, network.graph)
    if config.restore_model:
        network.restore_model(config.restore_model, config.restore_scopes)

    # Load gallery and probe file_list
    print('Loading probe and gallery images...')
    probes = []
    gal = []
    with open(splits_path + '/probe.txt' ,'r') as f:
        counter = 0
        for line in f:
            if counter == 0:
                counter = counter + 1
                continue
            probes.append(line.strip())
    probe_set = evaluate.ImageSet(probes, config)

    with open(splits_path  + '/train.txt', 'r') as f:
        counter = 0
        for line in f:
            if counter == 0:
                counter = counter + 1
                continue
            gal.append(line.strip())
    gal_set = evaluate.ImageSet(gal, config)

    trainset.start_batch_queue(config, True)

    #
    # Main Loop
    #
    print('\nStart Training\n# epochs: {}\nepoch_size: {}\nbatch_size: {}\n'.\
        format(config.num_epochs, config.epoch_size, config.batch_size))

    global_step = 0
    start_time = time.time()
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

        # Testing
        print('Testing...')
        probe_set.extract_features(network, len(probes))
        gal_set.extract_features(network, len(gal))

        rank1, rank5 = evaluate.identify(log_dir, probe_set, gal_set)
        print('rank-1: {:.3f}, rank-5: {:.3f}'.format(rank1[0], rank5[0]))
        
        # Output test result
        summary = tf.Summary()
        summary.value.add(tag='identification/rank1', simple_value=rank1[0])
        summary.value.add(tag='identification/rank5', simple_value=rank5[0])
        summary_writer.add_summary(summary, global_step)

        # Save the model
        network.save_model(log_dir, global_step)
    results_copy = os.path.join('log/result_{}_{}.txt'.format(config.model_version, counter))
    shutil.copyfile(os.path.join(log_dir,'result.txt'), results_copy)

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
    num_trainings = 3 if not settings.number else settings.number
    print('Running training {} times'.format(num_trainings))
    splitData = []

    ttsplit.Dataset(settings.directory, int(num_trainings))
    if not settings.splits:
        if os.path.exists(os.path.expanduser('./splits')):
            shutil.rmtree(os.path.expanduser('./splits')) 
        #splitData = splits.create_splits(settings.directory, num_trainings)
        #splitData = splitrewrite.DataSplitter(settings.directory, num_trainings)
    else:
        print('Using existing splits in the splits folder. Haven\'t implemented this yet so don\'t use it.')

    ttsplit.Dataset(settings.directory, kfold=int(num_trainings))
    for i in range(num_trainings):
        print('Starting training #{}\n'.format(i+1))
#        print('There are {} seal photos, {} unique seals in training, {} probe photos, {} gallery photos, {} unique seals for testing\n'.format(splitData[i][0], splitData[i][1], splitData[i][2], splitData[i][3], splitData[i][4]))
        train(settings.config_file, i+1)

if __name__ == '__main__':
    main()
