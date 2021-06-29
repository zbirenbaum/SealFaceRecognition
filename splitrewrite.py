"""Data Splitting."""
from __future__ import print_function
from __future__ import division
#import os
#from pathlib import Path
#import random
import math
#import itertools

class DataSplitter():
    def __init__(self, kfold, datalabels, openset=None, closedset=None):
        self.datalabels=datalabels
        self.numlabels = len(datalabels)
        self.kfold = kfold
        self.testnum = int(math.ceil(self.numlabels/kfold))  # array of splits
        self.trainnum = self.numlabels-math.floor(self.numlabels/kfold)  # array of splits
        self.training_data = []
        self.testing_data = []
        self.testidxarr=[]
        self.trainidxarr=[]
        if openset:
            self.set_type = "openset"
        elif closedset:
            self.set_type = "closedset"
   
    def print_param(self):
        print("datalabels: " + str(self.datalabels) + "\nnumlabels: " + str(self.numlabels) + "\nkfold: " + str(self.kfold) + "\ntestnum: " + str(self.testnum) + "\n")
    
    def opensetsplit(self):
        trainarr = []
        self.trainidxarr = self.calcindices(trainarr, 0)  # array of arrays, each holds classes to train on for fold[idx+1]
        print("index list for training (arr[n-1] = indexes of train labels for nth fold): " + str(self.trainidxarr))
        print("index list for testing (arr[n-1] = indexes of testing labels for nth fold): " + str(self.testidxarr))

    def closedsetsplit(self):  # same logic as open but need to create path to photos 1->n
        print("placeholder")

    def calcindices(self, trainarr, counter):
        if counter < self.kfold:
            testidx_min=self.numlabels-(self.testnum*(counter+1))
            testidx_max=testidx_min+(self.testnum)
            range_1 = list(range(0,testidx_min))
            range_2 = list(range(testidx_max,self.numlabels))
            if testidx_min < 0:
                testidx_min=0
            self.testidxarr.append(list(range(testidx_min, testidx_max)))
            range_1.extend(range_2)
            totalrange=range_1
            toappend = totalrange
            trainarr.append(toappend)
            trainarr = self.calcindices(trainarr, counter+1)
        return trainarr




#            self.numlabels-diff
            #trainarr.append(list(range(0,(self.numlabels-diff)).append(range(
 #       return self.trainindices(kfolds-1)
  #      return list(range(0,self.trainnum))
dsplit=DataSplitter(3, list(range(1,10)), openset=True)
dsplit.print_param()
dsplit.opensetsplit()
