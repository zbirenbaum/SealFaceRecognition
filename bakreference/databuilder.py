from __future__ import print_function
from __future__ import division
import os
import math
from pathlib import Path

class DataBuilder(object):
    def __init__(self, directory):
        self.dir = directory
        #self.lbdict = read_labels(directory)
        #self.frame = self.gen_frame()
        self.photoarray, self.labels = read_labels(directory)
        self.testphotoarrays = []
        self.trainphotoarrays = []

    def get_photoarray(self):
        return self.photoarray

    def get_testphotoarrays(self):
        return self.testphotoarrays

    def get_trainphotoarrays(self):
        return self.testphotoarrays

    def gen_test_from_index(self, idxlists):
        for idxlist in idxlists:
            labels= []
            for index in idxlist:
                labels.append(self.get_label_by_index(index))
            self.testphotoarrays.append(self.gen_from_labels(labels))
        return self.testphotoarrays

    def gen_train_from_index(self, idxlists):
        for idxlist in idxlists:
            labels= []
            for index in idxlist:
                labels.append(self.get_label_by_index(index))
            self.trainphotoarrays.append(self.gen_from_labels(labels))
        return self.trainphotoarrays


    def get_label_by_index(self, index):
        return self.labels[index]

    def gen_from_labels(self, labels):
        photoarr = []
        photos=[]
        for label in labels:
            paths = self.get_photoarray().get_paths_by_label(label)
            filenames = self.get_photoarray().get_photos_by_label(label)
            photos = [PhotoObj(path,filename, label) for path, filename in zip(paths, filenames)]
            photoarr.extend(photos)
        return PhotoArray(photoarr)

class PhotoArray(object):
    def __init__(self, photoarr=None):
        if photoarr is None:
            self.photoarr = []
        else:
            self.photoarr = photoarr
        return

    def __getitem__(self, index):
        return self.photoarr[index]

    def extend(self, toadd):
        self.photoarr.extend(toadd)
        return

    def get_tuples(self):
        return zip(self.get_photo_labels(), self.get_photo_paths())

    def get_arr(self):
        return list(self.photoarr)

    def get_photos(self):
        photolist = [photo for photo in self.photoarr]
        return photolist

    def get_photoobj_bylabel(self,label):
        return [photo for photo in self.photoarr if photo.getlabel() == label]
    

    def get_photo_names(self):
        return [photo.getfilename() for photo in self.photoarr]

    def get_photo_labels(self):
        return [photo.getlabel() for photo in self.photoarr]

    def get_photo_paths(self):
        return [photo.getpath() for photo in self.photoarr]

    def get_photos_by_label(self, label):
        return [photo.getfilename() for photo in self.photoarr if photo.getlabel() == label]

    def get_photos_by_index(self, index):
        return [photo.getfilename() for photo in self.photoarr if int(photo.getlabel()) == int(index+1)]

    def get_paths_by_label(self, label):
        return [photo.getpath() for photo in self.photoarr if photo.getlabel() == label]

    def get_paths_by_index(self, index):
        return [photo.getpath() for photo in self.photoarr if int(photo.getlabel()) == int(index+1)]
    

class PhotoObj(object):
    def __init__(self, path, filename, label):
        self.filename = filename
        self.path = os.path.join(path, filename)
        self.label = label
        return

    def getlabel(self):
        """Return the label of the photo obj"""
        return self.label
    def getpath(self):
        """Return the absolute path of the photo obj"""
        return self.path
    def getfilename(self):
        """Return the filename of the photo obj"""
        return self.filename



def read_labels(dir):
    extensions = ('png', 'jpg', 'jpeg')
    prefix = str(Path(dir).resolve())
    assert(os.path.exists(str(prefix)))
    labels = [i for i in os.listdir(str(prefix)) if not i.startswith(".")]
#    lbdict = {}
    photoarr = []
    for label in labels:
        path = os.path.join(prefix, label)
        if not os.path.isdir(path):
            continue
        photos = [PhotoObj(path,filename, label) for filename in os.listdir(path) if filename.endswith(extensions)]
        photoarr.extend(photos)
    return PhotoArray(photoarr), labels

        #lbdict[label] = {}
        #lbdict[label]['photos'] = photos
        #lbdict[label]['paths'] = [os.path.join(path, photo) for photo in photos]
    #return lbdict
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
        trainphotos.append(PhotoArray())
        trainpaths.append(PhotoArray())
        testphotos.append(PhotoArray())
        testpaths.append(PhotoArray())
        for index in trainidxlist:
            trainphotos[counter].extend(fullset.get_photos_by_index(index))
            trainpaths[counter].extend(fullset.get_paths_by_index(index))
        for index in testidxlist:
            testphotos[counter].extend(fullset.get_photos_by_index(index))
            testpaths[counter].extend(fullset.get_paths_by_index(index))
        counter = counter+1
    return trainphotos, trainpaths, testphotos, testpaths
