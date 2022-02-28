import dirhandler as dh
import traintestsplit as ttsplit
import json
import os
import random

COMMON_THRESH = .5
FOLDS = 5

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

def gen_dict_from_list(lst):
    ddict = {}
    for photodir in lst:
        ddict[photodir] = dh.get_photos_in_dir(photodir)
    return ddict

def gen_validation(src):
    valdict = {}
    for key in src: 
        idx = random.randint(0, len(src[key])-1)
        valdict[key] = [src[key].pop(idx)]
    return valdict

def get_random_dirs(photodirs, n_training_dirs):
    rand_dirs = []
    while len(rand_dirs) < n_training_dirs:
        rand = random.randint(0, len(photodirs)-1)
        rand_dirs.append(photodirs.pop(rand))
    return rand_dirs

def gen_train_list(photodirs,divisor):
    trainlist=[]
    n_training_dirs = len(photodirs)//divisor
    trainlist = get_random_dirs(photodirs, n_training_dirs)
    return trainlist

def gen_train_test():
    photodirs = dh.get_photo_dirs(path='final_dataset/processed', exclude=1)
    photodirs_eligable = dh.get_photo_dirs('final_dataset/processed', exclude=5)
    testlist = []
    for photodir in photodirs: #place all directories with not enough seals in open set
        if photodir not in photodirs_eligable:
            testlist.append(photodir)
    trainlist = gen_train_list(photodirs_eligable, 2)
    testlist.extend(photodirs_eligable.copy())
    return gen_dict_from_list(trainlist), gen_dict_from_list(testlist)

def validate_split(traindict, testdict, valdict):
    for key in valdict: #make sure no photos in val set still in training
        if valdict[key][0] in traindict[key]:
            print("Error: Photo in val set also in training")
            exit(1)

    for key in testdict.keys(): #make sure no seals in test set are in train
        if key in traindict.keys():
            print("Error: Seal in test set also in train")
            exit(1)

def get_intersections(folds_list):
    common = []
    for i in range(len(folds_list)):
        common.append([])
        for j in range(len(folds_list)):
            if j == i:
                continue
            common[i].append(len(list(set(folds_list[i]['train']).intersection(folds_list[j]['train']))))
    return common

def validate_folds(folds_list):
    common = get_intersections(folds_list)
    maximum=0
    for list in common:
        idx = common.index(list)
        foldmax = max(list)/len(folds_list[idx]['train'])
        if maximum < foldmax:
            maximum = foldmax
        print("Fold-" + str(idx+1) + " max common train dirs with all folds: " + str(max(list)) + "/" + str(len(folds_list[idx]['train'])) + " = " + str(foldmax))
    return maximum

def gen_openset(nfold):
    fold_list=[]
    for _ in range(nfold):
        traindict, testdict = gen_train_test()
        valdict = gen_validation(traindict)
        splits = {
                'train': traindict,
                'validation': valdict,
                'test': testdict,
                }
        fold_list.append(splits.copy())
    return fold_list

fold_list = gen_openset(FOLDS)
maximum = validate_folds(fold_list)
while(maximum > COMMON_THRESH):
    print("Max: " + str(maximum) + " over alloted % " + str(COMMON_THRESH) + ", rerunning...")
    fold_list = gen_openset(FOLDS)
    maximum = validate_folds(fold_list)

fold_counter = 1
for splits in fold_list:
    write_dicts(splits, fold_counter)
    fold_counter = fold_counter+1
