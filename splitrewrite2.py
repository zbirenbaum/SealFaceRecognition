from __future__ import print_function
from __future__ import division
import math
import databuilder as db

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
        self.dbobj = db.DataBuilder(photodir)
        self.full_dataset = self.dbobj.get_photos()
        self.datalabels = sorted(self.full_dataset.get_labels(), key=int)
        self.numlabels = len(self.datalabels)
        self.testnum = int(math.ceil(self.numlabels/self.kfold))  # array of splits
        self.trainnum = self.numlabels-math.floor(self.numlabels/self.kfold)  # array of splits
        self.testidxarr=[]
        self.trainidxarr=[]
        self.setsplit()
        return

    def print_param(self):
        print("datalabels: " + str(self.datalabels) + "\nnumlabels: " + str(self.numlabels) + "\nkfold: " + str(self.kfold) + "\ntestnum: " + str(self.testnum) + "\ntrainnum: " + str(self.trainnum) + "\n")
        return

    def setsplit(self):
        kfold = self.kfold
        numlabels = self.numlabels
        if self.set_type == "openset":
            self.trainidxarr, self.testidxarr = calcindices([], [], 0, numlabels, kfold)  # array of arrays, each holds classes to train on for fold[idx+1]
            self.trainphotos, self.trainpaths, self.testphotos, self.testpaths = split_bylabel(
                    self.trainidxarr,
                    self.testidxarr,
                    self.full_dataset
                    )
        return

    def printindexbyfold(self):
        counter = 1
        for trainidxlist, testidxlist in zip(self.trainidxarr, self.testidxarr):
            print("FOLD:" + str(counter))
            print("train indices:\n" + str(trainidxlist))
            print("test indices:\n" + str(testidxlist) + "\n")
            counter = counter+1
        return
    def printtrainsetbyfold(self):
        counter = 1
        for trainidxlist, testidxlist in zip(self.trainidxarr, self.testidxarr):
            print("FOLD:" + str(counter))
            print("trainidxlist:\n" + str(trainidxlist))
            print("train photos:\n" + str(self.trainphotos[counter-1]))
            print("trainpaths:\n" + str(self.trainpaths[counter-1]))
            print("test indices:\n" + str(testidxlist) + "\n")
            counter = counter+1
        return

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

def split_bylabel(trainidxarr, testidxarr, full_dataset):
    fullset = full_dataset
    trainphotos = []
    trainpaths = []
    training = [trainphotos, trainpaths]
    testphotos = []
    testpaths = []
    testing = [testphotos, testpaths]
    counter = 0
    for trainidxlist, testidxlist in zip(trainidxarr, testidxarr):
        trainphotos.append([])
        trainpaths.append([])
        testphotos.append([])
        testpaths.append([])
        for index in trainidxlist:
            trainphotos[counter].extend(fullset.get_photos_by_index(index))
            trainpaths[counter].extend(fullset.get_paths_by_index(index))
        for index in testidxlist:
            testphotos[counter].extend(fullset.get_photos_by_index(index))
            testpaths[counter].extend(fullset.get_paths_by_index(index))
        counter = counter+1
    return trainphotos, trainpaths, testphotos, testpaths


