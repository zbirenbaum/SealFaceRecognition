import numpy as np
import os
from pathlib import Path






def get_photos_in_dir(path):
    
    extensions = ('png', 'jpg', 'jpeg')
    photolist = [
            str(path) + '/' + filename for filename in os.listdir(path) \
                    if filename.endswith(extensions) \
                    and not filename.startswith('.')]
    return photolist





def gen_dict_for_dir(path, photoname):
    photodict = {}
    photodict[path] = {'name': folder, 'photos': photos}
    return


def gen_dict(folderdir, exclude=None):
    if exclude is None:
        exclude=0
    return get_photo_directories(folderdir, exclude)


def get_subdirs(path, exclude):
    photolist = get_photos_in_dir(path)
    if len(photolist) > 0:
        if len(photolist) < exclude:
            return []
    else:
        for entry in os.listdir(str(path)):
            entrypath = path + '/' + entry
            if not entry.startswith(".") and os.path.isdir(entrypath):
                photos_in_subdirs = get_subdirs(entrypath, exclude)
                #if photos_in_subdirs >= exclude:
                photolist.extend(photos_in_subdirs)

    return photolist

def get_photo_directories(folderdir, exclude):
    photodir = str(Path(folderdir).resolve())
    assert(os.path.exists(str(photodir)))
    folderlist = [dir for dir in os.listdir(str(photodir)) if not dir.startswith(".")]
    mapdict = {}
    counter = 0
    for folder in folderlist:
        path_to_folder = os.path.join(photodir, folder)
        if not os.path.isdir(path_to_folder):
            continue
        photos = list(get_photos_in_dir(path_to_folder))
        if len(photos) < exclude:
            continue
        else:
            mapdict[counter] = {'name': folder, 'photos': photos}
            counter = counter + 1
    return mapdict 








