import os
from pathlib import Path 



def generate_dataset(dir, exclude=None):
    if exclude is None:
        exclude = 0
    return read_labels(dir, exclude)

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


def get_label_directories(dir, exclude):
    photodir = str(Path(dir).resolve())
    assert(os.path.exists(str(photodir)))
    excludelist = []
    full_labels = [dir for dir in os.listdir(str(photodir)) if not dir.startswith(".")]
    postexclude = []
    photolist = []
    counter = 0
    for label in full_labels:
        photos = []
        path = os.path.join(photodir, label)
        if not os.path.isdir(path):
            continue
       
        photos = get_photos_in_dir(path, label, counter)
#        print(photos)
 #       print(photos['photos'])
 #       print(len(photos['photos']))
        if len(photos['photos']) < exclude:
            excludelist.append(label)
            continue
        else:
            postexclude.append(label)
            photolist.append(photos)
            counter = counter + 1

    return photolist, postexclude

def read_labels(dir, exclude):
   dictlist, labels = get_label_directories(dir, exclude)
#   print(labels)
   return dictlist



