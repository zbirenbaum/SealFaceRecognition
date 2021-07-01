"""Data Splitting."""
from __future__ import print_function
from __future__ import division
import os
from pathlib import Path
import random
import math
import pandas as pd
import numpy as np
import json
#import itertools

class DataSplitter(object):
    def __init__(self, kfold, photodir=None, openset=None, closedset=None):
        self.datalabels=[]
        self.kfold=kfold
        if photodir is None:
            photodir="photos"
        if openset:
            self.set_type = "openset"
        elif closedset:
            self.set_type = "closedset"
 
        self.set_params(photodir)

    def set_params(self, photodir):
        self.datalabelsdict = get_individuals(photodir)
        datalabels = list(self.datalabelsdict.keys())
        #datalabels = list(self.datalabelsdict['10'])
        self.datalabels = sorted(datalabels, key=int)
        self.numlabels = len(self.datalabels)
        self.testnum = int(math.ceil(self.numlabels/self.kfold))  # array of splits
        self.trainnum = self.numlabels-math.floor(self.numlabels/self.kfold)  # array of splits
        self.testidxarr=[]
        self.trainidxarr=[]
        return
        
    def print_param(self):
        print("datalabels: " + str(self.datalabelsdict['0']) + "\nnumlabels: " + str(self.numlabels) + "\nkfold: " + str(self.kfold) + "\ntestnum: " + str(self.testnum) + "\ntrainnum: " + str(self.trainnum) + "\n")
        return
    
    def setsplit(self):
        kfold = self.kfold
        numlabels = self.numlabels
        if self.set_type == "openset":
            self.trainidxarr, self.testidxarr = calcindices([], [], 0, numlabels, kfold)  # array of arrays, each holds classes to train on for fold[idx+1]
#            print("index list for training (arr[n-1] = indexes of train labels for nth fold): " + str(self.trainidxarr))
#            print("index list for testing (arr[n-1] = indexes of testing labels for nth fold): " + str(self.testidxarr))
        return


    def printbyfold(self):
        counter = 1
        for trainidxlist, testidxlist in zip(self.trainidxarr, self.testidxarr):
            print("FOLD:" + str(counter))
            print("train indices:\n" + str(trainidxlist))
            print("test indices:\n" + str(testidxlist) + "\n")
            counter = counter+1




"""  
    def read_labels(self):
        prefix = str(Path(self.dir).resolve())
        frame = pd.DataFrame(columns=['label','dirpath','photos','photopath'])
        extensions = ('png', 'jpg', 'jpeg')
#        byindex = []
        assert(os.path.exists(str(prefix)))
        lobjarr = []
        photos = []
        frame = pd.DataFrame()
        frames = []
        photopaths = []
        labels = []
        paths = []
        for item in os.listdir(str(prefix)):
            path = os.path.join(prefix, item)
            if not os.path.isdir(path):
                continue
            file_path=""
            for file_nameindex in os.listdir(path):
                if file_nameindex.lower().endswith(extensions):
                    file_path = os.path.join(path, file_nameindex)
            photopaths.append(str(file_path))
            paths.append(path)
            labels.append(item)
    #print(os.listdir(path))
            data = {"label": labels,
                    "paths": paths, "Photo Paths": photopaths}
            #print(item)
                    #ldata = LabelData(labels, paths, photos, photopaths)
                    #frame = ldata.frame
            frames.append(pd.DataFrame(data))
        frame = pd.concat(frames, axis=0, ignore_index=True, keys=['label','paths', 'Photo Paths'])
        print(frame)
                    #lobjarr.append(ldata)
                    #frame = frame.append([item, path, photos, photopaths])
        #return frame

class LabelData(object):
    def __init__(self, label, labeldirpath, photos, photopaths):
        self.photopaths = photopaths
        print(photopaths)
        print(label)
        print(labeldirpath)
        print(photos)
        self.photos = photos
        self.labeldirpath = labeldirpath
        self.label = label
        data = [label, labeldirpath, photos, photopaths]
        self.frame = pd.DataFrame(data, columns=['label','dirpath','photos','photopath'])

def get_individuals(directory):
    prefix = str(Path(directory).resolve())
    extensions = ('png', 'jpg', 'jpeg')
    individuals = {}
    assert(os.path.exists(str(prefix)))

    for item in os.listdir(str(prefix)):
        path = os.path.join(prefix, item)
        if not os.path.isdir(path):
            continue
        nameindex = str(int(item)-1)
        individuals[nameindex] = []
        for file_nameindex in os.listdir(path):
            if file_nameindex.lower().endswith(extensions):
                file_path = os.path.join(path, file_nameindex)
                individuals[nameindex].append(str(file_path))
    
    return individuals

def calcindices(trainarr, testarr, counter, numlabels, kfold, maxnumlabels=None):
    if maxnumlabels is None:
        maxnumlabels=numlabels  # only happens on first call
    if counter < kfold:
        testidx_min=numlabels-int(math.ceil(numlabels/(kfold-counter)))
        testidx_max=numlabels
        range_1 = list(range(0,testidx_min))
        range_2 = list(range(testidx_max, maxnumlabels))
        if testidx_min < 0:
            testidx_min=0
        test_append = list(range(testidx_min, testidx_max))
        testarr.append(test_append)
        numlabels=numlabels-len(test_append)
        range_1.extend(range_2)
        train_append = range_1
        trainarr.append(train_append)
        trainarr, testarr = calcindices(trainarr, testarr, counter+1, numlabels, kfold, maxnumlabels)
    return trainarr, testarr


""" 
#dsplit=DataSplitter(5, "photos", openset=True)
#dsplit.print_param()
#dsplit.setsplit()
#dsplit.printbyfold()

