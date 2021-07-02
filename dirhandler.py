import os
from pathlib import Path 



def generate_dataset(dir):
    return read_labels(dir)

def get_photos_in_dir(path, label, index):
    extensions = ('png', 'jpg', 'jpeg')
    dict = {
            "label" : label,
            "photos" : [],
            "originalindex" : index
            }
    for filename in os.listdir(path):
        if filename.endswith(extensions):
            photopath = os.path.join(path, filename)
            photoname = filename
            photolabel = label
            indict = {"photopath" : photopath,
                    "photoname" : photoname,
                    "photolabel" : photolabel
                    }
            dict['photos'].append(indict)
    return dict


def get_label_directories(dir):
    photodir = str(Path(dir).resolve())
    assert(os.path.exists(str(photodir)))
    labels = [dir for dir in os.listdir(str(photodir)) if not dir.startswith(".")]
    return photodir, labels

def read_labels(dir):
    photodir, labels = get_label_directories(dir)
    dictlist = []
    #dict= {"labels" : labels}
    counter = 0
    for label in labels:
        dictlist.append({})
        path = os.path.join(photodir, label)
        if not os.path.isdir(path):
            continue
        dictlist[counter] = get_photos_in_dir(path, label, counter)
        counter = counter + 1
    return dictlist



