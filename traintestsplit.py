import dirhandler as dh
import math

class Dataset(object):
    """
    set_byfold[fold] = list(labeldicts)
    labeldict dict_keys(['photos', 'label', 'originalindex'])
    labeldict['photos'] = list of dictionaries with photoinfo
    """
    def __init__(self, dir, kfold):
        self.dir = dir
        self.kfold = kfold
        self.fulldata = get_fulldata(self.dir)
        self.numlabels = len(self.fulldata)
        self.trainidxarr, self.testidxarr = calcindices([], [], 0, self.numlabels, self.kfold)  # array of arrays, each holds classes to train on for fold[idx+1]
        self.training_by_fold, self.testing_by_fold = get_k_splits(
                self.kfold, 
                self.fulldata, 
                self.trainidxarr, 
                self.testidxarr
                )

def get_fulldata(dir):
    fulldata = dh.generate_dataset(dir)
    return fulldata

def get_k_splits(kfold, fulldata, trainidxarr, testidxarr):
    training_by_fold = []
    testing_by_fold = []
    for k in range(0,kfold):
        training_by_fold.append(gen_fold_split(trainidxarr[k], fulldata))
        testing_by_fold.append(gen_fold_split(testidxarr[k], fulldata))
    return training_by_fold, testing_by_fold

def gen_fold_split(indices, fulldata):
    fold_photos = []
    for index in indices:
        fold_photos.append(fulldata[index])
    return fold_photos


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


def pretty(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))

def originalindex(setbyfold, kfold):
    originallistbyfold=[]
    for i in range (0, kfold):
        print("FOLD: " + str(i))
        originallist = []
        for labeldict in setbyfold[i]:
            originallist.append(labeldict['originalindex'])
        originallistbyfold.append(originallist)

    return originallistbyfold

def label_photos(setbyfold, kfold):
    photoslistbyfold=[]
    for i in range (0, kfold):
        print("FOLD: " + str(i))
        photoslist = []
        for labeldict in setbyfold[i]:
            photoslist.append(labeldict['photos'])
            for something in labeldict['photos']:
                print(something)
        photoslistbyfold.append(photoslist)
    return photoslistbyfold





dset = Dataset("photos", 5)
originaltrain = label_photos(dset.training_by_fold, 5)
originaltest = label_photos(dset.testing_by_fold, 5)
counter = 0
photos = label_photos(dset.training_by_fold, 5)


def print_train_test_ogindex(originaltrain, originaltest):
    counter = 0
    for ogtrain, ogtest in zip(originaltrain, originaltest):
        print("FOLD: " + str(counter))
        print(str(ogtrain) + "\n" + str(ogtest))
        counter = counter+1

