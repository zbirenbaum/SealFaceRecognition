import numpy as np
import os
from pathlib import Path

def gen_dict(folderdir, exclude=None):
    if exclude is None:
        exclude=0
    return get_photo_directories(folderdir, exclude)

def get_photos_in_dir(path):
    extensions = ('png', 'jpg', 'jpeg')
    photolist = [str(path) + filename for filename in os.listdir(path) if filename.endswith(extensions)]
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
