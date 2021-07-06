import dirhandler as dh
import math
import os
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

    def closedset(self):
        fullset = self.fulldata
        kfold = self.kfold
        for set in fullset:
            label = set['label']
            photos = set['label']['photos']
            num_photos = len(photos)
            calcindices([],[],0,num_photos,kfold)

            pass

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
                print(something['photopath'] + " " + something['photolabel'])
        photoslistbyfold.append(photoslist)
    return photoslistbyfold
def gen_set_photos_by_fold(setbyfold):
    photoslistbyfold=[]
    for fold in setbyfold:
        photoslist = []
        for labeldict in fold:
            for photo in labeldict['photos']:
                photoslist.append(photo['photopath'] + " " + photo['photolabel'])
        photoslistbyfold.append(photoslist)
    return photoslistbyfold


def create_set(listtowrite, type, k):
    splits_dir = os.path.join(os.path.expanduser('./splits/fold{}/'.format(k)))
    if not os.path.isdir(splits_dir):
        os.makedirs(splits_dir)


    fname = './splits/fold{}/{}.txt'.format(k,type)
    with open(fname, 'w') as f:
        for photo in listtowrite:
            f.write(photo + '\n')

kfold = 5
dset = Dataset("photos", kfold)
to_write_training=gen_set_photos_by_fold(dset.training_by_fold)
to_write_testing=gen_set_photos_by_fold(dset.testing_by_fold)

for k in range(1,kfold+1):
    create_set(to_write_training[k-1], "training", k)
    create_set(to_write_testing[k-1], "testing", k)






"""
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

"""

