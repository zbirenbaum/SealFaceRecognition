from __future__ import division
import math

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

def split_testset(settype, testingdict):
    if settype == 'closed':
        for label in testingdict.keys():
            ppaths = testingdict[label]
            num_photos = len(ppaths)
            if num_photos < 2:
                print("ERROR NOT ENOUGH PHOTOS")
                exit(1)
            testingdict['probes'] = []
            testingdict['gallery'] = [] 
            probepath = ppaths[0]
            testingdict['probes'].append(str(ppaths[0]) + str(label))
            ppaths = ppaths.remove(probepath)
            testingdict['gallery'].append(str(ppaths[0]) + str(label))
