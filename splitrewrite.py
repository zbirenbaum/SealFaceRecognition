from __future__ import print_function
from __future__ import division
import math

from matplotlib import test
import databuilder as db

class DataSplitter(object):
    """
    Class for calling data initialization and generating splits for cross validation:
        takes arguments: kfold (number of folds for cross validation), set_type ('open' or 'closed'), photo directory (default: photos)
    """
    def __init__(self, kfold, set_type, photodir=None):
        self.datalabels=[]
        self.kfold=kfold
        if photodir is None:
            photodir="photos"
        if set_type == 'open':
            self.set_type = "openset"
        elif set_type == 'closed':
            self.set_type = "closedset"
        else:
            print("set set_type parameter to either \'open\' or \'closed\'")
            return
        self.set_params(photodir)

    def set_params(self, photodir):
        """
        initializes the attributes to be used by the class, called automatically from init, do not call manually
        """
        self.dbobj = db.DataBuilder(photodir)
        self.full_dataset = self.dbobj.get_photoarray()
        self.datalabels = set(self.full_dataset.get_photo_labels())
        self.numlabels = len(self.datalabels)
        self.testnum = int(math.ceil(self.numlabels/self.kfold))  # array of splits
        self.trainnum = self.numlabels-math.floor(self.numlabels/self.kfold)  # array of splits
        self.testidxarr=[]
        self.trainidxarr=[]
        self.traindata, self.testdata = self.setsplit()
        return

    def print_param(self):
        print("datalabels: " + str(self.datalabels) + "\nnumlabels: " + str(self.numlabels) + "\nkfold: " + str(self.kfold) + "\ntestnum: " + str(self.testnum) + "\ntrainnum: " + str(self.trainnum) + "\n")
        return

    def setsplit(self):
        """
        gets the dataset information from the databuilder object and splits the sets according to indexing from calcindices
        """
        kfold = self.kfold
        numlabels = self.numlabels
        testphotos = []
        trainphotos = []
        if self.set_type == "openset":
            self.trainidxarr, self.testidxarr = calcindices([], [], 0, numlabels, kfold)  # array of arrays, each holds classes to train on for fold[idx+1]
            counter =0
            for trainingidx in self.trainidxarr:
                trainphotos.append([])
                for idx in trainingidx:
                    trainphotos[counter].extend(self.dbobj.get_photoarray().get_photoobj_bylabel(self.dbobj.labels[idx]))
                counter = counter +1
            counter =0
            for testingidx in self.testidxarr:
                testphotos.append([])
                for idx in testingidx:
                    testphotos[counter].extend(self.dbobj.get_photoarray().get_photoobj_bylabel(self.dbobj.labels[idx]))
                counter = counter +1


#testphotoarr = self.dbobj.gen_testing(self.trainidxarr)
               # print(self.dbobj.gen_from_index(idxarr).get_photo_names())
            #self.trainphotos, self.trainpaths, self.testphotos, self.testpaths = split_bylabel(
            #        self.trainidxarr,
            #        self.testidxarr,
            #        self.full_dataset
            #        )
        return trainphotos, testphotos

    """the following two methods are useless and only called by test scripts to verify proper functionality"""
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
#            print("train photos:\n" + str(self.trainphotos[counter-1]))
#            print("trainpaths:\n" + str(self.trainpaths[counter-1]))
            print("test indices:\n" + str(testidxlist) + "\n")
            counter = counter+1
        return

def calcindices(trainarr, testarr, counter, numlabels, kfold, maxnumlabels=None):
    """
    calculates the index of labels to be used for training and testing in each fold
    """
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
    """generates list indexed by fold of PhotoArrays to provide the paths and filenames of the relevant photos for training and testing"""
    fullset = full_dataset
    trainphotos = []
    trainpaths = []
    testphotos = []
    testpaths = []
    counter = 0
    for trainidxlist, testidxlist in zip(trainidxarr, testidxarr):
        trainphotos.append(db.PhotoArray())
        trainpaths.append(db.PhotoArray())
        testphotos.append(db.PhotoArray())
        testpaths.append(db.PhotoArray())
        for index in trainidxlist:
            trainphotos[counter].extend(fullset.get_photos_by_index(index))
            trainpaths[counter].extend(fullset.get_paths_by_index(index))
        for index in testidxlist:
            testphotos[counter].extend(fullset.get_photos_by_index(index))
            testpaths[counter].extend(fullset.get_paths_by_index(index))
        counter = counter+1
    return trainphotos, trainpaths, testphotos, testpaths
