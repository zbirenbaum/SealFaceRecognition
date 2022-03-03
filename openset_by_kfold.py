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

def gen_dict_from_list(fold_list):
    list_dict = []
    for lst in fold_list:
        ddict = {}
        for photodir in lst:
            ddict[photodir] = dh.get_photos_in_dir(photodir)
        list_dict.append(ddict.copy())
    return list_dict 

def calcindices(photodirs, counter, kfold):
    increment = math.ceil(len(photodirs)/kfold)
    start_ind = counter * increment
    end_ind = start_ind+increment
    test = photodirs[start_ind:end_ind]
    train = [photodir for photodir in photodirs if photodir not in test]
    return train, test

def gen_validation(listsrc, kfolds):
    valdict_list= []
    for src in listsrc:
        valdict = {}
        for key in src: 
            n_photos=len(src[key])
            n_remove = n_photos//kfolds
            for _ in range(n_remove):
                idx = random.randint(0, len(src[key])-1)
                valdict[key] = [src[key].pop(idx)]
        valdict_list.append(valdict.copy())
    return valdict_list

def gen_train_test(photodirs, photodirs_eligable, kfold):
    testlist = []
    trainlist = []
    for i in range(kfold):
        train, test = calcindices(photodirs_eligable, i, kfold)
        trainlist.append(train)
        for photodir in photodirs: #place all directories with not enough seals in open set
            if photodir not in photodirs_eligable:
                test.append(photodir)
        testlist.append(test)
    return gen_dict_from_list(trainlist), gen_dict_from_list(testlist)

def validate_split(traindict, valdict):
    for key in valdict: #make sure no photos in val set still in training
        if valdict[key][0] in traindict[key]:
            print("Error: Photo in val set also in training")
            exit(1)

def validate_folds(traindict_list, testdict_list):
    for i in range(len(traindict_list)-1):
        print("Train Intersect: " + str(len(set(traindict_list[i]).intersection(traindict_list[i+1]))))
        print("Test Intersect: " + str(len(set(testdict_list[i]).intersection(testdict_list[i+1]))))
        print("Test Intersect With Train: " + str(len(set(traindict_list[i]).intersection(testdict_list[i]))))

def gen_openset(photodirs, photodirs_eligable, kfold):
    fold_list=[]
    traindict_list, testdict_list = gen_train_test(photodirs, photodirs_eligable, kfold)
    valdict_list = gen_validation(traindict_list, kfold)
    validate_folds(traindict_list, testdict_list)
    for i in range(kfold):
        validate_split(traindict=traindict_list[i], valdict=valdict_list[i])
        splits = {
                'train': traindict_list[i],
                'validation': valdict_list[i],
                'test': testdict_list[i]
                }
        fold_list.append(splits.copy())
    return fold_list

def gen_splits(dir, kfold):
    photodirs = dh.get_photo_dirs(path=dir, exclude=1)
    photodirs_eligable = dh.get_photo_dirs(path=dir, exclude=kfold)
    openset_folds = gen_openset(photodirs, photodirs_eligable, kfold)
    for i in range(kfold):
        write_dicts(openset_folds[i], i+1)

gen_splits('final_dataset/processed', 5)
