from __future__ import division
import utils
import dirhandler as dh
import datasplitter as ds
import numpy as np
import os
import utils as ut
from pdb import set_trace as bp

def gen_full_dict(dir, startat=0):
    fulldict = {}
    data = dh.gen_dict(dir, startat=startat)
    for label in data.keys():
        labeldict = data[label]
        photolist = np.array(labeldict['photos'])
        fulldict[label] = photolist
    return fulldict

def create_split_probe_dict(dir, startat):
    ttdict = gen_full_dict(dir, startat)
    probeset = {}
    for label in ttdict.keys():
        for photopath in ttdict[label]:
            probeset[label] = [photopath]
            break
    return probeset

def create_probe_dict(ttdict):
    probeset = {}
    for label in ttdict.keys():
        for photopath in ttdict[label]:
            probeset[label] = [photopath]
            break
    return probeset

def gen_probes_from_dir(probedir):
    presplitprobes = create_probe_dict(dh.gen_dict(probedir, 0))
    return presplitprobes

def ignore(k):
    k=k+0
    return

class DatasetBuilder(object):
    def __init__(self, photodir, kfold,usedict=1, exclude=None, settype=None):
        self.photodir = photodir
        self.kfold = kfold
        
        if exclude is None:
            exclude = kfold
        self.exclude = exclude
        self.data = dh.gen_dict(photodir, self.exclude)
        self.dsetbyfold = []
        self.testsetbyfold = []
        self.probesetbyfold = []
        self.probeset = {} 
        if settype=='open':
            self.settype='open'
            self.ttdict = self.gen_open_ttdict()
            self.write_ttdict('open')
        elif settype == 'both':
            self.settype='both'
            self.ttdict = self.gen_both()
            self.write_ttdict('both')
            for fold in range(1, kfold+1):
                self.dsetbyfold.append(self.ttdict[fold]['training'])
                self.probesetbyfold.append(self.ttdict[fold]['probes'])
                self.testsetbyfold.append(self.ttdict[fold]['testing'])
        else:
            self.settype='closed'
            self.ttdict = self.gen_closed_ttdict()
            self.write_ttdict('closed')

        if usedict == 1 and settype != 'both':
            for fold in range(1, kfold+1):
                self.dsetbyfold.append(self.ttdict[fold]['training'])
                self.testsetbyfold.append(self.ttdict[fold]['testing'])
                self.probesetbyfold.append(create_probe_dict(self.ttdict[fold]['testing']))
        return

    def gen_set_info(self):
        total_classes = len(self.data.keys())
        training_num_classes = []
        if self.settype == 'open':
            for fold in self.ttdict.keys():
                training_num_classes = (len(self.ttdict[fold]['training'].keys()))
        else:
            for k in range(self.kfold):
                ignore(k)
                training_num_classes.append(total_classes)
        
        return total_classes, training_num_classes

    def gen_closed_ttdict(self):
        closeddict = {}
        for fold in range (1, self.kfold+1):
            closeddict[fold] = {
                    'training':{},
                    'testing':{}
                    }
        for label in self.data.keys():
            labeldict = self.data[label]
            photolist = np.array(labeldict['photos'])
            photoidx_training, photoidx_testing = ds.calcindices([],[],0,len(photolist), self.kfold)
            for fold in range(1, self.kfold+1):
                photos_training = list(photolist[photoidx_training[fold-1]])
                photos_testing = list(photolist[photoidx_testing[fold-1]])
                closeddict[fold]['training'][label] = photos_training
                closeddict[fold]['testing'][label] = photos_testing

        return closeddict

    def gen_full_ttdict(self):
        fulldict = {}
        for label in self.data.keys():
            labeldict = self.data[label]
            photolist = np.array(labeldict['photos'])
            fulldict[label] = photolist

        return fulldict

    def gen_open_ttdict(self):
        self.open_training_idx, self.open_testing_idx = ds.calcindices([],[],0,len(self.data.keys()), self.kfold)
        ttdict = {}
        for fold in range(1,self.kfold+1):
            ttdict[fold] = {
                    'training': {key : self.data[key]['photos'] for key in self.open_training_idx[fold-1]},
                    'testing': {key : self.data[key]['photos'] for key in self.open_testing_idx[fold-1]},
                    }
        return ttdict

    def gen_both(self):
        self.open_training_idx, self.open_testing_idx = ds.calcindices([],[],0,len(self.data.keys()), self.kfold)
        ttdict = {}
        for fold in range(1,self.kfold+1):
            ttdict[fold] = {'training': {}, 'testing': {}, 'probes': {}}
            for key in self.open_training_idx[fold-1]:
                photos = self.data[key]['photos'][:]
                #print(photos)
                holdout = photos.pop(fold-1)
                ttdict[fold]['training'][key] = photos
                ttdict[fold]['probes'][key]  = [holdout]
                ttdict[fold]['testing'][key] = [holdout]
            for key in self.open_testing_idx[fold-1]:
                photos = self.data[key]['photos'][:]
                ttdict[fold]['probes'][key] = photos
        return ttdict

    def write_ttdict(self, settype):
        for fold in range(1, self.kfold+1):
            if settype == 'closed':
                to_write_training = self.ttdict[fold]['training']
                to_write_testing = self.ttdict[fold]['testing']
                num_training_classes = len(to_write_training.keys())
                num_testing_classes = len(to_write_testing.keys())
                self.create_probe(to_write_testing, settype, 'probe', fold, num_testing_classes)
            elif settype == 'open':
                to_write_training = self.ttdict[fold]['training']
                to_write_testing = self.ttdict[fold]['testing']
                num_training_classes = len(to_write_training.keys())
                num_testing_classes = num_training_classes#len(to_write_testing.keys()) + num_training_classes
                self.create_probe(to_write_testing, settype, 'probe', fold, num_testing_classes)
            elif settype == 'both': 
                to_write_training = self.ttdict[fold]['training']
                to_write_testing = self.ttdict[fold]['testing'] #eval during training
                to_write_probes = self.ttdict[fold]['probes'] #eval afer training
                #print(to_write_probes)
                num_training_classes = len(to_write_training.keys())
                num_testing_classes = len(to_write_testing.keys())
                self.create_set(to_write_probes, settype, 'probe', fold, num_testing_classes)
            else:
                return "ERROR"
            self.create_set(to_write_training, settype, 'train', fold, num_training_classes)
            self.create_set(to_write_testing, settype, 'test', fold, num_testing_classes)
        return


    def create_probe_from_dict(self, ttdict, settype, typett, fold, num_classes):
        probeset = {}
        splits_dir = os.path.join(os.path.expanduser('./splits/{}/fold{}'.format(settype,fold)))
        if not os.path.isdir(splits_dir):
            os.makedirs(splits_dir)
        fname = './splits/{}/fold{}/{}.txt'.format(settype, fold, typett)
        with open(fname, 'w') as f:
            for label in ttdict.keys():
                for photopath in ttdict[label]:
                    probeset[label] = [photopath]
                    f.write(photopath + ' ' + str(label) + '\n')
                    break
        f.close()
        self.probesetbyfold.append(probeset)
        return

    def create_probe(self, ttdict, settype, typett, fold, num_classes):
        probeset = {}
        splits_dir = os.path.join(os.path.expanduser('./splits/{}/fold{}'.format(settype,fold)))
        if not os.path.isdir(splits_dir):
            os.makedirs(splits_dir)
        fname = './splits/{}/fold{}/{}.txt'.format(settype, fold, typett)
        with open(fname, 'w') as f:
            for label in ttdict.keys():
                for photopath in ttdict[label]:
                    probeset[label] = [photopath]
                    f.write(photopath + ' ' + str(label) + '\n')
                    break
        f.close()
        self.probesetbyfold.append(probeset)
        return

    def create_set(self, ttdict, settype, typett, fold, num_classes): 
        splits_dir = os.path.join(os.path.expanduser('./splits/{}/fold{}'.format(settype,fold)))
        if not os.path.isdir(splits_dir):
            os.makedirs(splits_dir)
        fname = './splits/{}/fold{}/{}.txt'.format(settype, fold, typett)
        with open(fname, 'w') as f:
            for label in ttdict.keys():
                for photopath in ttdict[label]:
                    f.write(photopath + ' ' + str(label) + '\n')
        f.close()
        return

    def gen_sub_ttdict(data, kfold):
        closeddict = {}
        for fold in range (1, self.kfold+1):
            closeddict[fold] = {
                    'training':{},
                    'testing':{}
                    }
        for label in data.keys():
            labeldict = data[label]
            photolist = np.array(labeldict['photos'])
            photoidx_training, photoidx_testing = ds.calcindices([],[],0,len(photolist), kfold)
            for fold in range(1, kfold+1):
                photos_training = list(photolist[photoidx_training[fold-1]])
                photos_testing = list(photolist[photoidx_testing[fold-1]])
                closeddict[fold]['training'][label] = photos_training
                closeddict[fold]['testing'][label] = photos_testing

        return closeddict
