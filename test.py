import dirhandler as dh
import json

def check(photodirs_all,photodirs_eligable, photodirs_ineligable, listphotos_all,listphotos_eligable, listphotos_ineligable):
    
    ld_all = len(photodirs_all)
    ld_eligable = len(photodirs_eligable)
    ld_ineligable = len(photodirs_ineligable)
    error_dirs = ld_all-(ld_eligable+ld_ineligable)

    print("Number of Directories: ")
    print("all: " + str(len(photodirs_all)))
    print("eligable: " + str(len(photodirs_eligable)))
    print("ineligable: " + str(len(photodirs_ineligable)))
    print("Error Test: " + str(error_dirs) + "\n")
    
    lp_all = len(listphotos_all)
    lp_eligable = len(listphotos_eligable)
    lp_ineligable = len(listphotos_ineligable)
    error_photos = lp_all-(lp_eligable+lp_ineligable)
    
    print("Number of Total Photos: ")
    print("all: " + str(len(listphotos_all)))
    print("eligable: " + str(len(listphotos_eligable)))
    print("ineligable: " + str(len(listphotos_ineligable)))
    print("Error Test: " + str(error_photos) + "\n")

    n_train = lp_eligable - ld_eligable
    print("Metrics: ")
    print("Training: " + str(n_train))
    print("Validation: " + str(ld_eligable))
    print("Testing: " + str(lp_ineligable))
    
    return

    
def gen_ineligable(all, eligable):
    photodirs_ineligable = []
    for photodir in all:
        if photodir not in eligable:
            photodirs_ineligable.append(photodir)
    return photodirs_ineligable

def gen_list(photodirs):
    listphotos = []
    for dir in photodirs:
        listphotos.extend(dh.get_photos_in_dir(dir))
    return listphotos

photodirs_all = dh.get_photo_dirs(path='final_dataset/processed', exclude=1)
photodirs_eligable = dh.get_photo_dirs(path='final_dataset/processed', exclude=5)
photodirs_ineligable = gen_ineligable(photodirs_all, photodirs_eligable)


listphotos_all = gen_list(photodirs_all)
listphotos_eligable = gen_list(photodirs_eligable)
listphotos_ineligable = gen_list(photodirs_ineligable)

check(photodirs_all,photodirs_eligable, photodirs_ineligable, listphotos_all,listphotos_eligable, listphotos_ineligable)
#photodirs_eligable = dh.get_photo_dirs('final_dataset/processed', exclude=4)

# def load_open_split(filename):
#     with open("./openset_splits/" + filename + ".json", "r") as infile:
#         return json.load(infile)
# 
# train = load_open_split('train')
# for key in train.keys():
#     for val in train[key]:
#         print(val)
