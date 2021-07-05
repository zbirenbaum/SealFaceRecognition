import dirhandler as dh
import math
import os
class Dataset(object):
    """
    set_byfold[fold] = list(labeldicts)
    labeldict dict_keys(['photos', 'label', 'originalindex'])
    labeldict['photos'] = list of dictionaries with photoinfo
    """
    def __init__(self, dir, kfold, exclude=None):
        if exclude is None:
            print("excluding directories with < #fold photos for closed")
            exclude = kfold
        self.exclude = exclude
        self.dir = dir
        self.kfold = kfold
        self.openset()
        self.closedset()
        self.write_open()
        self.write_closed()
#        print(self.closeddata)

    def openset(self):
        self.opendata = get_fulldata(self.dir, 0)
        self.openlabels = len(self.opendata)
        self.opentrainidxarr, self.opentestidxarr = calcindices([], [], 0, self.openlabels, self.kfold)  # array of arrays, each holds classes to train on for fold[idx+1]
        opentraining_by_fold, opentesting_by_fold = get_k_splits(
                self.kfold, 
                self.opendata, 
                self.opentrainidxarr, 
                self.opentestidxarr
                )
        self.opentraining_by_fold = gen_set_photos_by_fold(opentraining_by_fold)
        self.opentesting_by_fold = gen_set_photos_by_fold(opentesting_by_fold)
        return

    def closedset(self):
        self.closeddata = get_fulldata(self.dir, self.exclude)
        dictvar = {}
        photopaths = []
        for photoset in self.closeddata:
            photopaths = []
            for photo in photoset['photos']:
                photopaths.append(photo['photopath'])
            dictvar[photoset['label']] = photopaths
            #dict[photoset['label']] = [photolist for photolist in photoset['photos']['photopath']]
        #print(dict)
        #print("data" + str(self.closeddata[1]))
#        print(self.closeddata)
        self.splitperlabel = []
        self.closedtestidxarr = []
        self.closedtrainidxarr = []
        for counter in range (0, kfold):
            self.closedtestidxarr.append([])
            self.closedtrainidxarr.append([])
            self.closedtrainidxarr[counter] = {}
            self.closedtestidxarr[counter] = {}


        for set in self.closeddata:
            label = set['label']
            photos = set['photos']
            num_photos = len(photos)
            append_train, append_test = calcindices([],[],0,num_photos,kfold)
            for counter in range(0, kfold):
                self.closedtrainidxarr[counter][label] = append_train[counter]
                self.closedtestidxarr[counter][label] = append_test[counter]

        #print(self.closedtestidxarr[0]) 
        self.closedtraining_by_fold, self.closedtesting_by_fold = get_k_splits_closed(
            self.kfold, 
            dictvar, 
            self.closedtrainidxarr, 
            self.closedtestidxarr
        )
        #print(self.closedtesting_by_fold)
        print(type(self.closedtraining_by_fold))

        print(type(self.opentesting_by_fold))
        print(type(self.opentraining_by_fold))
            #self.splitperlabel.append()
        return

    def get_opensets(self):
            return self.opentraining_by_fold, self.opentesting_by_fold
    
    def get_closedsets(self):
        print(self.closedtesting_by_fold)
        return self.closedtraining_by_fold, self.closedtesting_by_fold


    def write_closed(self):
        to_write_training, to_write_testing = self.get_closedsets()
        for k in range(1, kfold+1):
            create_set(to_write_training[k-1], "closed", "training", k)
            create_set(to_write_testing[k-1], "closed", "testing", k)
        return

    def write_open(self):
        to_write_training, to_write_testing = self.get_opensets()
        for k in range(1, kfold+1):
            create_set(to_write_training[k-1], "open", "training", k)
            create_set(to_write_testing[k-1], "open", "testing", k)
        return 


def get_fulldata(dir, exclude):
    fulldata = dh.generate_dataset(dir, exclude)
    return fulldata

def get_k_splits_closed(kfold, fulldata, trainidxarr, testidxarr):
    training_by_fold = []
    testing_by_fold = []
    for k in range(0,kfold):
        training_by_fold.append(gen_fold_split_closed(trainidxarr[k], fulldata))
        testing_by_fold.append(gen_fold_split_closed(testidxarr[k], fulldata))
    return training_by_fold, testing_by_fold


def get_k_splits(kfold, fulldata, trainidxarr, testidxarr):
    training_by_fold = []
    testing_by_fold = []
    for k in range(0,kfold):
       # print(trainidxarr[k])
        training_by_fold.append(gen_fold_split(trainidxarr[k], fulldata))
        testing_by_fold.append(gen_fold_split(testidxarr[k], fulldata))
    return training_by_fold, testing_by_fold

def gen_fold_split(indices, fulldata):
    fold_photos = []
    for index in indices:
        fold_photos.append(fulldata[index])
    return fold_photos

def gen_fold_split_closed(indices, fulldata):
    fold_photos = [] 
    for label in indices.keys():
        for index in indices[label]:
            fold_photos.append(fulldata[label][index])
    #print(fold_photos)
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
        #print("FOLD: " + str(i))
        originallist = []
        for labeldict in setbyfold[i]:
            originallist.append(labeldict['originalindex'])
        originallistbyfold.append(originallist)

    return originallistbyfold

def label_photos(setbyfold, kfold):
    photoslistbyfold=[]
    for i in range (0, kfold):
        #print("FOLD: " + str(i))
        photoslist = []
        for labeldict in setbyfold[i]:
            photoslist.append(labeldict['photos'])
        #    for something in labeldict['photos']:
         #       print(something['photopath'] + " " + something['photolabel'])
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


def create_set(listtowrite, settype, typett, k): 
    print(type(listtowrite[0]))
    splits_dir = os.path.join(os.path.expanduser('./splits/fold{}/{}'.format(k,settype)))
    if not os.path.isdir(splits_dir):
        os.makedirs(splits_dir)
    fname = './splits/fold{}/{}/{}.txt'.format(k,settype, typett)
    with open(fname, 'w') as f:
        for photo in listtowrite:
            print(photo)
            f.write(photo + '\n')

kfold = 10 
dset = Dataset("photos", kfold)

   


#for settype in settypes:
#    to_write_training, to_write_testing = dset.getsets_by_type(settype)
#    print(type(to_write_testing[0]))
#    print(to_write_testing)

#    for typett in types:
#        for k in range(1,kfold+1):
#            create_set(to_write_training[k-1], settype, typett, k)
        #print(dset.closedtestidxarr)



#datatypes = ["training", "testing"]

#    create_set(to_write_testing[k-1], "open","testing", k)






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

