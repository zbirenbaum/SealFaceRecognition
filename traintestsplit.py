from __future__ import division
import dirhandler as dh
import calcindices as ci
import numpy as np
import os
import utils as ut


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
        if settype=='open':
            self.settype='open'
            self.ttdict = self.gen_open_ttdict()
            self.write_ttdict('open')
        else:
            self.settype='closed'
            self.ttdict = self.gen_closed_ttdict()
            self.write_ttdict('closed')

        if usedict == 1:
            for fold in range(1, kfold+1):
                self.dsetbyfold.append(ut.Dataset(ddict=self.ttdict[fold]['training'])) 
                self.testsetbyfold.append(self.ttdict[fold]['testing'])

        return

    def gen_set_info(self):
        total_classes = len(self.data.keys())
        training_num_classes = []
        if self.settype == 'open':
            for fold in self.ttdict.keys():
                training_num_classes.append(len(self.ttdict[fold]['training'].keys()))
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
            photoidx_training, photoidx_testing = ci.calcindices([],[],0,len(photolist), self.kfold)
            for fold in range(1, self.kfold+1):
                photos_training = list(photolist[photoidx_training[fold-1]])
                photos_testing = list(photolist[photoidx_testing[fold-1]])
                closeddict[fold]['training'][label] = photos_training
                closeddict[fold]['testing'][label] = photos_testing

        return closeddict

    def gen_open_ttdict(self):
        self.open_training_idx, self.open_testing_idx = ci.calcindices([],[],0,len(self.data.keys()), self.kfold)
        ttdict = {}
        for fold in range(1,self.kfold+1):
            ttdict[fold] = {
                    'training': {key : self.data[key]['photos'] for key in self.open_training_idx[fold-1]},
                    'testing': {key : self.data[key]['photos'] for key in self.open_testing_idx[fold-1]}
                    }
        return ttdict

    def write_ttdict(self, settype):
        for fold in range(1, self.kfold+1):
            if settype == 'closed':
                to_write_training = self.ttdict[fold]['training']
                to_write_testing = self.ttdict[fold]['testing']
                num_training_classes = len(to_write_training.keys())
                num_testing_classes = len(to_write_testing.keys())
            elif settype == 'open':
                to_write_training = self.ttdict[fold]['training']
                to_write_testing = self.ttdict[fold]['testing']
                num_training_classes = len(to_write_training.keys())
                num_testing_classes = num_training_classes#len(to_write_testing.keys()) + num_training_classes
            else:
                return "ERROR"

            self.create_set(to_write_training, settype, 'train', fold, num_training_classes)
            self.create_set(to_write_testing, settype, 'test', fold, num_testing_classes)
            self.create_probe(to_write_testing, settype, 'probe', fold, num_testing_classes)
        return



    def create_probe(self, ttdict, settype, typett, fold, num_classes):
        splits_dir = os.path.join(os.path.expanduser('./splits/{}/fold{}'.format(settype,fold)))
        if not os.path.isdir(splits_dir):
            os.makedirs(splits_dir)
        fname = './splits/{}/fold{}/{}.txt'.format(settype, fold, typett)
        with open(fname, 'w') as f:
            f.write('Total_Number_Of_Classes' + ' ' + str(num_classes) + '\n')
            for label in ttdict.keys():
                for photopath in ttdict[label]:
                    f.write(photopath + ' ' + str(label) + '\n')
                    break
        f.close()
        return



    def create_set(self, ttdict, settype, typett, fold, num_classes): 
        splits_dir = os.path.join(os.path.expanduser('./splits/{}/fold{}'.format(settype,fold)))
        if not os.path.isdir(splits_dir):
            os.makedirs(splits_dir)
        fname = './splits/{}/fold{}/{}.txt'.format(settype, fold, typett)
        with open(fname, 'w') as f:
            f.write('Total_Number_Of_Classes' + ' ' + str(num_classes) + '\n')
            for label in ttdict.keys():
                for photopath in ttdict[label]:
                    f.write(photopath + ' ' + str(label) + '\n')
        f.close()
        return
