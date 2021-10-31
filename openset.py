import dirhandler as dh
import traintestsplit as ttsplit
import json


def write_dicts(dictdict):
    for key in dictdict:
        filename = 'openset_splits/' + key + '.json'
        with open('openset_splits/' + key + '.json', 'w') as f:
            json.dump(dictdict[key], f)
            f.close()
            print(filename + " written")
    return
            
def gen_validation(src):
    valdict = {}
    for key in src:
        valdict[key] = [src[key].pop(0)]
    return valdict

def gen_train_list(photodirs,divisor):
    trainlist=[]
    i = 0
    for i in range(len(photodirs)//divisor):
       trainlist.append(photodirs[i]) 
    return trainlist

def gen_dict_from_list(lst):
    ddict = {}
    for photodir in lst:
        ddict[photodir] = dh.get_photos_in_dir(photodir)
    return ddict
        
def gen_openset():
    photodirs = dh.get_photo_dirs(path='final_dataset/processed', exclude=1)
    photodirs_eligable = dh.get_photo_dirs('final_dataset/processed', exclude=5)
    trainlist= []
    testlist= []
    print(len(photodirs_eligable))
    print(len(photodirs))
    for photodir in photodirs:
        if photodir not in photodirs_eligable:
            testlist.append(photodir)
            
    trainlist = gen_train_list(photodirs_eligable,2)
    
    testlist.extend(photodirs_eligable[len(trainlist):].copy())
    
    traindict = gen_dict_from_list(trainlist)
    testdict = gen_dict_from_list(testlist)
    valdict = gen_validation(traindict)
#     print(len(photodirs))
#     print(len(traindict.keys()))
#     print(len(testdict.keys()))
# 
#     print("trainlist"+str(len(trainlist)))
#     print("testlist"+str(len(testlist)))

    for key in valdict:
#        print(valdict[key])
        if valdict[key][0] in traindict[key]:
            print("error")
    dictdict = {
                'train': traindict,
                'validation': valdict,
                'test': testdict,
                }
    write_dicts(dictdict)
    print('done')
    

gen_openset() 
