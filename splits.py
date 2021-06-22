#! /usr/local/bin/python3

'''
 Gets a directory and outputs file names and individual names for use in splits
 Assumes each subdir contains only one individual, and the name of the subdir is the name of the individual
 Image extensions are expected, append to the tuple below to extend
'''

import os 
from pathlib import Path
import random

def create_splits(directory, num_splits):
    prefix = Path(directory).resolve()
    splits_dir = os.path.join(os.path.expanduser('./splits'))

    if not os.path.isdir(splits_dir):  
        os.makedirs(splits_dir)
    individuals = get_individuals(directory)
    labels = list(individuals.keys())
    num_testing = len(labels)//4
    for i in range(num_splits):
        random.shuffle(labels)
        create_testing_set(individuals, labels[:num_testing], i+1)
        create_training_set(individuals, labels[num_testing:], i+1)

def create_training_set(individuals, labels, counter):
    fname = './splits/split{}/train_1.txt'.format(counter)
    with open(fname, 'w') as f:
        for key in labels:
            for v in individuals[key]:
                f.write(v + ' ' + key + '\n')
    
def create_testing_set(individuals, labels, counter):
    splits_dir = os.path.join(os.path.expanduser('./splits/split{}/fold_1/'.format(counter)))
    if not os.path.isdir(splits_dir):
        os.makedirs(splits_dir)
    splits = min([len(value) for key, value in individuals.items()])

    for i in range(splits):
        gallery = open('./splits/split{}/fold_1/gal_{}.txt'.format(counter, i+1),'w')
        probe = open('./splits/split{}/fold_1/probe_{}.txt'.format(counter, i+1),'w')
        # verification = open('./splits{}/fold_1/verification.txt'.format(counter,i+1),'w')
        for key in labels:
            value = individuals[key]
            if i >= len(value):
                continue
            probe.write(value[i]+ ' ' + key + '\n')
            for j in range(len(value)):
                # verification.write(value[j] + ' ' + key + '\n')
                if j != i:
                    gallery.write(value[j] + ' ' + key + '\n')
            
        gallery.close()
        probe.close()
        # verification.close()


def get_individuals(directory):
    prefix = str(Path(directory).resolve())
    extensions = ('png', 'jpg', 'jpeg')
    individuals = {}
    assert(os.path.exists(str(prefix)))

    for item in os.listdir(str(prefix)):
        path = os.path.join(prefix, item)
        if not os.path.isdir(path):
            continue
        name = str(int(item))
        individuals[name] = []
        for file_name in os.listdir(path):
            if file_name.lower().endswith(extensions):
                file_path = os.path.join(path, file_name)
                individuals[name].append(str(file_path))
    
    return individuals