def create_splits(directory, num_splits, num_label_testing, num_label_training):

    """Create training and testing split according to num_splits

    Args:
        directory (string): the path to the photo directory
        num_splits (int): number of splits or cross-fold validation
        
    Returns:
        list[list]: list[i] is another list for each {i+1}_th split. 
                    list[i] = [num of training photos, number of unique seals for training, number of probe photos, number of gallery photos, number of unique seals for testing]
    """
    splits_dir = os.path.join(os.path.expanduser('./splits'))

    if not os.path.isdir(splits_dir):  
        os.makedirs(splits_dir)
    individuals = get_individuals(directory)
    labels = list(individuals.keys())
    
    splitData = []
    for i in range(num_label_testing):
        random.shuffle(labels)
        probeCount, galleryCount = create_testing_set(individuals, labels[:num_label_testing], i+1)
        trainingCount = create_training_set(individuals, labels[num_label_testing:], i+1)
        splitData.append([trainingCount, num_label_training, probeCount, galleryCount, num_label_testing])
        
    return splitData

def create_testing_set(individuals, labels, counter):
    """Create probe and gallery for testing, probe has one photo for each individual and gallery has the remaining photos

    Args:
        individuals (dictionary): map seal class to lists of file path to each of that seal's photo
        labels (list): list of the corresponding labels
        counter (int): current number of training - 1

    Returns:
        (int, int): number of probe and gallery images
    """
    splits_dir = os.path.join(os.path.expanduser('./splits/split{}/fold_1/'.format(counter)))
    if not os.path.isdir(splits_dir):
        os.makedirs(splits_dir)

    gallery = open('./splits/split{}/gal.txt'.format(counter),'w')
    probe = open('./splits/split{}/probe.txt'.format(counter),'w')
    
    probeCount, galleryCount = 0, 0
    
    for key in labels:
        value = individuals[key]
        temp = value[::]
        random.shuffle(temp)
        probe.write(temp[0]+ ' ' + key + '\n')
        probeCount += 1
        for j in range(1, len(value)):
            gallery.write(temp[j] + ' ' + key + '\n')
            galleryCount += 1
        
    gallery.close()
    probe.close()
    
    return probeCount, galleryCount

def create_training_set(individuals, labels, counter):
    """Create a training set (train.txt file) in the splits folder. 
       The training file will be in the form:
       Total_Number_Of_Labels X
       PATH_TO_PHOTO1 LABEL
       PATH_TO_PHOTO2 LABEL
       ...

    Args:
        individuals (dictionary): map seal class to lists of file path to each of that seal's photo
        labels (list): list of the corresponding labels
        counter (int): current number of training - 1
        
    Returns:
        int: number of training images
    """
    fname = './splits/split{}/train.txt'.format(counter)
    
    trainingCount = 0
    with open(fname, 'w') as f:
        f.write('Total_Number_Of_Labels ' + str(len(individuals)) + '\n')
        for key in labels:
            for v in individuals[key]:
                f.write(v + ' ' + key + '\n')
                trainingCount += 1
                
    return trainingCount
                
 




