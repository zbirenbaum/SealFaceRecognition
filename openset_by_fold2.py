import dirhandler as dh
import random
import math
import os
import json

def write_dicts(splits, fold):
    foldstr = str(fold) + "/"
    for key in splits:
        filedir = 'openset_splits/' + foldstr
        filename = filedir + key + '.json'
        if not os.path.exists(filedir):
            os.mkdir(filedir)
        with open(filename, 'w') as f:
            json.dump(splits[key], f)
            f.close()
            print(filename + " written")
    return

def gen_dict_from_list(lst, kfold):
    list_dict = []
    for _ in range(kfold):
        ddict = {}
        for photodir in lst:
            ddict[photodir] = dh.get_photos_in_dir(photodir)
        list_dict.append(ddict.copy())
    return ddict

def calcindices(photodirs, counter, kfold):
    increment = math.ceil(len(photodirs)/kfold)
    start_ind = counter * increment
    end_ind = start_ind+increment
    test = photodirs[start_ind:end_ind]
    train = [photodir for photodir in photodirs if photodir not in test]
    return train, test

def gen_validation(src, kfolds):
    valdict = {}
    for key in src: 
        n_photos=len(src[key])
        n_remove = n_photos//kfolds
        for _ in range(n_remove):
            idx = random.randint(0, len(src[key])-1)
            valdict[key] = [src[key].pop(idx)]
    return valdict

def gen_train_test(photodirs, photodirs_eligable, kfold):
    testlist = []
    trainlist = []
    for i in range(kfold):
        train, test = calcindices(photodirs_eligable, i, kfold)
        trainlist.append(train)
        testlist.append(test)
        for photodir in photodirs: #place all directories with not enough seals in open set
            if photodir not in photodirs_eligable:
                testlist.append(photodir)
    return gen_dict_from_list(trainlist), gen_dict_from_list(testlist)

def gen_openset(photodirs, photodirs_eligable, kfold):
    fold_list=[]
    traindict, testdict = gen_train_test(photodirs, photodirs_eligable, kfold)
    valdict = gen_validation(traindict, kfold)
    for i in range[kfold]:
        splits = {
                'train': traindict[i],
                'validation': valdict[i],
                'test': testdict[i]
                }
        fold_list.append(splits.copy())
    return fold_list

def gen_splits(dir, kfold):
    photodirs = dh.get_photo_dirs(path=dir, exclude=1)
    photodirs_eligable = dh.get_photo_dirs(dir, exclude=kfold)
    openset_folds = gen_openset(photodirs, photodirs_eligable, kfold)
    for i in range(kfold):
        write_dicts(openset_folds[i], i)

gen_splits('final_dataset/processed', 5)
