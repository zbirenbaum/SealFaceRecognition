from __future__ import print_function
from __future__ import division
import os
from pathlib import Path

class DataBuilder(object):
    def __init__(self, directory):
        self.dir = directory
        #self.lbdict = read_labels(directory)
        #self.frame = self.gen_frame()
        self.photoarr = read_labels(directory)
        return

    def get_photos(self):
        return self.photoarr


class PhotoObj(object):
    def __init__(self, path, filename, label):
        self.filename = filename
        self.path = os.path.join(path, filename)
        self.label = label
        return
    def getlabel(self):
        """Return the label of the photo obj"""
        return self.label
    def getpath(self):
        """Return the absolute path of the photo obj"""
        return self.path
    def getfilename(self):
        """Return the filename of the photo obj"""
        return self.filename

class PhotoArray(object):
    def __init__(self, photoarr=None):
        if photoarr is None:
            self.photoarr = []
        else:
            self.photoarr = photoarr
        return

    def extend(self, toadd):
        self.photoarr.extend(toadd)
        return

    def get_labels(self):
        return set([photo.getlabel() for photo in self.photoarr])

    def get_photos(self):
        return self.photoarr

    def get_photo_names(self):
        return [photo.getfilename() for photo in self.photoarr]

    def get_photo_paths(self):
        return [photo.getpath() for photo in self.photoarr]

    def get_photos_by_label(self, label):
        return [photo.getfilename() for photo in self.photoarr if photo.getlabel() == label]

    def get_photos_by_index(self, index):
        return [photo.getfilename() for photo in self.photoarr if int(photo.getlabel()) == int(index+1)]

    def get_paths_by_label(self, label):
        return [photo.getpath() for photo in self.photoarr if photo.getlabel() == label]

    def get_paths_by_index(self, index):
        return [photo.getpath() for photo in self.photoarr if int(photo.getlabel()) == int(index+1)]


def read_labels(dir):
    extensions = ('png', 'jpg', 'jpeg')
    prefix = str(Path(dir).resolve())
    assert(os.path.exists(str(prefix)))
    labels = [i for i in os.listdir(str(prefix)) if not i.startswith(".")]
#    lbdict = {}
    photoarr = PhotoArray()
    for label in labels:
        path = os.path.join(prefix, label)
        if not os.path.isdir(path):
            continue
        photos = [PhotoObj(path,filename, label) for filename in os.listdir(path) if filename.endswith(extensions)]
        photoarr.extend(photos)
    return photoarr
        #lbdict[label] = {}
        #lbdict[label]['photos'] = photos
        #lbdict[label]['paths'] = [os.path.join(path, photo) for photo in photos]
    #return lbdict
